from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.vault_service import VaultService
from app.llm_factual_checker import check_factual_overlap
from app.risk_engine import calculate_risk


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="SentinelVault",
    description=(
        "Real-time AI output security and "
        "protected-data leakage detection system."
    ),
    version="1.0.0"
)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
@app.get("/")
def root():
    return FileResponse("static/index.html")

# --------------------------------------------------
# INITIALIZE VAULT ONCE
# --------------------------------------------------

vault = VaultService()


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class AnalyzeRequest(BaseModel):

    ai_output: str


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")

def health():

    return {
        "status": "healthy",
        "protected_documents": len(
            vault.documents
        ),
        "protected_chunks": len(
            vault.chunks
        )
    }


# --------------------------------------------------
# ANALYZE ENDPOINT
# --------------------------------------------------

@app.post("/analyze")
def analyze(
    request: AnalyzeRequest
):

    ai_output = request.ai_output


    # --------------------------------------------------
    # SEMANTIC SEARCH
    # --------------------------------------------------

    try:
        results = vault.search(
            query=ai_output,
            top_k=3
        )
    except Exception as e:
        return {"error": f"Vault search failed: {str(e)}"}


    if not results:

        semantic_score = 0.0

        factual_result = {
            "relationship": "NONE",
            "overlap_score": 0.0,
            "exposed_facts": [],
            "contradicted_facts": [],
            "explanation": (
                "No protected information "
                "was retrieved."
            )
        }

        risk_result = calculate_risk(
            semantic_score=0.0,
            factual_result=factual_result
        )

        return {
            "ai_output": ai_output,
            "semantic_score": 0.0,
            "matched_source": None,
            "factual_analysis": factual_result,
            "risk_analysis": risk_result
        }


    # --------------------------------------------------
    # BEST MATCH
    # --------------------------------------------------

    best_match = results[0]

    semantic_score = (
        best_match["similarity"]
    )


    # --------------------------------------------------
    # FACTUAL ANALYSIS
    # --------------------------------------------------

    if semantic_score >= 0.60:

        try:
            factual_result = check_factual_overlap(
                ai_output=ai_output,
                protected_context=best_match["content"]
            )
        except Exception as e:
            return {"error": f"Factual analysis failed: {str(e)}"}

    else:

        factual_result = {
            "relationship": "NONE",
            "overlap_score": 0.0,
            "exposed_facts": [],
            "contradicted_facts": [],
            "explanation": (
                "Semantic similarity is below "
                "the factual-analysis threshold."
            )
        }


    # --------------------------------------------------
    # RISK ANALYSIS
    # --------------------------------------------------

    risk_result = calculate_risk(
        semantic_score=semantic_score,
        factual_result=factual_result
    )


    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    below_threshold = semantic_score < 0.60

    return {

        "ai_output": ai_output,

        "semantic_analysis": {
            "similarity_score": round(
                semantic_score,
                4
            ),
            "source": None if below_threshold else best_match["document"],
            "matched_content": None if below_threshold else best_match["content"]
        },

        "factual_analysis": factual_result,

        "risk_analysis": risk_result
    }
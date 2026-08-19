import json
import os

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY was not found. "
        "Please add it to your .env file."
    )
os.environ.pop("GOOGLE_API_KEY", None)

# Explicitly use the Gemini key loaded from .env.
# Do not let the SDK choose GOOGLE_API_KEY.
client = genai.Client(
    api_key=api_key
)



# --------------------------------------------------
# Factual overlap checker
# --------------------------------------------------

def check_factual_overlap(
    ai_output: str,
    protected_context: str
):
    """
    Compare AI-generated output against protected
    information using an LLM.

    Possible relationships:
    MATCH
    PARTIAL
    CONTRADICTION
    NONE
    """

    prompt = f"""
You are a security-focused factual overlap detector.

Compare the AI-generated output with the protected
information.

Determine whether the AI output reveals facts contained
in the protected information.

Possible relationships:

MATCH:
The output reveals the same protected facts, even if
the wording is paraphrased.

PARTIAL:
The output reveals some protected facts but not all
important information.

CONTRADICTION:
The output discusses the same subject but gives a fact
that conflicts with the protected information.

NONE:
The output does not reveal meaningful protected facts.

Important rules:

- Focus on factual meaning, not exact wording.
- Do not assume high semantic similarity means factual overlap.
- Pay attention to names, departments, salaries, dates,
  financial values, project information, managers and
  other sensitive information.
- Distinguish contradictions from actual disclosure.
- Return ONLY valid JSON.

Protected information:
---
{protected_context}
---

AI-generated output:
---
{ai_output}
---

Return exactly this structure:

{{
    "relationship": "MATCH",
    "overlap_score": 0.0,
    "exposed_facts": [],
    "contradicted_facts": [],
    "explanation": ""
}}

Rules for overlap_score:

0.0 = no meaningful factual overlap
0.1-0.3 = very weak overlap
0.3-0.6 = partial overlap
0.6-0.8 = strong overlap
0.8-1.0 = very strong factual overlap

The overlap_score must be between 0.0 and 1.0.
"""


    response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)


    raw_output = response.text.strip()


    # --------------------------------------------------
    # Remove markdown JSON fences if the model adds them
    # --------------------------------------------------

    if raw_output.startswith("```json"):
        raw_output = raw_output[7:]

    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]

    raw_output = raw_output.strip()


    # --------------------------------------------------
    # Parse JSON
    # --------------------------------------------------

    try:

        result = json.loads(raw_output)

    except json.JSONDecodeError:

        return {
            "relationship": "NONE",
            "overlap_score": 0.0,
            "exposed_facts": [],
            "contradicted_facts": [],
            "explanation": (
                "The factual checker returned "
                "an invalid JSON response."
            ),
            "raw_response": raw_output
        }


    return result


# --------------------------------------------------
# Local testing
# --------------------------------------------------

if __name__ == "__main__":

    protected_information = """
    Employee ID: EMP001
    Name: Arjun Kumar
    Department: Finance
    Salary: 1240000 INR annually
    Manager: Priya Sharma
    Joining Date: 14 June 2023
    """


    test_outputs = [

        "Arjun earns approximately 12.4 lakh rupees per year.",

        "Arjun works in Finance but earns only 5 lakh rupees annually.",

        "Arjun works in the Finance department.",

        "The company cafeteria serves lunch from 12 PM to 2 PM."
    ]


    print("=" * 60)
    print("SENTINELVAULT - FACTUAL OVERLAP DETECTOR")
    print("=" * 60)


    for number, output in enumerate(
        test_outputs,
        start=1
    ):

        print("\n" + "=" * 60)
        print(f"TEST CASE {number}")
        print("=" * 60)

        print("\nAI Output:")
        print(output)


        result = check_factual_overlap(
            ai_output=output,
            protected_context=protected_information
        )


        print("\nLLM FACTUAL ANALYSIS")
        print("-" * 60)

        print(
            f"Relationship: "
            f"{result.get('relationship')}"
        )

        print(
            f"Overlap Score: "
            f"{result.get('overlap_score')}"
        )

        print(
            f"Exposed Facts: "
            f"{result.get('exposed_facts')}"
        )

        print(
            f"Contradicted Facts: "
            f"{result.get('contradicted_facts')}"
        )

        print(
            f"Explanation: "
            f"{result.get('explanation')}"
        )
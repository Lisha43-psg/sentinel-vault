// ================================================
// SENTINELVAULT - FRONTEND LOGIC
// ================================================


// ------------------------------------------------
// ELEMENTS
// ------------------------------------------------

const aiOutput = document.getElementById("aiOutput");
const analyzeButton = document.getElementById("analyzeButton");

const characterCount = document.getElementById("characterCount");

const loading = document.getElementById("loading");
const results = document.getElementById("results");

const errorBox = document.getElementById("error");
const errorMessage = document.getElementById("errorMessage");


// ------------------------------------------------
// CHARACTER COUNTER
// ------------------------------------------------

aiOutput.addEventListener("input", function () {

    const length = aiOutput.value.length;

    characterCount.textContent =
        `${length} characters`;

});


// ------------------------------------------------
// ANALYZE OUTPUT
// ------------------------------------------------

async function analyzeOutput() {

    const output = aiOutput.value.trim();


    // --------------------------------------------
    // VALIDATE INPUT
    // --------------------------------------------

    if (!output) {

        showError(
            "Please enter AI-generated output before analyzing."
        );

        return;
    }


    // --------------------------------------------
    // UI STATE
    // --------------------------------------------

    hideError();

    results.classList.add("hidden");

    loading.classList.remove("hidden");

    analyzeButton.disabled = true;

    analyzeButton.textContent =
        "Analyzing...";


    try {

        // ----------------------------------------
        // CALL FASTAPI BACKEND
        // ----------------------------------------

        const response = await fetch(
            "/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    ai_output: output
                })
            }
        );


        // ----------------------------------------
        // HANDLE HTTP ERRORS
        // ----------------------------------------

        if (!response.ok) {

            throw new Error(
                `Server returned HTTP ${response.status}`
            );
        }


        const data = await response.json();


        // ----------------------------------------
        // DISPLAY RESULTS
        // ----------------------------------------

        displayResults(data);

    }

    catch (error) {

        console.error(
            "SentinelVault analysis error:",
            error
        );

        showError(
            "Unable to analyze the output. " +
            "Please make sure the SentinelVault server is running."
        );

    }

    finally {

        loading.classList.add("hidden");

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "Analyze Output";

    }

}


// ------------------------------------------------
// DISPLAY RESULTS
// ------------------------------------------------

function displayResults(data) {

    results.classList.remove("hidden");


    // --------------------------------------------
    // SEMANTIC ANALYSIS
    // --------------------------------------------

    const semantic =
        data.semantic_analysis || {};

    const semanticScore =
        semantic.similarity_score || 0;

    document.getElementById(
        "semanticScore"
    ).textContent =
        `${(semanticScore * 100).toFixed(2)}%`;


    document.getElementById(
        "source"
    ).textContent =
        semantic.source || "None";


    document.getElementById(
        "matchedContent"
    ).textContent =
        semantic.matched_content ||
        "No protected information matched.";


    // --------------------------------------------
    // FACTUAL ANALYSIS
    // --------------------------------------------

    const factual =
        data.factual_analysis || {};

    document.getElementById(
        "factualRelationship"
    ).textContent =
        factual.relationship || "NONE";


    document.getElementById(
        "overlapScore"
    ).textContent =
        factual.overlap_score ?? 0;


    const exposedFacts =
        factual.exposed_facts || [];

    document.getElementById(
        "exposedFacts"
    ).textContent =
        exposedFacts.length
            ? exposedFacts.join(", ")
            : "None";


    const contradictedFacts =
        factual.contradicted_facts || [];

    document.getElementById(
        "contradictedFacts"
    ).textContent =
        contradictedFacts.length
            ? contradictedFacts.join(", ")
            : "None";


    // --------------------------------------------
    // RISK ANALYSIS
    // --------------------------------------------

    const risk =
        data.risk_analysis || {};


    const riskScore =
        risk.risk_score ?? 0;

    document.getElementById(
        "riskScore"
    ).textContent =
        Number(riskScore).toFixed(2);


    document.getElementById(
        "riskLevel"
    ).textContent =
        risk.risk_level || "LOW";


    // --------------------------------------------
    // DECISION
    // --------------------------------------------

    const decision =
        risk.decision || "ALLOW";

    const decisionBadge =
        document.getElementById(
            "decisionBadge"
        );

    decisionBadge.textContent =
        decision;


    // --------------------------------------------
    // DECISION STYLING
    // --------------------------------------------

    decisionBadge.style.background =
        getDecisionBackground(decision);

    decisionBadge.style.color =
        getDecisionColor(decision);


    // --------------------------------------------
    // REASONS
    // --------------------------------------------

    const reasons =
        risk.reasons || [];

    const reasonsList =
        document.getElementById("reasons");

    reasonsList.innerHTML = "";


    if (reasons.length === 0) {

        const li =
            document.createElement("li");

        li.textContent =
            "No additional security concerns detected.";

        reasonsList.appendChild(li);

    }

    else {

        reasons.forEach(reason => {

            const li =
                document.createElement("li");

            li.textContent =
                reason;

            reasonsList.appendChild(li);

        });

    }


    // --------------------------------------------
    // SCROLL TO RESULTS
    // --------------------------------------------

    results.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


// ------------------------------------------------
// DECISION COLORS
// ------------------------------------------------

function getDecisionBackground(decision) {

    if (decision === "BLOCK") {
        return "#fff0f0";
    }

    if (decision === "REVIEW") {
        return "#fff8e8";
    }

    return "#edf9f3";
}


function getDecisionColor(decision) {

    if (decision === "BLOCK") {
        return "#b42318";
    }

    if (decision === "REVIEW") {
        return "#a15c00";
    }

    return "#18794e";
}


// ------------------------------------------------
// ERROR HANDLING
// ------------------------------------------------

function showError(message) {

    errorMessage.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );

    loading.classList.add(
        "hidden"
    );

}


function hideError() {

    errorBox.classList.add(
        "hidden"
    );

}
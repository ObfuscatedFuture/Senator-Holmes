

function getScoreBand(score) {
    if (score < 40) {
        return {
            label: "High concern",
            detail: "This score falls in the lower range of the current dataset and signals a comparatively weak showing.",
            color: "#c84b4b"
        };
    }

    if (score < 70) {
        return {
            label: "Mixed record",
            detail: "This score sits in the middle band of the current dataset and suggests a more mixed profile.",
            color: "#c98b29"
        };
    }

    return {
        label: "Stronger score",
        detail: "This score lands in the upper range of the current dataset and compares favorably with most listed senators.",
        color: "#2f8a57"
    };
}

function animateScore(progressCircle, wheelCenter, finalScore, circumference) {
    const duration = 1200;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = 1 - Math.pow(1 - progress, 3);
        const currentScore = Math.round(finalScore * easedProgress);
        const offset = circumference - (currentScore / 100) * circumference;

        progressCircle.style.strokeDashoffset = offset;
        wheelCenter.textContent = currentScore;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function createBreakdownCard(label, value, description) {
    const card = document.createElement("article");
    card.className = "detail-card breakdown-card";

    const labelEl = document.createElement("span");
    labelEl.className = "detail-label";
    labelEl.textContent = label;

    const valueEl = document.createElement("strong");
    valueEl.className = "detail-value breakdown-value";
    valueEl.textContent = value;

    const descriptionEl = document.createElement("p");
    descriptionEl.className = "breakdown-description";
    descriptionEl.textContent = description;

    card.appendChild(labelEl);
    card.appendChild(valueEl);
    card.appendChild(descriptionEl);

    return card;
}

async function loadSenatorDetails() {
    const params = new URLSearchParams(window.location.search);
    const state = params.get("state");
    const senatorName = params.get("senator");

    const senatorTitle = document.getElementById("senatorTitle");
    const senatorSubtitle = document.getElementById("senatorSubtitle");
    const senatorState = document.getElementById("senatorState");
    const senatorBandDetail = document.getElementById("senatorBandDetail");
    const backToResultsLink = document.getElementById("backToResultsLink");
    const senatorHeadshot = document.getElementById("senatorHeadshot");
    const wheelProgress = document.getElementById("senatorWheelProgress");
    const wheelCenter = document.getElementById("senatorWheelCenter");
    const wheelLabel = document.getElementById("senatorWheelLabel");
    const breakdownGrid = document.getElementById("breakdownGrid");
    const methodologyCopy = document.getElementById("methodologyCopy");

    if (!state || !senatorName) {
        senatorTitle.textContent = "Senator not found";
        senatorSubtitle.textContent = "Return to the results page and select a senator name to view the score breakdown.";
        senatorState.textContent = "Unavailable";
        return;
    }

    backToResultsLink.href = `results.html?state=${encodeURIComponent(state)}`;

    try {
        const response = await fetch("data/senators.json");

        if (!response.ok) {
            throw new Error("Could not load senator data.");
        }

        const data = await response.json();
        const allSenators = data.flatMap((entry) =>
            entry.senators.map((senator) => ({
                state: entry.state,
                name: typeof senator === "string" ? senator : senator.name,
                score: typeof senator === "string" ? 0 : senator.score
            }))
        );

        const senator = allSenators.find((entry) => entry.state === state && entry.name === senatorName);

        if (!senator) {
            senatorTitle.textContent = "Senator not found";
            senatorSubtitle.textContent = "The requested senator could not be matched to the current dataset.";
            senatorState.textContent = state;
            return;
        }

        const sortedScores = [...allSenators].sort((a, b) => b.score - a.score);
        const rank = sortedScores.findIndex((entry) => entry.name === senator.name && entry.state === senator.state) + 1;
        const percentile = Math.round(((allSenators.length - rank) / Math.max(allSenators.length - 1, 1)) * 100);
        const scoreBand = getScoreBand(senator.score);
        const circumference = 2 * Math.PI * 85;

        senatorTitle.textContent = senator.name;
        senatorSubtitle.textContent = `Detailed score context for ${senator.name} of ${senator.state}.`;
        senatorState.textContent = senator.state;
        senatorBandDetail.textContent = scoreBand.detail;

        const testImg = new Image();
        testImg.onload = () => {
            senatorHeadshot.src = headshotSrc;
        };
        testImg.src = headshotSrc;

        wheelProgress.style.stroke = scoreBand.color;
        wheelProgress.style.strokeDasharray = String(circumference);
        wheelProgress.style.strokeDashoffset = String(circumference);
        wheelCenter.style.color = scoreBand.color;
        wheelLabel.style.color = scoreBand.color;

        breakdownGrid.innerHTML = "";
        breakdownGrid.appendChild(
            createBreakdownCard(
                "Raw score",
                `${senator.score}/100`,
                "The stored trust score currently assigned to this senator."
            )
        );
        breakdownGrid.appendChild(
            createBreakdownCard(
                "Score band",
                scoreBand.label,
                "A quick interpretation tier derived from the current score range."
            )
        );
        breakdownGrid.appendChild(
            createBreakdownCard(
                "Dataset rank",
                `#${rank} of ${allSenators.length}`,
                "This ranking compares the score against every currently listed senator in the dataset."
            )
        );
        breakdownGrid.appendChild(
            createBreakdownCard(
                "Relative position",
                `${percentile}th percentile`,
                "This percentile shows how high the score sits relative to the other listed entries."
            )
        );

        methodologyCopy.textContent = `This breakdown uses the current local dataset for context. The interpretation tier, rank, and percentile are derived from the stored score of ${senator.score} and may change as more senators or updated scores are added.`;

        animateScore(wheelProgress, wheelCenter, senator.score, circumference);
    } catch (error) {
        senatorTitle.textContent = "Error loading senator";
        senatorSubtitle.textContent = "The score breakdown could not be loaded.";
        senatorState.textContent = state;
        console.error(error);
    }
}

loadSenatorDetails();

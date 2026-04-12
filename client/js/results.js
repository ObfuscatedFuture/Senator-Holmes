function animateScore(progressCircle, wheelCenterValue, finalScore, circumference) {
    const duration = 1200;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = 1 - Math.pow(1 - progress, 3);
        const currentScore = Math.round(finalScore * easedProgress);
        const offset = circumference - (currentScore / 100) * circumference;

        progressCircle.style.strokeDashoffset = offset;
        wheelCenterValue.textContent = currentScore;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function getHeadshotSrc(senatorName) {
    const filename = senatorName
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/(^-|-$)/g, "");

    return `assets/senators/${filename}.jpg`;
}

function getScoreBand(score) {
    if (score < 40) {
        return {
            label: "High concern",
            detail: "This score falls in the lower range of the dataset.",
            color: "#c84b4b"
        };
    }

    if (score < 70) {
        return {
            label: "Mixed record",
            detail: "This score sits in the middle tier and may warrant closer review.",
            color: "#c98b29"
        };
    }

    return {
        label: "Stronger score",
        detail: "This score ranks in the upper portion of the currently listed entries.",
        color: "#2f8a57"
    };
}

function createDetailCard(label, value) {
    const detailCard = document.createElement("div");
    detailCard.className = "detail-card";

    const detailLabel = document.createElement("span");
    detailLabel.className = "detail-label";
    detailLabel.textContent = label;

    const detailValue = document.createElement("span");
    detailValue.className = "detail-value";
    detailValue.textContent = value;

    detailCard.appendChild(detailLabel);
    detailCard.appendChild(detailValue);

    return detailCard;
}

function buildSenatorDetailUrl(state, senatorName) {
    const params = new URLSearchParams({
        state,
        senator: senatorName
    });

    return `senator.html?${params.toString()}`;
}

function createScoreWheel(score, senatorName, state, delay = 0) {
    const radius = 50;
    const circumference = 2 * Math.PI * radius;
    const scoreBand = getScoreBand(score);

    const card = document.createElement("article");
    card.className = "senator-card";

    const nameBlock = document.createElement("div");
    nameBlock.className = "name-block";

    const headshotImg = document.createElement("img");
    headshotImg.src = "assets/placeholder-headshot.svg";
    headshotImg.alt = `${senatorName} headshot`;
    headshotImg.className = "senator-headshot";

    const headshotSrc = getHeadshotSrc(senatorName);
    const testImg = new Image();
    testImg.onload = () => {
        headshotImg.src = headshotSrc;
    };
    testImg.onerror = () => {
        // Keep placeholder if headshot asset is missing.
    };
    testImg.src = headshotSrc;

    const nameLink = document.createElement("a");
    nameLink.className = "senator-name senator-name-link";
    nameLink.href = buildSenatorDetailUrl(state, senatorName);
    nameLink.textContent = senatorName;

    nameBlock.appendChild(headshotImg);
    nameBlock.appendChild(nameLink);

    const scoreCopy = document.createElement("div");
    scoreCopy.className = "score-copy";

    const scoreMeta = document.createElement("div");
    scoreMeta.className = "score-meta";

    const metaText = document.createElement("div");

    const metaLabel = document.createElement("span");
    metaLabel.className = "meta-label";
    metaLabel.textContent = "Score overview";

    const scoreDescription = document.createElement("p");
    scoreDescription.className = "score-description";
    scoreDescription.textContent = scoreBand.detail;

    metaText.appendChild(metaLabel);
    metaText.appendChild(scoreDescription);


    const scoreLayout = document.createElement("div");
    scoreLayout.className = "score-layout";

    const wheelWrap = document.createElement("div");
    wheelWrap.className = "wheel-wrap";

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "score-wheel");
    svg.setAttribute("width", "132");
    svg.setAttribute("height", "132");
    svg.setAttribute("viewBox", "0 0 132 132");

    const bgCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    bgCircle.setAttribute("class", "wheel-bg");
    bgCircle.setAttribute("cx", "66");
    bgCircle.setAttribute("cy", "66");
    bgCircle.setAttribute("r", String(radius));

    const progressCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    progressCircle.setAttribute("class", "wheel-progress");
    progressCircle.setAttribute("cx", "66");
    progressCircle.setAttribute("cy", "66");
    progressCircle.setAttribute("r", String(radius));
    progressCircle.style.stroke = scoreBand.color;
    progressCircle.style.strokeDasharray = String(circumference);
    progressCircle.style.strokeDashoffset = String(circumference);

    svg.appendChild(bgCircle);
    svg.appendChild(progressCircle);

    const wheelCenter = document.createElement("div");
    wheelCenter.className = "wheel-center";

    const wheelCenterValue = document.createElement("span");
    wheelCenterValue.textContent = "0";

    const wheelCenterLabel = document.createElement("small");
    wheelCenterLabel.textContent = "Trust score";

    wheelCenter.appendChild(wheelCenterValue);
    wheelCenter.appendChild(wheelCenterLabel);

    wheelWrap.appendChild(svg);
    wheelWrap.appendChild(wheelCenter);

    const scoreDetails = document.createElement("div");
    scoreDetails.className = "score-details";
    scoreDetails.appendChild(createDetailCard("Rating band", scoreBand.label));
    scoreDetails.appendChild(createDetailCard("Raw score", `${score}/100`));

    scoreLayout.appendChild(wheelWrap);
    scoreLayout.appendChild(scoreDetails);

    scoreCopy.appendChild(scoreMeta);
    scoreCopy.appendChild(scoreLayout);

    card.appendChild(nameBlock);
    card.appendChild(scoreCopy);

    setTimeout(() => {
        animateScore(progressCircle, wheelCenterValue, score, circumference);
    }, delay);

    return card;
}

function renderEmptyState(resultBox, message) {
    resultBox.innerHTML = "";

    const emptyState = document.createElement("div");
    emptyState.className = "empty-state";
    emptyState.textContent = message;

    resultBox.appendChild(emptyState);
}

async function loadStateResults() {
    const params = new URLSearchParams(window.location.search);
    const state = params.get("state");

    const stateTitle = document.getElementById("stateTitle");
    const stateSubtitle = document.getElementById("stateSubtitle");
    const resultBox = document.getElementById("resultBox");

    if (!state) {
        stateTitle.textContent = "No state selected";
        stateSubtitle.textContent = "Return to the search page and choose a state to view its senator profiles.";
        renderEmptyState(resultBox, "Please go back and search for a state.");
        return;
    }

    stateTitle.textContent = `${state} Senators`;
    stateSubtitle.textContent = "Review currently available senator score cards and compare the listed results at a glance.";

    try {
        const response = await fetch(`/state/${state}`);

        if (!response.ok) {
            throw new Error("Could not load senator data.");
        }

        const data = await response.json();
        const match = data.find((entry) => entry.state === state);

        if (!match || !match.senators.length) {
            renderEmptyState(resultBox, `No senator data found for ${state}.`);
            return;
        }

        resultBox.innerHTML = "";

        const normalizedSenators = match.senators.map((senator) => ({
            name: typeof senator === "string" ? senator : senator.name,
            score: typeof senator === "string" ? 0 : senator.score
        }));

        normalizedSenators.forEach((senator, index) => {
            const wheelCard = createScoreWheel(senator.score, senator.name, state, index * 220);
            resultBox.appendChild(wheelCard);
        });
    } catch (error) {
        renderEmptyState(resultBox, "Error loading senator data.");
        console.error(error);
    }
}

loadStateResults();

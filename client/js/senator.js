function createOverviewCard(text) {
    const detailCard = document.createElement("div");
    detailCard.className = "detail-card";

    const detailLabel = document.createElement("span");
    detailLabel.className = "detail-label";
    detailLabel.textContent = "Score overview";

    const description = document.createElement("p");
    description.className = "score-description";
    description.textContent = text;

    detailCard.appendChild(detailLabel);
    detailCard.appendChild(description);

    return detailCard;
}

async function loadSenatorDetails() {
    const params = new URLSearchParams(window.location.search);
    const state = params.get("state");
    const senatorName = params.get("senator");
    const stateCode = STATE_CODES[state];

    const senatorTitle = document.getElementById("senatorTitle");
    const senatorSubtitle = document.getElementById("senatorSubtitle");
    const backToResultsLink = document.getElementById("backToResultsLink");
    const senatorCardHost = document.getElementById("senatorCardHost");

    if (!state || !senatorName || !stateCode) {
        senatorTitle.textContent = "Senator not found";
        senatorSubtitle.textContent = "Return to the results page and select a senator name to view the score breakdown.";
        return;
    }

    backToResultsLink.href = `results.html?state=${encodeURIComponent(state)}`;

    try {
        const response = await fetch(`${API_BASE}/senators/${senatorName}`);

        if (!response.ok) {
            throw new Error("Could not load senator data.");
        }

        const senator = await response.json();

        if (!senator) {
            senatorTitle.textContent = "Senator not found";
            senatorSubtitle.textContent = "The requested senator could not be matched to the current dataset.";
            return;
        }

        const scoreBand = getScoreBand(senator.score);
        const radius = 50;
        const circumference = 2 * Math.PI * radius;

        senatorTitle.textContent = senator.name;
        senatorSubtitle.textContent = `Detailed score context for ${senator.name} of ${senator.state}.`;
        senatorCardHost.innerHTML = "";

        const card = document.createElement("article");
        card.className = "senator-card";

        const nameBlock = document.createElement("div");
        nameBlock.className = "name-block";

        const headshotImg = document.createElement("img");
        headshotImg.src = senator["depiction"]?.["imageUrl"] || "assets/placeholder-headshot.svg";
        headshotImg.alt = `${senator.name} headshot`;
        headshotImg.className = "senator-headshot";

        const nameText = document.createElement("div");
        nameText.className = "senator-name";
        nameText.textContent = senator.name;

        nameBlock.appendChild(headshotImg);
        nameBlock.appendChild(nameText);

        const scoreCopy = document.createElement("div");
        scoreCopy.className = "score-copy";

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
        scoreDetails.className = "score-details is-single";
        scoreDetails.appendChild(createOverviewCard(scoreBand.detail));

        scoreLayout.appendChild(wheelWrap);
        scoreLayout.appendChild(scoreDetails);

        scoreCopy.appendChild(scoreLayout);

        card.appendChild(nameBlock);
        card.appendChild(scoreCopy);
        senatorCardHost.appendChild(card);

        animateScore(progressCircle, wheelCenterValue, senator.score, circumference);
    } catch (error) {
        senatorTitle.textContent = "Error loading senator";
        senatorSubtitle.textContent = "The score breakdown could not be loaded.";
        console.error(error);
    }
}

loadSenatorDetails();

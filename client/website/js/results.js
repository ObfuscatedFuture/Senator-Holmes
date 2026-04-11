function animateScore(progressCircle, wheelCenter, finalScore, circumference) {
    const duration = 1200;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // ease-out animation
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

function getHeadshotSrc(senatorName) {
    const filename = senatorName
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/(^-|-$)/g, "");
    return `assets/senators/${filename}.jpg`;
}

function createScoreWheel(score, senatorName, delay = 0) {
    const radius = 85;
    const circumference = 2 * Math.PI * radius;

    const card = document.createElement("div");
    card.className = "senator-card";

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "score-wheel");
    svg.setAttribute("width", "220");
    svg.setAttribute("height", "220");
    svg.setAttribute("viewBox", "0 0 220 220");

    // Background circle
    const bgCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    bgCircle.setAttribute("class", "wheel-bg");
    bgCircle.setAttribute("cx", "110");
    bgCircle.setAttribute("cy", "110");
    bgCircle.setAttribute("r", "85");

    // Progress circle
    const progressCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    progressCircle.setAttribute("class", "wheel-progress");
    progressCircle.setAttribute("cx", "110");
    progressCircle.setAttribute("cy", "110");
    progressCircle.setAttribute("r", "85");

    svg.appendChild(bgCircle);
    svg.appendChild(progressCircle);

    const nameBlock = document.createElement("div");
    nameBlock.className = "name-block";

    // Add headshot image; start with placeholder and swap in the real file only after it loads
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
        // keep placeholder if headshot asset is missing
    };
    testImg.src = headshotSrc;

    const nameDiv = document.createElement("div");
    nameDiv.className = "senator-name";
    nameDiv.textContent = senatorName;

    nameBlock.appendChild(headshotImg);
    nameBlock.appendChild(nameDiv);

    const wheelBlock = document.createElement("div");
    wheelBlock.className = "wheel-block";

    const wheelWrap = document.createElement("div");
    wheelWrap.className = "wheel-wrap";

    const wheelCenter = document.createElement("div");
    wheelCenter.className = "wheel-center";
    wheelCenter.textContent = "0";

    wheelWrap.appendChild(svg);
    wheelWrap.appendChild(wheelCenter);
    wheelBlock.appendChild(wheelWrap);

    // Start empty
    progressCircle.style.strokeDasharray = circumference;
    progressCircle.style.strokeDashoffset = circumference;

    // Set color based on score
    if (score < 40) {
        progressCircle.style.stroke = "#ef4444";
    } else if (score < 70) {
        progressCircle.style.stroke = "#f59e0b";
    } else {
        progressCircle.style.stroke = "#22c55e";
    }

    card.appendChild(nameBlock);
    card.appendChild(wheelBlock);

    // Animate after a delay so cards can appear one by one
    setTimeout(() => {
        animateScore(progressCircle, wheelCenter, score, circumference);
    }, delay);

    return card;
}

async function loadResults() {
    const params = new URLSearchParams(window.location.search);
    const state = params.get("state");

    const stateTitle = document.getElementById("stateTitle");
    const resultBox = document.getElementById("resultBox");

    if (!state) {
        stateTitle.textContent = "No state selected";
        resultBox.textContent = "Please go back and search for a state.";
        return;
    }

    stateTitle.textContent = `Senators from ${state}`;

    try {
        const response = await fetch("data/senators.json");

        if (!response.ok) {
            throw new Error("Could not load senator data.");
        }

        const data = await response.json();
        const match = data.find(entry => entry.state === state);

        if (!match) {
            resultBox.textContent = `No senator data found for ${state}.`;
            return;
        }

        resultBox.innerHTML = "";

        match.senators.forEach((senator, index) => {
            const senatorName = typeof senator === "string" ? senator : senator.name;
            const senatorScore = typeof senator === "string" ? 0 : senator.score;

            const wheelCard = createScoreWheel(senatorScore, senatorName, index * 250);
            resultBox.appendChild(wheelCard);
        });

    } catch (error) {
        resultBox.textContent = "Error loading senator data.";
        console.error(error);
    }
}

loadResults();
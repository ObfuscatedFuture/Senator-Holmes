const STATE_CODES = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
};

function getScoreBand(score) {
    if (score < 40) {
        return {
            label: "High concern",
            detail: "This score falls in the lower range of the current dataset.",
            color: "#c84b4b"
        };
    }

    if (score < 70) {
        return {
            label: "Mixed record",
            detail: "This score sits in the middle tier of the current dataset.",
            color: "#c98b29"
        };
    }

    return {
        label: "Stronger score",
        detail: "This score ranks in the upper portion of the current dataset.",
        color: "#2f8a57"
    };
}

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

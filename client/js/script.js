import API_BASE from "./config.js";

const validStates = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
];

async function searchState() {
    const state = document.getElementById("stateInput").value.trim();

    if (!validStates.includes(state)) {
        alert("Please enter a valid U.S. state.");
        return;
    }
    try {
        const response = await fetch(`${API_BASE}/state/${encodeURIComponent(state)}`);
        if (!response.ok) {
            throw new Error("API request failed");
        }
        const data = await response.json();

        console.log(data);

        // Example: display result on page
        document.getElementById("output").textContent = JSON.stringify(data, null, 2);

    } catch (error) {
        console.error(error);
        alert("Error calling API");
    }
}

document.getElementById("searchButton").addEventListener("click", searchState);

document.getElementById("stateInput").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        searchState();
    }
});

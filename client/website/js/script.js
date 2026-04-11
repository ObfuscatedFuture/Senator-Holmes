function searchState(){
    const state = document.getElementById("stateInput").value;
    alert("You searched for: " + state);
}

const validStates = [
    "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
    "Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa",
    "Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan",
    "Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
    "New Hampshire","New Jersey","New Mexico","New York","North Carolina",
    "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
    "South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont",
    "Virginia","Washington","West Virginia","Wisconsin","Wyoming"
];

document.getElementById("searchButton").addEventListener("click", searchState);

function searchState() {
    const state = document.getElementById("stateInput").value.trim();

    if (!validStates.includes(state)) {
        alert("Please enter a valid U.S. state.");
        return;
    }

    window.location.href = `results.html?state=${encodeURIComponent(state)}`;
}
const API_URL = "http://127.0.0.1:5000";

async function fetchTransactions() {
    const response = await fetch(`${API_URL}/transactions`);
    const transactions = await response.json();
    displayTransactions(transactions);
}

async function addTransaction() {
    const amount = document.getElementById("amount").value;
    const description = document.getElementById("description").value;
    const type = document.getElementById("type").value;

    await fetch(`${API_URL}/transactions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount, description, type }),
    });

    fetchTransactions();
}

function displayTransactions(transactions) {
    const transactionsDiv = document.getElementById("transactions");
    transactionsDiv.innerHTML = transactions
        .map(
            (t) =>
                `<p>${t.type.toUpperCase()}: $${t.amount} - ${t.description}</p>`
        )
        .join("");
}

// Initial load
fetchTransactions();

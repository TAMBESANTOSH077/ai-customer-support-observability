const API_URL = "http://127.0.0.1:8000";


async function askSupport() {

    const question =
        document.getElementById("question").value.trim();

    const result =
        document.getElementById("result");

    if (!question) {
        result.innerHTML = "Please enter a question.";
        return;
    }

    result.innerHTML = "Processing...";

    try {

        const response = await fetch(
            `/support?question=${encodeURIComponent(question)}`
        );

        const data = await response.json();

        result.innerHTML = `
            <h3>Response</h3>
            <p>${data.answer || data.error}</p>

            <p>
                <b>Request ID:</b>
                ${data.request_id || "N/A"}
            </p>

            <p>
                <b>Status:</b>
                ${response.status}
            </p>

            <p>
                <b>Processing Time:</b>
                ${response.headers.get("X-Process-Time") || "N/A"}
            </p>
        `;

    } catch (error) {

        result.innerHTML =
            `Backend error: ${error.message}`;
    }
}


async function checkHealth() {

    const result =
        document.getElementById("result");

    try {

        const response =
            await fetch("/health");

        const data =
            await response.json();

        result.innerHTML = `
            <h3>System Health</h3>

            <p>
                Status: <b>${data.status}</b>
            </p>

            <p>
                Service: ${data.service}
            </p>

            <p>
                Request ID: ${data.request_id}
            </p>
        `;

    } catch (error) {

        result.innerHTML =
            `Backend unavailable: ${error.message}`;
    }
}
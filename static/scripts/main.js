document.addEventListener("DOMContentLoaded", function () {
    const outputDiv = document.getElementById("output");
    const analysisDiv = document.getElementById("results-analysis");
    const tickerSpan = document.getElementById("result-ticker"); // Ensure ID is correct
    const adviceSpan = document.getElementById("output-advice");
    const ratiosList = document.getElementById("fundamental-ratios");
    const errorDiv = document.getElementById("error-message");

    // Ensure form submission is handled correctly
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const loadingSpinner = document.getElementById("loading-spinner");
            if (loadingSpinner) loadingSpinner.style.display = "block";

            const resultsContainer = document.getElementById("results-container");
            if (resultsContainer) resultsContainer.style.display = "none";

            const errorMessage = document.getElementById("error-message");
            if (errorMessage) errorMessage.style.display = "none";

            const formData = new FormData(form);
            const requestData = Object.fromEntries(formData.entries());

            console.log("Form submitted:", requestData);

            try {
                const response = await fetch("/perform_analysis", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(requestData),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || "Unknown error occurred");
                }

                const data = await response.json();
                console.log("Analysis Data:", data);

                if (loadingSpinner) loadingSpinner.style.display = "none";

                if (data.status === "success" && data.data) {
                    updateUI(data.data);
                    if (resultsContainer) resultsContainer.style.display = "block";
                } else {
                    throw new Error(data.message || "Invalid response data");
                }
            } catch (error) {
                if (loadingSpinner) loadingSpinner.style.display = "none";
                showError(error.message);
            }
        });
    });

    function updateUI(responseData) {
        console.log("Updating UI with stock data:", responseData);
    
        if (!responseData.data) {
            console.error("Error: No valid stock data found.");
            showError("Invalid response structure.");
            return;
        }
    
        const stockData = responseData.data; // Extract actual stock data
    
        // Ensure elements exist before updating
        const resultTicker = document.getElementById("result-ticker");
        if (resultTicker) {
            resultTicker.textContent = stockData.ticker || "N/A";
        } else {
            console.warn("⚠️ Warning: Missing element #result-ticker in HTML.");
        }
    
        const resultAdvice = document.getElementById("output-advice");
        if (resultAdvice) {
            resultAdvice.textContent = stockData.advice || "N/A";
        }
    
        if (!outputDiv) {
            console.error(" Error: Missing #output container in HTML!");
            return;
        }
    
        //  Render fundamental ratios dynamically
        const fundamentalRatios = stockData.fundamental_ratios || {};
        const ratiosHtml = Object.entries(fundamentalRatios)
            .map(([key, value]) => `<li><strong>${key}:</strong> ${value}</li>`)
            .join("");
    
        outputDiv.innerHTML = `
            <h2>Stock Analysis for ${stockData.ticker || "N/A"}</h2>
            <p><strong>Advice:</strong> ${stockData.advice || "N/A"}</p>
            <h3>Fundamental Ratios:</h3>
            <ul>${ratiosHtml}</ul>
        `;
    
        outputDiv.style.display = "block"; // Show the results
    }    

    function showError(message) {
        if (errorDiv) {
            errorDiv.textContent = `Error: ${message}`;
            errorDiv.style.color = "red";
            errorDiv.style.display = "block";
        }
        console.error(message);
    }
});
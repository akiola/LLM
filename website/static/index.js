// Recipe Generator JavaScript

async function getRecipes() {
    let selectedIngredients = [];
    document.querySelectorAll("input[name='ingredients']:checked").forEach(checkbox => {
        selectedIngredients.push(checkbox.value);
    });

    if (selectedIngredients.length === 0) {
        alert("Please select at least one ingredient!");
        return;
    }

    // Show loading indicator
    document.getElementById("recipeResults").innerHTML = '<div class="col-12 text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';

    // Fetch recipes from Flask backend
    const response = await fetch("/generate-recipe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: selectedIngredients.join(", ") })
    });

    const data = await response.json();

    let resultContainer = document.getElementById("recipeResults");
    resultContainer.innerHTML = ""; // Clear previous results

    if (data.recipes && data.images) {
        for (let i = 0; i < data.recipes.length; i++) {
            let recipeHtml = `
                <div class="col-md-4">
                    <div class="card mb-4">
                        ${data.images[i] ? `<img src="${data.images[i]}" class="card-img-top" alt="Recipe Image">` : ''}
                        <div class="card-body">
                            <h5 class="card-title">${data.recipes[i].split('\n')[0] || 'Recipe ' + (i + 1)}</h5>
                            <p class="card-text">${data.recipes[i].replace(/\n/g, "<br>")}</p>
                        </div>
                    </div>
                </div>
            `;
            resultContainer.innerHTML += recipeHtml;
        }
    } else {
        resultContainer.innerHTML = "<p class='text-danger'>Error generating recipes.</p>";
    }
}

// Initialize any event listeners or other setup when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // If you have any initialization code, put it here
    console.log('Recipe Generator initialized');
});
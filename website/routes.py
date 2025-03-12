from flask import render_template, request, jsonify
import os
from openai import OpenAI
from flask import Blueprint, render_template, request
from dotenv import load_dotenv

load_dotenv()

main = Blueprint("main", __name__)

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

def generate_recipe(ingredients):
    """
    Generates a recipe based on provided ingredients
    
    Args:
        ingredients (str): Comma-separated list of ingredients
    
    Returns:
        str: The generated recipe
    """
    try:
        prompt = f"""Generate a detailed recipe using these ingredients: {ingredients}.
        
The recipe should include:
1. A creative name for the dish
2. List of all ingredients with measurements
3. Step-by-step cooking instructions
4. Approximate cooking time
5. Serving size
6. A brief description of the flavor profile
        
Only use the ingredients provided or very basic pantry staples (salt, pepper, oil, etc.)."""

        # Make the API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-4",  # You can change this to a different model as needed
            messages=[
                {"role": "system", "content": "You are a professional chef who specializes in creating delicious recipes with limited ingredients."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Return the generated recipe
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error generating recipe: {e}")
        return f"Error generating recipe: {str(e)}"

def generate_image_for_recipe(recipe_name):
    """
    Generates an image for the recipe using DALL-E
    
    Args:
        recipe_name (str): Name of the recipe
    
    Returns:
        str: URL of the generated image
    """
    try:
        # Extract the recipe name from the full recipe text
        # Assuming the name is the first line of the recipe
        recipe_title = recipe_name.split('\n')[0] if '\n' in recipe_name else recipe_name

        response = client.images.generate(
            model="dall-e-3",
            prompt=f"A professional food photography image of {recipe_title}. Top-down view, on a wooden table, natural lighting.",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate-recipe', methods=['POST'])
def recipe_generator():
    data = request.json
    ingredients = data.get('ingredients', '')
    
    if not ingredients:
        return jsonify({'error': 'No ingredients provided'}), 400
    
    try:
        # Generate multiple recipes
        num_recipes = 3
        recipes = []
        images = []
        
        for _ in range(num_recipes):
            recipe_text = generate_recipe(ingredients)
            recipes.append(recipe_text)
            
            # Generate image for the recipe
            image_url = generate_image_for_recipe(recipe_text)
            images.append(image_url)
        
        return jsonify({
            'recipes': recipes,
            'images': images
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import streamlit as st
import google.generativeai as genai
import json

def generate_recipe(cuisine_type, dietary_restrictions, time_available, skill_level, ingredients):
    """Generates a recipe based on given parameters.

    Args:
        cuisine_type: The type of cuisine.
        dietary_restrictions: List of dietary restrictions.
        time_available: The amount of time available for cooking.
        skill_level: The cooking skill level.
        ingredients: The ingredients available.

    Returns:
        A string containing the full recipe, or None if an error occurs.
    """
    try:
        # Configure API key
        genai.configure(api_key="AIzaSyD9UClG8tAdgNjWiGSyecdnjClSVerdskg")

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an expert chef. Create delicious recipes tailored to the user's needs, including cuisine type, dietary restrictions, time available, skill level, and available ingredients. Use only the given ingredients.",
        )

        # Construct the prompt
        prompt = (f"Create a {cuisine_type} recipe for a {skill_level} cook that meets the following dietary restrictions: {', '.join(dietary_restrictions)}. "
                  f"The recipe should take no more than {time_available} minutes to prepare and use only the following ingredients: {ingredients}. "
                  "Include a clear list of ingredients with quantities, detailed instructions, and the estimated cooking time.")

        # Generate the recipe
        response = model.generate_content(prompt)
        recipe_text = response.text

        return recipe_text

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="AI-Powered Recipe Generator", page_icon=":shallow_pan_of_food:")

st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput > div > div > input {
        background-color: #f1f1f1;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-size: 16px;
    }
    .stSelectbox, .stSlider, .stMultiSelect {
        margin-bottom: 20px;
    }
    .recipe-title {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
    }
    .recipe-section {
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        color: #2C3E50;
    }
    .recipe-item {
        font-size: 16px;
        color: #34495E;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("AI-Powered Recipe Generator :shallow_pan_of_food:")
st.write("Enter the details to get a tailored recipe.")

col1, col2 = st.columns(2)

with col1:
    cuisine_type = st.selectbox("Cuisine Type", ["Italian", "Chinese", "Mexican", "Indian", "American"])
    skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Expert"])

with col2:
    dietary_restrictions = st.multiselect("Dietary Restrictions", ["Gluten-Free", "Vegan", "Keto", "Vegetarian", "Dairy-Free"])
    time_available = st.slider("Time Available (minutes)", 15, 120, 30)

ingredients = st.text_area("Enter available ingredients, separated by commas:")

if st.button("Generate Recipe"):
    recipe_text = generate_recipe(cuisine_type, dietary_restrictions, time_available, skill_level, ingredients)

    if recipe_text:
        st.header("Generated Recipe")
        st.text_area("", recipe_text, height=500)
    else:
        st.error("Failed to generate recipe.")
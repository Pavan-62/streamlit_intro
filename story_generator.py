import streamlit as st
import google.generativeai as genai
import time

def generate_story(hints, genre, length):
    """Generates a story based on given hints.

    Args:
        hints: The hints or prompts for the story.
        genre: The genre of the story.
        length: The desired length of the story.

    Returns:
        A string containing the generated story, or an error message if an error occurs.
    """
    try:
        # Configure API key
        genai.configure(api_key="AIzaSyCTrlIOwORw1kjrO3EB_hDCIutx5yEcp4Y")

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
            system_instruction="You are a creative writer. Generate engaging and imaginative stories based on the user's hints, genre, and desired length.",
        )

        # Construct the prompt
        prompt = (f"Write a {length} story in the {genre} genre using the following hints: {hints}. "
                  "Ensure the story is coherent and engaging.")

        # Generate the story
        response = model.generate_content(prompt)

        # Extract the generated text
        if response and hasattr(response, 'text') and response.text:
            story_text = response.text
            return story_text
        else:
            st.warning("The model did not generate any content.")
            return None

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="AI-Powered Story Generator", page_icon=":books:")

st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput > div > div > input, .stTextArea textarea {
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
    .story-title {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
    }
    .story-section {
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        color: #2C3E50;
    }
    .story-item {
        font-size: 16px;
        color: #34495E;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("AI-Powered Story Generator :books:")
st.write("Enter the details to get a tailored story.")

col1, col2 = st.columns(2)

with col1:
    genre = st.selectbox("Genre", ["Fantasy", "Science Fiction", "Mystery", "Romance", "Horror"])
    length = st.selectbox("Length", ["Short Story", "Medium Story", "Long Story"])

with col2:
    hints = st.text_area("Enter story hints, separated by hyphens (e.g., hint1 - hint2 - hint3):")

if st.button("Generate Story"):
    with st.spinner("Generating story..."):
        story_text = generate_story(hints, genre, length)
        time.sleep(2)  # Adding buffer time

    if story_text:
        st.header("Generated Story")
        st.text_area("", story_text, height=500)
    else:
        st.error("Failed to generate story.")

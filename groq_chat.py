
# Import necessary libraries
from groq import Groq
import streamlit as st

# Configure Groq API here
client = Groq(
    api_key="Enter_GroqAPI"
)


# -------------------- Functions to interact with Groq API ----------------------
# This function sends a prompt to the Groq model and retrieves the model's response.
def send_prompt_to_groq(prompt_text):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.5,  # To control randomness
        max_tokens=1000  # Max length of the response
    )
    return response.choices[0].message.content.strip()


# This function checks and improves grammar for a user's input text.
def check_grammar(text_to_check):
    prompt_text = f"Please check the following text for grammar mistakes and suggest improvements:\n\n{text_to_check}"
    return send_prompt_to_groq(prompt_text)


# This function will generate 5 writing ideas for user's input academic topic
def create_topic_ideas(main_topic):
    prompt_text = f"Give me 5 academic writing ideas related to the topic: {main_topic}"
    ideas_string = send_prompt_to_groq(prompt_text)

    # Process the response to remove numbering or bullets
    ideas_list = [write_idea.strip("-•1234567890. ") for write_idea in ideas_string.split('\n') if write_idea.strip()]
    return ideas_list


# This function gives a short answer responding to user's research related question
def research_question_answer(research_question):
    prompt_text = f"Answer this research question in a short and clear way, as if explaining to a student:\n\n{research_question}"
    return send_prompt_to_groq(prompt_text)


# This function generates APA or MLA style citation based on user's input
def create_citation(reference_info):
    prompt_text = f"Generate a proper citation for this reference in APA format:\n\n{reference_info}"
    return send_prompt_to_groq(prompt_text)


# ----------------------- Streamlit app UI setup -------------------------

# Title
st.title("📚 Writing Helper Bot")

# Dropdown menu for users to choose what they want to do
app_choice = st.selectbox(
    "Choose an option:",
    ("Grammar Check", "Generate Topic Ideas", "Answer Research Question", "Citation Generator")
)

# Based on the user's choice, show the relevant input fields and buttons
# When user selects Grammar Check
if app_choice == "Grammar Check":
    st_text = st.text_area("Enter the text you want to check:")
    if st.button("Check Grammar"):
        if st_text.strip():
            grammar_result = check_grammar(st_text)
            st.success(grammar_result)
        else:
            st.warning("Please enter some text.")

        # When user selects Generate Topic Ideas
elif app_choice == "Generate Topic Ideas":

    st_topic = st.text_input("Enter the main topic:")
    if st.button("Get Writing Ideas"):
        if st_topic.strip():
            topic_ideas = create_topic_ideas(st_topic)
            st.subheader("Ideas:")
            for write_idea in topic_ideas:
                st.write(f"- {write_idea}")
        else:
            st.warning("Please enter a topic.")

            # When user selects Answer Research Question
elif app_choice == "Answer Research Question":

    st_question = st.text_input("Enter your research question:")
    if st.button("Get Answer"):
        if st_question.strip():
            research_answer = research_question_answer(st_question)
            st.subheader("Answer:")
            st.write(research_answer)
        else:
            st.warning("Please enter a research question.")

        # If user selects Citation Generator
elif app_choice == "Citation Generator":

    st_reference = st.text_input("Enter reference details (title, author, year, etc.):")
    if st.button("Generate Citation"):
        if st_reference.strip():
            citation_result = create_citation(st_reference)
            st.subheader("Citation:")
            st.write(citation_result)
        else:
            st.warning("Please enter reference details.")

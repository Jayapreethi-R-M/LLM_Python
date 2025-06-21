
import streamlit as st
from groq import Groq

# Configure Groq API here
client = Groq(
    api_key="Enter_API_key_here"
)


# ------------------- Groq_chatbot functions -------------------
def send_prompt_to_groq(prompt_text):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt_text}],
        temperature=0.5,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()


def check_grammar(text):
    return send_prompt_to_groq(
        f"Please check the following text for grammar mistakes and suggest improvements:\n\n{text}"
    )


def create_topic_ideas(main_topic):
    prompt = f"Give me 5 academic writing ideas related to the topic: {main_topic}"
    ideas_string = send_prompt_to_groq(prompt)
    return [idea.strip("-•1234567890. ") for idea in ideas_string.split('\n') if idea.strip()]


def research_question_answer(question):
    return send_prompt_to_groq(
        f"Answer this research question in a short and clear way, as if explaining to a student:\n\n{question}"
    )


def create_citation(reference_info, style):
    style_prompt = "APA" if style == "APA" else "MLA"
    return send_prompt_to_groq(
        f"Generate a proper citation for this reference in {style_prompt} format:\n\n{reference_info}"
    )


# ------------------- Streamlit App UI -------------------
st.set_page_config(page_title="Writing Helper Bot", layout="centered")
st.title("\U0001F4DA Writing Helper Bot")

with st.expander("ℹ️ About Writing Helper Bot"):
    st.markdown("""
    Academic Writing Helper Bot** is an AI-powered assistant for academic writing, built using LLMs via the Groq API.

    It helps you:
    - ✅ Fix grammar issues
    - 🧠 Brainstorm & Generate academic research topic ideas
    - ❓ Get clear and concise information about specific concepts
    - 🧾 Format citations in APA or MLA style

    📌 Useful for students, researchers, and academic writers.
    """)

app_choice = st.selectbox("Choose an option:",
                          ("Grammar Check", "Generate Topic Ideas", "Answer Research Question", "Citation Generator"))

if app_choice == "Grammar Check":
    st_text = st.text_area("Enter the text you want to check:", placeholder="Paste your paragraph here...")
    if st.button("Check Grammar"):
        if st_text.strip():
            st.success(check_grammar(st_text))
        else:
            st.warning("Please enter some text.")

elif app_choice == "Generate Topic Ideas":
    st_topic = st.text_input("Enter the main topic:", placeholder="Enter the key words/ briefly describe it...")
    if st.button("Get Writing Ideas"):
        if st_topic.strip():
            ideas = create_topic_ideas(st_topic)
            st.markdown("### Writing Ideas:")
            for idea in ideas:
                st.markdown(f"- {idea}")
        else:
            st.warning("Please enter a topic.")

elif app_choice == "Answer Research Question":
    st_question = st.text_input("Enter your research question:", placeholder="Enter a concept that you would like to learn about...")
    if st.button("Get Answer"):
        if st_question.strip():
            answer = research_question_answer(st_question)
            st.subheader("Generated Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a research question.")

elif app_choice == "Citation Generator":
    st_reference = st.text_input("Enter reference details:", placeholder="like Author, Title, Year, DOI/URL")
    style = st.radio("Choose citation style:", ["APA", "MLA"])
    if st.button("Generate Citation"):
        if st_reference.strip():
            citation_result = create_citation(st_reference, style)
            st.subheader(f"{style} Citation:")
            st.write(citation_result)
        else:
            st.warning("Please enter reference details.")

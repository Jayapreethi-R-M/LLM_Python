__author__ = 'Jayapreethi Radhakrishnan Madanraj, jayam@ad.unc.edu, Onyen = jayam'

# ------------------- Imports -------------------
from groq import Groq
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from rouge_score import rouge_scorer

# ------------------- Config -------------------
client = Groq(api_key="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")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ------------------- Evaluation Functions -------------------
def context_similarity(main_topic, generated_ideas, reference_ideas=None):
    main_emb = embedding_model.encode(main_topic, convert_to_tensor=True)
    gen_embs = embedding_model.encode(generated_ideas, convert_to_tensor=True)
    if reference_ideas:
        ref_embs = embedding_model.encode(reference_ideas, convert_to_tensor=True)
        sim_matrix = util.cos_sim(gen_embs, ref_embs)
        max_sims = sim_matrix.max(dim=1).values
        return max_sims.mean().item()
    else:
        sims = util.cos_sim(gen_embs, main_emb)
        return sims.mean().item()


def rouge_evaluation(reference, generated):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)['rougeL']
    return {
        "ROUGE-L Precision": round(scores.precision, 3),
        "ROUGE-L Recall": round(scores.recall, 3),
        "ROUGE-L F1": round(scores.fmeasure, 3)
    }


def semantic_similarity(text1, text2):
    emb1 = embedding_model.encode(text1, convert_to_tensor=True)
    emb2 = embedding_model.encode(text2, convert_to_tensor=True)
    return round(util.cos_sim(emb1, emb2).item(), 3)


def evaluate_research_answer(reference_answer, generated_answer):
    return {
        "ROUGE Scores": rouge_evaluation(reference_answer, generated_answer),
        "Semantic Similarity": semantic_similarity(reference_answer, generated_answer)
    }


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
        f"Please check the following text for grammar mistakes and suggest improvements:\n\n{text}")


def create_topic_ideas(main_topic, reference_ideas=None):
    prompt = f"Give me 5 academic writing ideas related to the topic: {main_topic}"
    ideas_string = send_prompt_to_groq(prompt)
    ideas_list = [idea.strip("-•1234567890. ") for idea in ideas_string.split('\n') if idea.strip()]
    similarity_score = context_similarity(main_topic, ideas_list, reference_ideas)
    return ideas_list, similarity_score


def research_question_answer(question):
    return send_prompt_to_groq(
        f"Answer this research question in a short and clear way, as if explaining to a student:\n\n{question}")


def create_citation(reference_info, style):
    style_prompt = "APA" if style == "APA" else "MLA"
    return send_prompt_to_groq(
        f"Generate a proper citation for this reference in {style_prompt} format:\n\n{reference_info}")


# ------------------- Streamlit App UI -------------------
st.title("\U0001F4DA Academic Writing Helper Bot")

with st.expander("ℹ️ About Academic Writing Helper Bot"):
    st.markdown("""
    **Academic Writing Helper Bot** is an AI-powered assistant for academic writing, built using LLMs via the Groq API.

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
            ideas, sim_score = create_topic_ideas(st_topic)
            st.markdown("### Writing Ideas:")
            for idea in ideas:
                st.markdown(f"- {idea}")
            st.info(f"Context Similarity Score: {sim_score:.3f}")
        else:
            st.warning("Please enter your topic.")

elif app_choice == "Answer Research Question":
    st_question = st.text_input("Enter your research question:", placeholder="Enter a concept that you would like to learn about...")
    st_reference = st.text_area("(Optional) Reference answer for this model evaluation:",
                                placeholder="Paste the ideal answer to compare and evaluate this language model")
    if st.button("Get Answer"):
        if st_question.strip():
            answer = research_question_answer(st_question)
            st.subheader("Generated Answer:")
            st.write(answer)
            if st_reference.strip():
                scores = evaluate_research_answer(st_reference, answer)
                st.subheader("Evaluation Scores:")
                st.json(scores)
            else:
                st.info("Provide a reference answer above to evaluate accuracy.")
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


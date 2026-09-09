# app.py

import streamlit as st
import workflow

st.set_page_config(
    page_title="AI Study Pack Generator",
    page_icon="📚",
    layout="wide"
)

st.title("⚡ Multi-Stage AI Study Pack Generator")
st.caption("Structured AI Workflow: Planning ➔ Generation ➔ Assessment ➔ QA & Refinement")

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")
    
    api_key_default = st.secrets.get("GROQ_API_KEY", "") if "GROQ_API_KEY" in st.secrets else ""
    api_key = st.text_input("Groq API Key", value=api_key_default, type="password")
    
    st.markdown("---")
    st.header("Pipeline Progress")
    s1_slot = st.empty()
    s2_slot = st.empty()
    s3_slot = st.empty()
    s4_slot = st.empty()

# Inputs
notes_input = st.text_area("Paste your source notes or study material here:", height=220)
level_input = st.selectbox(
    "Select Target Academic Level:",
    ["Beginner / Primary", "Intermediate / High School", "Advanced / University"]
)

# Pipeline Execution
if st.button("Generate Study Pack", type="primary"):
    if not api_key:
        st.error("Please enter a valid Groq API Key in the sidebar.")
    elif not notes_input.strip():
        st.warning("Please paste study notes or text to process.")
    else:
        status_callbacks = {
            "stage1": lambda msg: s1_slot.info(msg),
            "stage2": lambda msg: s2_slot.info(msg),
            "stage3": lambda msg: s3_slot.info(msg),
            "stage4": lambda msg: s4_slot.info(msg)
        }

        try:
            client = workflow.get_client(api_key)
            
            with st.spinner("Executing Groq pipeline stages..."):
                results = workflow.run_study_pack_pipeline(client, notes_input, level_input, status_callbacks)
            
            s1_slot.success("✅ Stage 1: Blueprint Created")
            s2_slot.success("✅ Stage 2: Content Drafted")
            s3_slot.success("✅ Stage 3: Assessment Ready")
            s4_slot.success("✅ Stage 4: QA Completed")

            st.session_state["study_pack_data"] = results

        except Exception as e:
            st.error(f"Error during workflow execution: {e}")

# Render Output Tabs
if "study_pack_data" in st.session_state:
    data = st.session_state["study_pack_data"]
    
    st.markdown("---")
    tab_summary, tab_flashcards, tab_quiz = st.tabs(["📝 Summary", "🎴 Flashcards", "🧪 Practice Quiz"])

    with tab_summary:
        st.markdown(data.get("summary", "No summary content generated."))

    with tab_flashcards:
        flashcards = data.get("flashcards", [])
        if not flashcards:
            st.info("No flashcards generated.")
        else:
            for idx, card in enumerate(flashcards, 1):
                with st.expander(f"Flashcard {idx}: {card['question']}"):
                    st.markdown(f"**Answer:** {card['answer']}")

    with tab_quiz:
        quiz = data.get("quiz", [])
        if not quiz:
            st.info("No quiz items available.")
        else:
            for idx, q in enumerate(quiz, 1):
                st.subheader(f"Question {idx}: {q['question']}")
                selected_option = st.radio(
                    "Select an answer:",
                    q["options"],
                    key=f"quiz_opt_{idx}"
                )
                
                if st.button(f"Submit Answer Q{idx}", key=f"btn_quiz_{idx}"):
                    if selected_option == q["correct_answer"]:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. The correct answer is: {q['correct_answer']}")
                    st.info(f"**Explanation:** {q['explanation']}")
                st.write("---")

    # Download Button
    export_md = f"# AI GENERATED STUDY PACK\n\n## 📝 Summary\n{data.get('summary', '')}\n\n## 🎴 Flashcards\n"
    for fc in data.get("flashcards", []):
        export_md += f"- **Q:** {fc['question']}\n  **A:** {fc['answer']}\n"

    st.download_button(
        label="Download Full Study Pack (.md)",
        data=export_md,
        file_name="study_pack.md",
        mime="text/markdown"
    )

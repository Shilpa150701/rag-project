"""
Streamlit app
"""
import streamlit as st
import json
import ollama
import re

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Salary Assistant",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# LOAD SALARY DATA
# -----------------------------------

try:
    with open("salary_data.json", "r", encoding="utf-8") as f:
        salary_data = json.load(f)

    data_loaded = True

except Exception as e:
    data_loaded = False
    salary_data = {}
    st.error(f"Error loading salary_data.json: {e}")

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("⚙️ Settings")

    model_name = st.selectbox(
        "Select Model",
        [
            "deepseek-r1:7b",
            "qwen3:8b",
            "qwen2.5:7b",
            "qwen2.5:1.5b"
        ]
    )

    st.divider()

    if data_loaded:

        if isinstance(salary_data, list):
            st.success(
                f"Loaded {len(salary_data)} records"
            )
        else:
            st.success("Salary data loaded")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []
        st.rerun()

# -----------------------------------
# TITLE
# -----------------------------------

st.title("💰 Salary Assistant")

st.caption(
    "Ask any question about payroll, salary, deductions, allowances, totals, averages, and comparisons."
)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------
# DISPLAY PREVIOUS MESSAGES
# -----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -----------------------------------
# USER INPUT
# -----------------------------------

question = st.chat_input(
    "Ask a salary-related question..."
)

if question:

    # -----------------------------
    # Store User Message
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # -----------------------------
    # Create Prompt
    # -----------------------------

    prompt = f"""
You are a payroll assistant.

Use ONLY the salary data provided below.

Salary Data:
{json.dumps(salary_data, indent=2)}

Rules:

1. Use only salary data provided.
2. Never invent values.
3. Perform calculations when required.
4. Calculate totals accurately.
5. Calculate averages accurately.
6. Compare months when asked.
7. Calculate deduction percentages when asked.
8. Calculate take-home pay when asked.
9. Use Indian Rupees (₹).
10. Explain reasoning step by step.
11. If data is unavailable, clearly state it.
12. Give concise but accurate answers.

Question:
{question}
"""

    # --------------------------------
    # Assistant Response
    # --------------------------------

    with st.chat_message("assistant"):

        reasoning_expander = st.expander(
            "🧠 Model Reasoning",
            expanded=False
        )

        answer_placeholder = st.empty()

        full_response = ""

        try:

            stream = ollama.chat(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True
            )

            for chunk in stream:

                content = chunk["message"]["content"]

                full_response += content

                answer_placeholder.markdown(
                    full_response + "▌"
                )

            answer_placeholder.markdown(
                full_response
            )

            # --------------------------------
            # Extract reasoning if available
            # --------------------------------

            think_match = re.search(
                r"<think>(.*?)</think>",
                full_response,
                re.DOTALL
            )

            if think_match:

                reasoning = think_match.group(1).strip()

                final_answer = re.sub(
                    r"<think>.*?</think>",
                    "",
                    full_response,
                    flags=re.DOTALL
                ).strip()

                with reasoning_expander:
                    st.write(reasoning)

                answer_placeholder.markdown(
                    final_answer
                )

                save_answer = final_answer

            else:

                with reasoning_expander:
                    st.info(
                        "Model did not provide reasoning output."
                    )

                save_answer = full_response

            # Store assistant response

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": save_answer
                }
            )

        except Exception as e:

            st.error(f"Error: {e}")
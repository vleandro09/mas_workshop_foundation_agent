import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # Load environment variables


def main():
    """
    Stage 0 — Foundation Agent:
    A minimal LLM-powered chatbot using Groq ChatCompletions API.
    No memory, no LangChain, no enterprise framework.
    """

    # Load Groq key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("GROQ_API_KEY not found in environment variables.")
        return

    # Initialize Groq client
    client = Groq(api_key=groq_api_key)

    # UI
    st.title("Foundation Agent (Stage 0)")
    st.write("A minimal LLM chatbot using Groq. No memory, no framework, raw LLM behavior.")

    # Sidebar setup
    st.sidebar.title("Customize Your Foundation Agent")
    system_prompt = st.sidebar.text_area("System Prompt:", value="You are a helpful assistant.")
    model = st.sidebar.selectbox(
        "Choose Model:",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    )

    # User input
    user_input = st.text_input("Ask me something:")

    if user_input:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.7,
            )

            response = completion.choices[0].message.content
            st.write("### Response:")
            st.write(response)

        except Exception as e:
            st.error(f"Error calling Groq API: {e}")


if __name__ == "__main__":
    main()

# foundation_agent.py
# Version 1.2 — Same app as before, with very explicit explanations of how messages are sent to Groq

import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # Loads environment variables when running locally


def main():
    """
    Stage 0 — Foundation Agent

    This file shows a very simple Generative AI application.
    It explains clearly how Python code sends questions to Groq
    and why earlier questions and earlier answers are sent again.
    """

    # -------------------------------------------------
    # Read the Groq API key from the environment
    # -------------------------------------------------
    # When this app runs on Heroku, Heroku provides this value.
    # This value is not stored in GitHub and is not visible to users.
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("GROQ_API_KEY not found in environment variables.")
        return

    # Create a Groq client object.
    # This object contains functions that can send requests to Groq.
    client = Groq(api_key=groq_api_key)

    # -------------------------------------------------
    # Build the web page
    # -------------------------------------------------
    # Streamlit is only used to show text boxes and text on the screen.
    # Streamlit does not add memory, intelligence, or logic.
    st.title("Foundation Agent (Stage 0)")
    st.write(
        "This app sends your question to Groq and shows Groq’s response. "
        "It also sends earlier questions and earlier Groq responses again "
        "so follow-up questions make sense."
    )

    # Sidebar controls
    st.sidebar.title("Customize Your Foundation Agent")
    system_prompt = st.sidebar.text_area(
        "System Prompt:",
        value="You are a helpful assistant."
    )
    model = st.sidebar.selectbox(
        "Choose Model:",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    )

    # -------------------------------------------------
    # Store earlier questions and answers in the app
    # -------------------------------------------------
    # Groq does not remember anything between requests.
    # This Python list is the only place where earlier
    # questions and earlier Groq responses are kept.
    #
    # Check whether this app has already created a place to store messages.
    # "messages" is just a name we chose for that stored value.
    # st.session_state is where Streamlit keeps values while the page is open.
    #
    # This line asks:
    # "Have we already created a list called 'messages' for this user session?"
    #
    # If the answer is NO, the next line will create an empty list.
    # If the answer is YES, we do nothing and keep the existing list.
    #
    # This is important because we do NOT want to erase
    # earlier questions and earlier Groq responses every time the app runs.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------------------------------------------------
    # User input
    # -------------------------------------------------
    user_input = st.text_input("Ask me something:")

    if user_input:
        try:
            # -------------------------------------------------
            # Save the new user question
            # -------------------------------------------------
            # This line adds the user’s new question to the list.
            # Nothing is sent to Groq on this line.
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            # -------------------------------------------------
            # SEND REQUEST TO GROQ (THIS IS THE IMPORTANT PART)
            # -------------------------------------------------
            # The function call below is:
            # client.chat.completions.create(...)
            #
            # When Python reaches this line, the following happens in order:
            #
            # 1. Python collects the arguments passed to the function:
            #    - the model name
            #    - the messages list
            #    - the temperature value
            #
            # 2. Python sends these values over the network to Groq.
            #
            # 3. The messages argument is built using the + operator.
            #    The + operator joins two Python lists together:
            #
            #    a) The first list contains one item:
            #       {"role": "system", "content": system_prompt}
            #
            #    b) The second list is st.session_state.messages,
            #       which already contains:
            #       - earlier user questions
            #       - earlier Groq responses
            #       - plus the new user question added above
            #
            # 4. Because these two lists are joined together,
            #    ALL earlier questions and ALL earlier Groq responses
            #    are sent again to Groq along with the new question.
            #
            # 5. Groq processes the text it receives and sends back a reply.
            #
            # 6. Python waits until Groq responds.
            #
            # 7. Python stores Groq’s response in the variable named `completion`.
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt}
                ] + st.session_state.messages,
                temperature=0.7,
            )

            # -------------------------------------------------
            # Read Groq’s reply from the response object
            # -------------------------------------------------
            # The response returned by Groq contains several fields.
            # The generated text is located at:
            # completion.choices[0].message.content
            response = completion.choices[0].message.content

            # -------------------------------------------------
            # Save Groq’s reply
            # -------------------------------------------------
            # This line adds Groq’s reply to the same list.
            # This is why Groq’s old answers are sent again
            # when the next question is asked.
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

            # Show the response on the page
            st.write("### Response:")
            st.write(response)

        except Exception as e:
            st.error(f"Error calling Groq API: {e}")


if __name__ == "__main__":
    main()

import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("MY Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    summary_type = st.sidebar.selectbox(
        "Type of summary",
        (
            "Summarize in 100 words",
            "Summarize in 2 connecting paragraphs",
            "Summarize in 5 bullet points"
        ),
    )

    instruction_map = {
        "Summarize in 100 words": "Summarize the document in about 100 words.",
        "Summarize in 2 connecting paragraphs": "Summarize the document in exactly 2 connecting paragraphs.",
        "Summarize in 5 bullet points": "Summarize the document in exactly 5 bullet points."
    }
    instruction = instruction_map[summary_type]

    use_advanced_model = st.sidebar.checkbox("Use advanced model")
    model = "gpt-5-nano" if use_advanced_model else "gpt-3.5-turbo"

    # Validate the key right away by making a test call.
    # This catches a bad/fake key immediately, instead of waiting
    # until the user has uploaded a document and asked a question.
    try:
        client.models.list()
    except Exception:
        st.error("That API key doesn't seem to work. Please check it and try again.", icon="🚫")
        st.stop()
    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    if uploaded_file:

        # Process the uploaded file.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {instruction}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)

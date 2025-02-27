import streamlit as st
from gradio_client import Client
import os

def analyze_data(file_input, additional_notes):
    api_key = st.secrets["API_KEY"]
    os.environ["GRADIO_API_KEY"] = api_key  # Set API key as an environment variable
    client = Client("m-ric/agent-data-analyst")  # No need to pass api_key here
    result = client.predict(
        file_input=file_input,
        additional_notes=additional_notes,
        api_name="/interact_with_agent"
    )
    return result

st.title("Data Analysis App")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "txt"])
notes = st.text_area("Additional Notes")

if uploaded_file is not None:
    file_path = "uploaded_file"  # You might want to generate a unique filename
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    if st.button("Analyze File"):
        with st.spinner("Analyzing..."):
            try:
                result = analyze_data(file_path, notes)
                st.success("Analysis Complete!")
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                os.remove(file_path) #clean up the uploaded file.

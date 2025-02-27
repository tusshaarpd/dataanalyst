import streamlit as st
from gradio_client import Client, handle_file
import os

def analyze_data(file_input, additional_notes):
    api_key = st.secrets["API_KEY"]
    client = Client("m-ric/agent-data-analyst", api_key=api_key)
    result = client.predict(
        file_input=file_input,
        additional_notes=additional_notes,
        api_name="/interact_with_agent"
    )
    return result

st.title("Data Analyst App")
st.write("Upload a file for analysis")

uploaded_file = st.file_uploader("Your file to analyze", type=["csv", "xlsx", "pdf", "txt"])
notes = st.text_area("Additional notes to support the analysis", "Hello!!")

if uploaded_file is not None:
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("File uploaded successfully!")
    
    if st.button("Analyze File"):
        with st.spinner("Analyzing..."):
            result = analyze_data(file_path, notes)
        st.success("Analysis Complete!")
        st.write(result)
    
    os.remove(file_path)

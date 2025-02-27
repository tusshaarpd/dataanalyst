import streamlit as st
from gradio_client import Client, handle_file
import os

def analyze_data(file_input, api_name):
    api_key = st.secrets.get("API_KEY")
    if not api_key:
        st.error("API Key is missing. Please add it to Streamlit secrets.")
        return None
    
    client = Client("nolanzandi/virtual-data-analyst", api_key=api_key)
    result = client.predict(
        input=file_input,
        api_name=api_name
    )
    return result

st.title("Data Analyst App")
st.write("Upload a file for analysis")

uploaded_file = st.file_uploader("Your file to analyze", type=["csv", "xlsx", "pdf", "txt"])
api_option = st.selectbox("Select API Endpoint", ["/run_example", "/run_example_1", "/example_display"])

if uploaded_file is not None:
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("File uploaded successfully!")
    
    if st.button("Analyze File"):
        with st.spinner("Analyzing..."):
            result = analyze_data(handle_file(file_path), api_option)
        if result:
            st.success("Analysis Complete!")
            st.write(result)
    
    os.remove(file_path)

import streamlit as st
from streamlit_chat import message
import pandas as pd
from llm_utils import chat_with_data_api
from pathlib import Path


def find_file_type_and_read(file):
    # Determine the file extension
    file_extension = Path(file.name).suffix

    # Dictionary mapping file extensions to pandas read functions
    read_functions = {
        ".csv": pd.read_csv,
        ".xlsx": pd.read_excel,
        ".xls": pd.read_excel,
        ".txt": pd.read_csv,  # Assuming text files are treated as CSV
        ".parquet": pd.read_parquet,
        ".json": pd.read_json,
    }

    # Check if the file extension matches any key in the dictionary
    if file_extension in read_functions.keys():
        # Use the corresponding function to read the file
        return read_functions[file_extension](file)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def chat_with_data():
    st.title("Chat with your own data")

    uploaded_file = st.file_uploader(label="Choose file", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        df = find_file_type_and_read(uploaded_file)
        prompt = f"""You are a python expert. You will be given questions for
            manipulating an input dataframe. For ploting a graph or a chart, 
            use the library plotly with streamlit UI and plotlyCharts tool.
            The available columns are: `{df.columns}`.
            Use them for extracting the relevant data.
        """
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": prompt}]
        uploaded_file = st.write("File uploaded successfully!")
    else:
        df = pd.DataFrame([])

    # Every message sent or received in the chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all the previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask your data analyst your questions?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if df.empty:
                st.warning("Dataframe is empty, upload a valid file", icon="⚠️")
                st.session_state.messages = []
            else:
                message_placeholder = st.text("Loading....")
                response = chat_with_data_api(df)
                if response is not None:
                    st.session_state["messages"].append(
                        {"role": "assistant", "content": response}
                    )
                message_placeholder.markdown(response)


if __name__ == "__main__":
    chat_with_data()

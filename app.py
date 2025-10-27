from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

from htmlTemplates import css, bot_template, user_template
import streamlit as st
import tempfile
import os


def handle_userinput(user_question):
    # Call the search_and_summarize method of RAGSearch
    response = st.session_state.rag_search.search_and_summarize(user_question, top_k=3)
    
    # Append the user question and bot response to the chat history
    st.session_state.chat_history.append({"user": user_question, "bot": response})


def main():
    st.set_page_config(page_title="Chat With PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # Initialize session state variables
    if "rag_search" not in st.session_state:
        st.session_state.rag_search = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chat With Multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")

    if st.button("Search"):
        if user_question and st.session_state.rag_search:
            handle_userinput(user_question)
        elif not st.session_state.rag_search:
            st.warning("Please upload and process documents first!")

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload Your PDFs Here & Click Process", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                # Create a temporary directory to save uploaded files
                with tempfile.TemporaryDirectory() as temp_dir:
                    for pdf in pdf_docs:
                        # Save each uploaded file to the temporary directory
                        temp_file_path = os.path.join(temp_dir, pdf.name)
                        with open(temp_file_path, "wb") as f:
                            f.write(pdf.read())

                    # Extract text from the uploaded PDFs
                    raw_text = load_all_documents(temp_dir)
                    # st.write("### Extracted Text:")
                    # st.write(raw_text)

                    # Create vector store
                    store = FaissVectorStore("faiss_store")
                    store.build_from_documents(raw_text)
                    store.load()

                    st.write("### Text Processed Sucessfully.")

                    # Initialize the RAGSearch object and store it in session state
                    st.session_state.rag_search = RAGSearch()

    # Handle user input
    if user_question and st.session_state.rag_search:
        handle_userinput(user_question)

    # Display chat history
    if st.session_state.chat_history:
        for chat in reversed(st.session_state.chat_history):
            st.write(user_template.replace("{{MSG}}", chat["user"]), unsafe_allow_html=True)
            st.write(bot_template.replace("{{MSG}}", chat["bot"]), unsafe_allow_html=True)


if __name__ == "__main__":
    main()

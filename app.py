"""
Streamlit web interface for the RAG ChatBot.
Run with: streamlit run app.py
"""

import streamlit as st
import os
from pathlib import Path
from rag import Embedder, Generator, Retriever, VectorStore


@st.cache_resource
def load_rag_components():
    """Load RAG components once and cache them."""
    index_path = "index"
    if not os.path.exists(index_path):
        return None, None, None, None
    
    store = VectorStore.load(index_path)
    embedder = Embedder()
    retriever = Retriever(embedder, store)
    generator = Generator()
    return store, embedder, retriever, generator


def main():
    st.set_page_config(
        page_title="RAG ChatBot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 RAG ChatBot")
    st.markdown("Ask questions about your documents!")
    
    # Load RAG components
    store, embedder, retriever, generator = load_rag_components()
    
    if store is None:
        st.error("No index found! Please run `python ingest.py` first to build the index.")
        st.info("Place your documents in the `docs/` folder and run: `python ingest.py --docs docs/ --index index/`")
        return
    
    st.success(f"✅ Loaded {len(store)} document chunks")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        k = st.slider("Number of chunks to retrieve", 1, 10, 4)
        mode = st.selectbox("Retrieval mode", ["hybrid", "semantic", "keyword"])
        show_sources = st.checkbox("Show source chunks", True)
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Retrieve relevant chunks
                results = retriever.retrieve(prompt, k=k, mode=mode)
                
                # Show sources if enabled
                if show_sources and results:
                    with st.expander("📚 Retrieved Sources"):
                        for i, (chunk, score) in enumerate(results, start=1):
                            st.markdown(f"**Source {i}** (Score: {score:.3f})")
                            st.markdown(f"📄 {os.path.basename(chunk.source)}")
                            st.text(chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text)
                            st.divider()
                
                # Generate answer
                answer = generator.answer(prompt, results)
                st.markdown(answer)
                
                # Add assistant message
                st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
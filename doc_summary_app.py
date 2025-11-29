"""
Document Summarization App using Amazon Bedrock Converse API
Interactive Streamlit frontend for PDF document analysis with native PDF processing
"""

import streamlit as st
import doc_summary_lib as lib

# Page configuration
st.set_page_config(
    page_title="AWS Bedrock Document Summarizer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF9900;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #232F3E;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .summary-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF9900;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📄 AWS Bedrock Document Summarizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered document analysis using Amazon Bedrock Converse API</p>', unsafe_allow_html=True)

# Initialize session state
if 'pdf_file' not in st.session_state:
    st.session_state.pdf_file = None
if 'pdf_file_name' not in st.session_state:
    st.session_state.pdf_file_name = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    model_options = {
        "Claude 3 Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
        "Claude 3 Haiku": "anthropic.claude-3-haiku-20240307-v1:0",
        "Claude 3.5 Sonnet": "anthropic.claude-3-5-sonnet-20240620-v1:0"
    }
    selected_model_name = st.selectbox(
        "Select Model",
        options=list(model_options.keys()),
        index=0
    )
    model_id = model_options[selected_model_name]
    
    st.divider()
    
    # Summary style
    st.subheader("Summary Style")
    summary_style = st.radio(
        "Choose style:",
        options=["concise", "detailed", "bullet-points", "executive"],
        index=0
    )
    
    st.divider()
    
    # Information
    st.info("""
    **Features:**
    - PDF upload & analysis
    - Multiple summary styles
    - Sentiment analysis
    - Topic extraction
    - Q&A about documents
    """)

# Chat input must be outside tabs (Streamlit limitation)
# Handle Q&A input first if document is loaded
if st.session_state.pdf_file is not None:
    st.markdown("---")
    st.markdown("### 💬 Ask Questions About Your Document")
    st.info("✨ Type your question below and press Enter to get AI-powered answers!")
    question = st.chat_input("💬 Ask a question about the document...")
    
    if question:
        # Process question
        with st.spinner("🤔 Thinking..."):
            try:
                result = lib.answer_questions_about_document(
                    st.session_state.pdf_file,
                    question,
                    model_id
                )
                
                # Save to history
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": result["answer"]
                })
                
                # Rerun to update the display
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Main content area with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📤 Upload & Summarize", 
    "💬 Ask Questions", 
    "🎭 Sentiment Analysis",
    "🏷️ Topic Extraction",
    "ℹ️ About"
])

# Tab 1: Upload and Summarize
with tab1:
    st.header("Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to summarize"
    )
    
    if uploaded_file is not None:
        # Store PDF file in session state
        st.session_state.pdf_file = uploaded_file
        st.session_state.pdf_file_name = uploaded_file.name
        
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.caption(f"File size: {uploaded_file.size / 1024:.2f} KB")
        
        st.divider()
        
        # Summarization section
        st.subheader("Generate Summary")
        
        st.info(f"Using **{summary_style}** style with native Bedrock PDF processing")
        
        summarize_button = st.button(
            "✨ Summarize",
            type="primary"
        )
        
        if summarize_button:
            with st.spinner("📄 Processing PDF with Amazon Bedrock Converse API..."):
                try:
                    # Generate summary directly from PDF
                    result = lib.summarize_pdf_document(
                        st.session_state.pdf_file,
                        summary_style,
                        model_id
                    )
                    
                    # Display summary
                    st.markdown("### 📋 Summary")
                    st.markdown(f'<div class="summary-box">{result["summary"]}</div>', unsafe_allow_html=True)
                    
                    # Display metadata
                    st.divider()
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Model", selected_model_name)
                    with col2:
                        st.metric("Input Tokens", result["input_tokens"])
                    with col3:
                        st.metric("Output Tokens", result["output_tokens"])
                    with col4:
                        st.metric("Stop Reason", result["stop_reason"])
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Tab 2: Ask Questions
with tab2:
    st.header("Ask Questions About Your Document")
    
    if st.session_state.pdf_file is None:
        st.warning("⚠️ Please upload a PDF document first in the 'Upload & Summarize' tab.")
    else:
        # Document info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✅ Document loaded: {st.session_state.pdf_file_name}")
        with col2:
            if st.session_state.chat_history:
                st.metric("Questions Asked", len(st.session_state.chat_history))
        
        st.divider()
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 💬 Q&A Session")
            
            # Display all Q&A pairs in chronological order
            for idx, chat in enumerate(st.session_state.chat_history, 1):
                # Question
                with st.chat_message("user", avatar="🙋"):
                    st.markdown(f"**Q{idx}:** {chat['question']}")
                
                # Answer
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(chat["answer"])
            
            st.divider()
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("🗑️ Clear History", type="secondary", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
            with col2:
                if st.button("📥 Export Chat", type="secondary", use_container_width=True):
                    # Create exportable text
                    export_text = "# Document Q&A Session\n\n"
                    for idx, chat in enumerate(st.session_state.chat_history, 1):
                        export_text += f"## Question {idx}\n{chat['question']}\n\n"
                        export_text += f"## Answer {idx}\n{chat['answer']}\n\n"
                        export_text += "---\n\n"
                    
                    st.download_button(
                        label="💾 Download",
                        data=export_text,
                        file_name="document_qa_session.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
        else:
            # Empty state with helpful message
            st.markdown("### 🎯 Get Started")
            st.info("""
            **No questions asked yet!** 
            
            Use the **chat input at the bottom of the page** to ask questions about your document.
            
            **Example questions:**
            - What is the main topic of this document?
            - Can you summarize the key findings?
            - What are the recommendations mentioned?
            - Who are the main stakeholders discussed?
            """)

# Tab 3: Sentiment Analysis
with tab3:
    st.header("Document Sentiment Analysis")
    
    if st.session_state.pdf_file is None:
        st.warning("⚠️ Please upload a PDF document first.")
    else:
        st.info("Analyze the overall sentiment and emotional tone of your document using Bedrock.")
        
        if st.button("🎭 Analyze Sentiment", type="primary"):
            with st.spinner("📄 Analyzing sentiment with Bedrock..."):
                try:
                    result = lib.analyze_document_sentiment(
                        st.session_state.pdf_file,
                        model_id
                    )
                    
                    st.markdown("### Analysis Results")
                    st.markdown(f'<div class="summary-box">{result["analysis"]}</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Tab 4: Topic Extraction
with tab4:
    st.header("Extract Key Topics")
    
    if st.session_state.pdf_file is None:
        st.warning("⚠️ Please upload a PDF document first.")
    else:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            num_topics = st.slider(
                "Number of topics to extract",
                min_value=3,
                max_value=10,
                value=5
            )
        
        with col2:
            st.write("")
            st.write("")
            extract_button = st.button("🏷️ Extract Topics", type="primary", use_container_width=True)
        
        if extract_button:
            with st.spinner("📄 Extracting key topics with Bedrock..."):
                try:
                    result = lib.extract_key_topics(
                        st.session_state.pdf_file,
                        num_topics,
                        model_id
                    )
                    
                    st.markdown("### Key Topics & Themes")
                    st.markdown(f'<div class="summary-box">{result["topics"]}</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Tab 5: About
with tab5:
    st.header("About This Application")
    
    st.markdown("""
    ### 🎯 Features
    
    This application demonstrates the power of **Amazon Bedrock Converse API** for document analysis:
    
    #### Core Capabilities
    - **📄 PDF Processing**: Upload and extract text from PDF documents
    - **✨ AI Summarization**: Generate summaries in multiple styles (concise, detailed, bullet-points, executive)
    - **💬 Document Q&A**: Ask questions about your documents using RAG-style approach
    - **🎭 Sentiment Analysis**: Analyze the emotional tone and writing style
    - **🏷️ Topic Extraction**: Identify key themes and topics automatically
    
    #### Technical Stack
    - **Backend**: Amazon Bedrock Converse API
    - **Models**: Claude 3 family (Sonnet, Haiku, 3.5 Sonnet)
    - **Frontend**: Streamlit
    - **PDF Processing**: Native Bedrock document understanding
    
    ### 🔧 Related Labs
    
    Explore more Bedrock capabilities in the workshop:
    
    - **RAG (Retrieval-Augmented Generation)**: `completed/rag/`
    - **Chatbots**: `completed/chatbot/`
    - **Embeddings**: `completed/embedding/` and `completed/embeddings_search/`
    - **Multimodal Features**: `completed/image/`, `completed/image_understanding/`
    - **Guardrails**: `completed/guardrails/`
    - **Tool Use**: `completed/tool_use/`
    
    ### 📚 Learn More
    
    - [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
    - [Converse API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
    - [Anthropic Claude Models](https://www.anthropic.com/claude)
    
    ### 🚀 Getting Started
    
    1. Ensure AWS credentials are configured
    2. Install dependencies: `pip install -r requirements.txt`
    3. Run the app: `streamlit run doc_summary_app.py`
    """)
    
    st.divider()
    
    st.info("""
    **💡 Pro Tips:**
    - Use **Claude 3.5 Sonnet** for best quality results
    - Use **Claude 3 Haiku** for faster, cost-effective processing
    - Try different summary styles to find what works best for your use case
    - The chat input activates after you upload and summarize a document
    """)

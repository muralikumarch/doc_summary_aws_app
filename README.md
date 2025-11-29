# AWS Bedrock Document Summarizer

A complete GenAI application for summarizing documents using Amazon Bedrock's Converse API with an interactive Streamlit frontend.

## 🌟 Features

### Core Functionality
- **📄 PDF Document Upload & Processing**: Upload PDF files and extract text content
- **✨ AI-Powered Summarization**: Generate summaries in multiple styles
  - Concise (2-3 paragraphs)
  - Detailed (comprehensive coverage)
  - Bullet-points (key ideas highlighted)
  - Executive (leadership-focused insights)
- **💬 Document Q&A**: Ask questions about uploaded documents using RAG-style approach
- **🎭 Sentiment Analysis**: Analyze emotional tone and writing style
- **🏷️ Topic Extraction**: Automatically identify key themes and topics

### Technical Capabilities
- **Dual Processing Modes**:
  - Text extraction method (using PyPDF2)
  - Direct PDF processing (native Bedrock document understanding)
- **Multiple Claude Models**:
  - Claude 3 Sonnet (balanced performance)
  - Claude 3 Haiku (fast & cost-effective)
  - Claude 3.5 Sonnet (best quality)
- **Interactive Chat Interface**: Conversational Q&A about documents
- **Token Usage Tracking**: Monitor API usage and costs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials configured (via AWS CLI or environment variables)

### Installation

1. **Install dependencies**:
```powershell
pip install -r requirements.txt
```

2. **Configure AWS credentials** (if not already done):
```powershell
aws configure
```

3. **Run the application**:
```powershell
streamlit run doc_summary_app.py
```

4. **Access the app**: Open your browser to `http://localhost:8501`

## 📖 Usage Guide

### 1. Upload & Summarize
1. Upload a PDF document
2. Click "Extract Text" to process the PDF
3. Choose your preferred summary style
4. Click "Summarize" to generate AI summary

### 2. Ask Questions
1. Ensure a document is loaded
2. Type questions in the chat input
3. Get instant answers based on document content
4. View chat history of all Q&A interactions

### 3. Sentiment Analysis
1. Load a document
2. Click "Analyze Sentiment"
3. Get insights on emotional tone and writing style

### 4. Topic Extraction
1. Load a document
2. Select number of topics (3-10)
3. Click "Extract Topics"
4. View key themes and descriptions

## 🏗️ Architecture

```
doc_summary_aws_app/
├── doc_summary_app.py      # Streamlit frontend application
├── doc_summary_lib.py      # Backend logic with Bedrock API
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Key Components

#### `doc_summary_lib.py`
Backend library providing:
- `extract_text_from_pdf()`: PDF text extraction
- `summarize_document_with_text()`: Text-based summarization
- `summarize_document_with_pdf()`: Direct PDF summarization
- `analyze_document_sentiment()`: Sentiment analysis
- `extract_key_topics()`: Topic extraction
- `answer_questions_about_document()`: Q&A functionality

#### `doc_summary_app.py`
Streamlit frontend with:
- Multi-tab interface (Upload, Q&A, Sentiment, Topics, About)
- Model selection sidebar
- Summary style configuration
- Real-time processing feedback
- Chat-based Q&A interface

## 🔧 Configuration

### Model Selection
Choose from available Claude models in the sidebar:
- **Claude 3 Sonnet**: Balanced performance and quality
- **Claude 3 Haiku**: Fastest, most cost-effective
- **Claude 3.5 Sonnet**: Highest quality (recommended)

### Summary Styles
- **Concise**: Quick 2-3 paragraph overview
- **Detailed**: Comprehensive summary covering all key points
- **Bullet-points**: Main ideas in easy-to-scan format
- **Executive**: Leadership-focused actionable insights

## 🎯 API Details

### Bedrock Converse API
This app uses the `converse()` method which provides:
- Unified interface across models
- Native document support
- Streaming capabilities
- Multi-modal input support

### Example API Call
```python
response = bedrock_runtime.converse(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "document": {
                        "format": "pdf",
                        "name": "document.pdf",
                        "source": {"bytes": pdf_bytes}
                    }
                },
                {"text": "Summarize this document"}
            ]
        }
    ],
    inferenceConfig={
        "temperature": 0.5,
        "maxTokens": 2048
    }
)
```

## 💡 Best Practices

### Performance Optimization
- Use **Claude 3 Haiku** for quick summaries of short documents
- Use **Claude 3.5 Sonnet** for complex analysis requiring high accuracy
- Adjust temperature (0.2-0.7) based on creativity vs consistency needs

### Cost Optimization
- Extract text once and reuse for multiple operations
- Use appropriate token limits (maxTokens parameter)
- Choose models based on task complexity

### Quality Tips
- For best summaries, use the "detailed" or "executive" styles
- Direct PDF processing works better for complex formatting
- Lower temperature (0.2-0.3) for factual Q&A
- Higher temperature (0.5-0.7) for creative summaries

## 🐛 Troubleshooting

### Common Issues

**"Could not locate credentials"**
- Ensure AWS credentials are configured: `aws configure`
- Check environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

**"Model not found"**
- Verify Bedrock model access in your AWS region
- Request model access in AWS Console > Bedrock > Model access

**"PDF extraction failed"**
- Ensure PDF is not encrypted or password-protected
- Try Direct PDF processing method instead

**"Token limit exceeded"**
- Document too large for single API call
- Consider chunking large documents

## 📚 Additional Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Converse API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

This is a workshop example. Feel free to extend and customize:
- Add support for more document formats (DOCX, TXT, etc.)
- Implement document comparison features
- Add export functionality (PDF, DOCX reports)
- Integrate with S3 for document storage
- Add user authentication

## 📄 License

See the LICENSE file in the workshop root directory.

---

Built with ❤️ using Amazon Bedrock Converse API and Streamlit

# Testing Guide for AWS Bedrock Document Analyzer

This guide provides comprehensive test scenarios for all features including RAG, guardrails, document comparison, and question generation.

---

## 🚀 Quick Start Testing

### Prerequisites
1. Ensure you have a PDF document uploaded (any multi-page PDF works)
2. AWS credentials configured with Bedrock access
3. All dependencies installed: `pip install -r requirements.txt`

---

## 📋 Feature Testing Scenarios

### 1. **Basic Document Summarization**

#### Test Case 1.1: Different Summary Styles
**Steps:**
1. Upload a technical document (e.g., research paper, whitepaper)
2. Select "Concise" style → Click "Summarize Document"
3. Change to "Detailed" → Click "Summarize Document" again
4. Try "Bullet Points" and "Executive" styles

**Expected Results:**
- Concise: 2-3 paragraphs
- Detailed: Comprehensive coverage of all sections
- Bullet Points: Clear, structured list format
- Executive: High-level insights suitable for leadership

**Sample Documents to Test:**
- AWS whitepapers
- Research papers (PDF format)
- Business proposals
- Technical documentation

---

### 2. **RAG-Enabled Q&A (Conversational Context)**

#### Test Case 2.1: Simple Questions
**Steps:**
1. Upload a document about AWS services
2. Enable "Use RAG" in sidebar (should be ON by default)
3. Ask: "What is the main topic of this document?"
4. Ask: "What are the key benefits mentioned?"

**Expected Results:**
- Answers reference document content
- Responses are contextual and accurate

#### Test Case 2.2: Follow-up Questions (RAG Context)
**Steps:**
1. Ask: "What is Amazon S3?"
2. Follow up: "What are its main use cases?"
3. Follow up: "How does it compare to the previous point?"

**Expected Results:**
- Second question understands "its" refers to S3
- Third question references conversation history
- Chat history shows in the interface

**Sample Questions:**
```
Initial: "What security features are mentioned?"
Follow-up: "Can you elaborate on the first one?"
Follow-up: "How does it compare to the second feature?"
```

#### Test Case 2.3: RAG vs Non-RAG Comparison
**Steps:**
1. Ask a question with RAG enabled
2. Toggle "Use RAG" OFF in sidebar
3. Ask the same follow-up question

**Expected Results:**
- With RAG: Understands context from previous questions
- Without RAG: Treats each question independently

---

### 3. **Content Guardrails (PII Filtering)**

#### Test Case 3.1: PII Detection in Questions
**Steps:**
1. Enable "Use Guardrails" in sidebar
2. Ask: "My email is john.doe@example.com - what does the document say about privacy?"
3. Check chat history

**Expected Results:**
- Email is redacted: `[EMAIL_REDACTED]`
- Question is processed safely

#### Test Case 3.2: Multiple PII Types
**Steps:**
1. Enable guardrails
2. Ask: "My SSN is 123-45-6789 and credit card 1234567812345678. What about data protection?"

**Expected Results:**
- SSN redacted: `[SSN_REDACTED]`
- Card redacted: `[CARD_REDACTED]`
- Document still answers the core question

#### Test Case 3.3: Guardrails OFF
**Steps:**
1. Disable "Use Guardrails"
2. Ask the same question with PII

**Expected Results:**
- PII not filtered (passes through as-is)
- Demonstrates the toggle functionality

**PII Test Patterns:**
```
Email: test@example.com
SSN: 123-45-6789
Credit Card: 1234567812345678
```

---

### 4. **Document Comparison**

#### Test Case 4.1: Compare Similar Documents
**Steps:**
1. Go to "Compare Documents" tab
2. Upload two versions of the same document (e.g., v1 and v2 of a proposal)
3. Click "Compare Documents"

**Expected Results:**
- Lists main similarities
- Highlights key differences
- Shows unique points in each document
- Provides overall summary

#### Test Case 4.2: Compare Different Topics
**Steps:**
1. Upload document about AWS EC2
2. Upload document about AWS S3
3. Compare them

**Expected Results:**
- Clear differentiation between compute vs storage
- Identifies any common AWS themes
- Highlights unique capabilities

**Sample Document Pairs:**
- AWS EC2 guide vs AWS Lambda guide
- Business proposal v1 vs v2
- Research paper A vs research paper B on similar topics

---

### 5. **Question Generation**

#### Test Case 5.1: Generate Study Questions
**Steps:**
1. Go to "Generate Questions" tab
2. Set number of questions: 5
3. Click "Generate Questions"

**Expected Results:**
- Mix of factual and analytical questions
- Questions cover key concepts from document
- Useful for study/review purposes

#### Test Case 5.2: Different Question Counts
**Steps:**
1. Generate 3 questions
2. Generate 10 questions
3. Compare the outputs

**Expected Results:**
- 3 questions: High-level, most critical concepts
- 10 questions: More comprehensive coverage

**Sample Use Cases:**
- Creating study guides from textbooks
- Preparing interview questions from job descriptions
- Generating discussion questions from research papers

---

### 6. **Sentiment Analysis**

#### Test Case 6.1: Positive Document
**Steps:**
1. Upload a positive document (success story, achievements report)
2. Go to "Sentiment Analysis" tab
3. Click "Analyze Sentiment"

**Expected Results:**
- Overall sentiment: Positive
- Identifies optimistic tones
- Notes confident writing style

#### Test Case 6.2: Neutral/Technical Document
**Steps:**
1. Upload technical documentation
2. Analyze sentiment

**Expected Results:**
- Neutral sentiment
- Professional/objective tone
- Informative writing style

---

### 7. **Topic Extraction**

#### Test Case 7.1: Extract Multiple Topics
**Steps:**
1. Go to "Topic Extraction" tab
2. Set slider to 5 topics
3. Click "Extract Topics"

**Expected Results:**
- 5 distinct topics identified
- Brief description for each
- Topics reflect document structure

#### Test Case 7.2: Adjust Topic Count
**Steps:**
1. Try with 3 topics (high-level themes)
2. Try with 10 topics (granular breakdown)

**Expected Results:**
- 3 topics: Broad categories
- 10 topics: More detailed categorization

---

### 8. **Model Comparison**

#### Test Case 8.1: Compare Model Responses
**Steps:**
1. Upload a document
2. Summarize with "Claude 3 Sonnet" (default)
3. Change model to "Claude 3 Haiku"
4. Summarize the same document

**Expected Results:**
- Sonnet: More detailed, nuanced
- Haiku: Faster, more concise
- Both accurate but different styles

#### Test Case 8.2: Speed vs Quality
**Steps:**
1. Ask complex question with Haiku (fast)
2. Ask same question with Claude 3.5 Sonnet (quality)

**Expected Results:**
- Haiku: Quick response
- 3.5 Sonnet: More comprehensive answer

---

## 🧪 Integration Testing Scenarios

### Scenario 1: Complete Workflow
**Steps:**
1. Upload research paper
2. Generate 5 questions from it
3. Use those questions in Q&A tab (with RAG enabled)
4. Export chat history
5. Check for continuity

### Scenario 2: Multi-Document Analysis
**Steps:**
1. Upload document A → Summarize → Note key points
2. Upload document B → Summarize
3. Go to Compare tab → Upload both A and B
4. Review comprehensive comparison

### Scenario 3: Privacy-Aware Q&A
**Steps:**
1. Enable guardrails
2. Ask questions with embedded PII
3. Verify all PII is filtered
4. Confirm answers still make sense

---

## 📊 Performance Testing

### Test Case: Token Usage Tracking
**Steps:**
1. Note input/output tokens for each operation
2. Compare across different models:
   - Haiku: Lowest token usage
   - Sonnet: Moderate
   - 3.5 Sonnet: Higher but better quality

**Metrics to Track:**
- Input tokens per summary style
- Output tokens per model
- Total cost estimation

---

## 🔍 Edge Cases & Error Handling

### Test Case: Large Documents
**Steps:**
1. Upload very large PDF (50+ pages)
2. Try summarization
3. Check if token limits are handled

### Test Case: Scanned PDFs
**Steps:**
1. Upload image-based PDF (scanned document)
2. Test if Bedrock can process it
3. Note: Claude models can handle image-based PDFs

### Test Case: Empty Questions
**Steps:**
1. Try submitting empty question
2. Verify error handling

### Test Case: Invalid File Upload
**Steps:**
1. Try uploading non-PDF file
2. Check error messages

---

## 📝 Sample Test Documents

### Recommended Test PDFs:
1. **AWS Whitepapers**: https://aws.amazon.com/whitepapers/
   - Test technical content understanding
   
2. **Research Papers**: Any academic PDF
   - Test analytical capabilities
   
3. **Business Documents**: Create sample proposals
   - Test executive summary styles
   
4. **Multi-version Documents**: Create v1 and v2
   - Test document comparison

---

## ✅ Validation Checklist

- [ ] All summary styles work correctly
- [ ] RAG maintains conversation context across 3+ exchanges
- [ ] Guardrails filter SSN, emails, credit cards
- [ ] Document comparison identifies similarities/differences
- [ ] Question generation produces relevant questions
- [ ] Sentiment analysis accurate for different tones
- [ ] Topic extraction scales with slider (3-10 topics)
- [ ] All three models (Haiku, Sonnet, 3.5 Sonnet) functional
- [ ] Chat history exports successfully
- [ ] Token metrics display correctly
- [ ] File upload handles various PDF types
- [ ] Error messages clear and helpful

---

## 🐛 Common Issues & Solutions

**Issue**: "Bedrock API error: Validation Exception"
- **Solution**: Filename has invalid characters. App auto-sanitizes, but check uploaded file names.

**Issue**: Chat history not showing context
- **Solution**: Ensure "Use RAG" is enabled in sidebar.

**Issue**: PII not being filtered
- **Solution**: Toggle "Use Guardrails" ON in sidebar.

**Issue**: Slow responses
- **Solution**: Switch to Claude Haiku for faster processing.

---

## 💡 Advanced Testing Ideas

1. **Batch Testing**: Upload same doc, run all features sequentially
2. **Stress Testing**: Rapid-fire questions to test rate limiting
3. **Comparison Matrix**: Test all 3 models on same question
4. **History Limit**: Ask 10+ questions, verify only last 3 used in RAG
5. **Cross-tab Testing**: Upload in one tab, use in another

---

## 📞 Support & Debugging

If issues occur:
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify boto3 version: `pip show boto3` (need ≥1.34.60)
3. Check Streamlit version: `streamlit --version`
4. Review app logs in terminal
5. Test with simple/small PDF first

---

**Happy Testing! 🎉**

For questions or issues, refer to the main README or AWS Bedrock documentation.

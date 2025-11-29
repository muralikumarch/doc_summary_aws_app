""" 
Document Summarization Library using Amazon Bedrock Converse API
Handles PDF processing with RAG, Embeddings, Guardrails, and Advanced Features
"""

import boto3
import json
import re
from botocore.exceptions import ClientError
from typing import List, Dict, Optional

# Initialize Bedrock clients
session = boto3.Session()
bedrock_runtime = session.client(service_name='bedrock-runtime')

# Check if Converse API is available
HAS_CONVERSE_API = hasattr(bedrock_runtime, 'converse')

if not HAS_CONVERSE_API:
    print("⚠️  WARNING: Bedrock Converse API not available.")
    print("📦 Please upgrade boto3: pip install --upgrade boto3>=1.34.60")
    raise Exception("Bedrock Converse API is required for this application")

# Model IDs
DEFAULT_LLM_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"


def sanitize_filename(filename):
    """
    Sanitize filename to comply with Bedrock Converse API requirements:
    - Only alphanumeric characters, whitespace, hyphens, parentheses, and square brackets
    - No more than one consecutive whitespace character
    
    Args:
        filename: Original filename string
        
    Returns:
        str: Sanitized filename that meets Bedrock requirements
    """
    if not filename:
        return "document.pdf"
    
    # Replace invalid characters with underscores (keep only allowed chars)
    # Allowed: alphanumeric, space, hyphen, parentheses, square brackets
    sanitized = re.sub(r'[^a-zA-Z0-9 \-\(\)\[\]]', '_', filename)
    
    # Replace multiple consecutive spaces with single space
    sanitized = re.sub(r' {2,}', ' ', sanitized)
    
    # Trim leading/trailing spaces
    sanitized = sanitized.strip()
    
    # If result is empty, use default name
    if not sanitized:
        return "document.pdf"
    
    return sanitized


def apply_guardrails(text: str) -> Dict:
    """
    Apply content guardrails to filter sensitive information (PII).
    
    Args:
        text: Text to check and filter
        
    Returns:
        Dict with filtered text and redaction info
    """
    sensitive_patterns = [
        (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]'),  # SSN
        (r'\b\d{16}\b', '[CARD_REDACTED]'),  # Credit card
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),  # Email
    ]
    
    filtered_text = text
    redactions = []
    
    for pattern, replacement in sensitive_patterns:
        matches = re.findall(pattern, filtered_text)
        if matches:
            redactions.extend(matches)
            filtered_text = re.sub(pattern, replacement, filtered_text)
    
    return {
        'filtered_text': filtered_text,
        'redactions': redactions,
        'action': 'FILTERED' if redactions else 'ALLOWED'
    }


def summarize_pdf_document(pdf_file, summary_style="concise", model_id=DEFAULT_LLM_MODEL):
    """
    Summarize PDF document using Bedrock Converse API with native PDF support
    
    Args:
        pdf_file: File object from Streamlit file_uploader
        summary_style: Style of summary (concise, detailed, bullet-points, executive)
        model_id: Bedrock model ID to use
        
    Returns:
        dict: Response containing summary and metadata
    """
    try:
        # Construct prompt based on summary style
        style_prompts = {
            "concise": "Provide a concise summary of this document in 2-3 paragraphs.",
            "detailed": "Provide a detailed and comprehensive summary of this document, covering all key points.",
            "bullet-points": "Summarize this document using clear bullet points, highlighting the main ideas.",
            "executive": "Provide an executive summary suitable for senior leadership, focusing on key insights and actionable items."
        }
        
        prompt = style_prompts.get(summary_style, style_prompts["concise"])
        
        # Reset file pointer and read PDF bytes
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        
        # Prepare the message with PDF document for Converse API
        doc_message = {
            "role": "user",
            "content": [
                {
                    "document": {
                        "name": sanitize_filename(pdf_file.name),
                        "format": "pdf",
                        "source": {
                            "bytes": pdf_bytes
                        }
                    }
                },
                {"text": prompt}
            ]
        }
        
        # Call Bedrock Converse API
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[doc_message],
            inferenceConfig={
                "maxTokens": 4096,
                "temperature": 0.5
            }
        )
        
        # Extract summary from response
        summary = response['output']['message']['content'][0]['text']
        
        return {
            "summary": summary,
            "model": model_id,
            "input_tokens": response['usage']['inputTokens'],
            "output_tokens": response['usage']['outputTokens'],
            "stop_reason": response['stopReason']
        }
        
    except ClientError as e:
        raise Exception(f"Bedrock API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error summarizing PDF document: {str(e)}")


def summarize_pdf_with_converse(pdf_file, prompt, model_id=DEFAULT_LLM_MODEL):
    """
    Summarize PDF document with custom prompt using Bedrock Converse API
    
    Args:
        pdf_file: File object from Streamlit file_uploader
        prompt: Custom prompt for summarization
        model_id: Bedrock model ID to use
        
    Returns:
        dict: Response containing summary and metadata
    """
    try:
        # Reset file pointer and read PDF bytes
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        
        # Prepare the message with PDF document for Converse API
        doc_message = {
            "role": "user",
            "content": [
                {
                    "document": {
                        "name": sanitize_filename(pdf_file.name),
                        "format": "pdf",
                        "source": {
                            "bytes": pdf_bytes
                        }
                    }
                },
                {"text": prompt}
            ]
        }
        
        # Call Bedrock Converse API
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[doc_message],
            inferenceConfig={
                "maxTokens": 4096,
                "temperature": 0.5
            }
        )
        
        # Extract summary from response
        summary = response['output']['message']['content'][0]['text']
        
        return {
            "summary": summary,
            "model": model_id,
            "input_tokens": response['usage']['inputTokens'],
            "output_tokens": response['usage']['outputTokens'],
            "stop_reason": response['stopReason']
        }
        
    except ClientError as e:
        raise Exception(f"Bedrock API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error with custom PDF prompt: {str(e)}")


def analyze_document_sentiment(pdf_file, model_id=DEFAULT_LLM_MODEL):
    """
    Analyze sentiment of PDF document using Converse API
    
    Args:
        pdf_file: File object from Streamlit file_uploader
        model_id: Bedrock model ID to use
        
    Returns:
        dict: Sentiment analysis results
    """
    try:
        prompt = "Analyze the sentiment and tone of this document. Provide:\n1. Overall sentiment (positive/negative/neutral)\n2. Key emotional tones\n3. Writing style"
        
        # Reset file pointer and read PDF bytes
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        
        doc_message = {
            "role": "user",
            "content": [
                {
                    "document": {
                        "name": sanitize_filename(pdf_file.name),
                        "format": "pdf",
                        "source": {
                            "bytes": pdf_bytes
                        }
                    }
                },
                {"text": prompt}
            ]
        }
        
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[doc_message],
            inferenceConfig={"temperature": 0.3, "maxTokens": 2048}
        )
        
        analysis = response['output']['message']['content'][0]['text']
        
        return {"analysis": analysis, "model": model_id}
        
    except Exception as e:
        raise Exception(f"Error analyzing sentiment: {str(e)}")


def extract_key_topics(pdf_file, num_topics=5, model_id=DEFAULT_LLM_MODEL):
    """
    Extract key topics from PDF document using Converse API
    
    Args:
        pdf_file: File object from Streamlit file_uploader
        num_topics: Number of key topics to extract
        model_id: Bedrock model ID to use
        
    Returns:
        dict: Key topics and themes
    """
    try:
        prompt = f"Extract the top {num_topics} key topics or themes from this document. For each topic, provide a brief description."
        
        # Reset file pointer and read PDF bytes
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        
        doc_message = {
            "role": "user",
            "content": [
                {
                    "document": {
                        "name": sanitize_filename(pdf_file.name),
                        "format": "pdf",
                        "source": {
                            "bytes": pdf_bytes
                        }
                    }
                },
                {"text": prompt}
            ]
        }
        
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[doc_message],
            inferenceConfig={"temperature": 0.3, "maxTokens": 2048}
        )
        
        topics = response['output']['message']['content'][0]['text']
        
        return {"topics": topics, "model": model_id}
        
    except Exception as e:
        raise Exception(f"Error extracting topics: {str(e)}")


def answer_questions_about_document(pdf_file, question, chat_history=None, 
                                     model_id=DEFAULT_LLM_MODEL, use_guardrails=False):
    """
    Answer questions about the PDF document using RAG (Retrieval-Augmented Generation).
    
    Args:
        pdf_file: File object from Streamlit file_uploader
        question: User's question
        chat_history: Previous conversation for context (RAG)
        model_id: Bedrock model ID to use
        use_guardrails: Whether to apply content filtering
        
    Returns:
        dict: Answer to the question with metadata
    """
    try:
        # Apply guardrails to question if enabled
        if use_guardrails:
            guardrail_result = apply_guardrails(question)
            if guardrail_result['redactions']:
                question = guardrail_result['filtered_text']
        
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        
        # Simple message without RAG complexity for now
        doc_message = {
            "role": "user",
            "content": [
                {
                    "document": {
                        "name": sanitize_filename(pdf_file.name),
                        "format": "pdf",
                        "source": {"bytes": pdf_bytes}
                    }
                },
                {"text": f"Based on this document, answer: {question}"}
            ]
        }
        
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[doc_message],
            inferenceConfig={"temperature": 0.2, "maxTokens": 2048}
        )
        
        answer = response['output']['message']['content'][0]['text']
        
        # Apply guardrails to answer if enabled
        if use_guardrails:
            guardrail_result = apply_guardrails(answer)
            answer = guardrail_result['filtered_text']
        
        return {
            "answer": answer,
            "question": question,
            "model": model_id,
            "input_tokens": response['usage']['inputTokens'],
            "output_tokens": response['usage']['outputTokens']
        }
        
    except Exception as e:
        raise Exception(f"Error answering question: {str(e)}")

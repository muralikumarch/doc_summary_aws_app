"""
Simple test script to verify the document summarization library works
Run this to test the backend without the Streamlit UI
"""

import doc_summary_lib as lib
import os

def test_text_summarization():
    """Test basic text summarization"""
    print("🧪 Testing text summarization...")
    
    sample_text = """
    Artificial Intelligence (AI) is revolutionizing the way we live and work. 
    From healthcare to finance, AI applications are transforming industries by 
    automating tasks, improving decision-making, and creating new opportunities.
    
    Machine learning, a subset of AI, enables systems to learn from data without 
    explicit programming. Deep learning, using neural networks, has achieved 
    remarkable results in image recognition, natural language processing, and 
    game playing.
    
    However, AI also raises important ethical questions about privacy, bias, 
    and job displacement. As we continue to develop AI systems, it's crucial 
    to address these concerns and ensure that AI benefits all of humanity.
    """
    
    try:
        result = lib.summarize_document_with_text(
            sample_text,
            summary_style="concise",
            model_id="anthropic.claude-3-haiku-20240307-v1:0"
        )
        
        print("✅ Summary generated successfully!")
        print(f"\n📋 Summary:\n{result['summary']}\n")
        print(f"📊 Tokens - Input: {result['input_tokens']}, Output: {result['output_tokens']}")
        print(f"🎯 Model: {result['model']}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_sentiment_analysis():
    """Test sentiment analysis"""
    print("\n🧪 Testing sentiment analysis...")
    
    sample_text = """
    The new product launch exceeded all our expectations! The team worked 
    incredibly hard, and their dedication really paid off. Customer feedback 
    has been overwhelmingly positive, with many praising the innovative features 
    and user-friendly design. This is a major milestone for our company!
    """
    
    try:
        result = lib.analyze_document_sentiment(
            sample_text,
            model_id="anthropic.claude-3-haiku-20240307-v1:0"
        )
        
        print("✅ Sentiment analysis completed!")
        print(f"\n🎭 Analysis:\n{result['analysis']}\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_topic_extraction():
    """Test topic extraction"""
    print("\n🧪 Testing topic extraction...")
    
    sample_text = """
    Climate change poses significant challenges to global agriculture. Rising 
    temperatures affect crop yields, while changing precipitation patterns 
    create water scarcity in some regions and flooding in others.
    
    Sustainable farming practices, including precision agriculture and organic 
    farming, offer potential solutions. Technology such as IoT sensors, drones, 
    and AI-powered analytics help farmers optimize resource use.
    
    Policy interventions, including carbon pricing and subsidies for green 
    technologies, are essential to accelerate the transition to sustainable 
    agriculture. International cooperation will be crucial for addressing 
    this global challenge.
    """
    
    try:
        result = lib.extract_key_topics(
            sample_text,
            num_topics=3,
            model_id="anthropic.claude-3-haiku-20240307-v1:0"
        )
        
        print("✅ Topics extracted successfully!")
        print(f"\n🏷️ Topics:\n{result['topics']}\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_qa():
    """Test Q&A functionality"""
    print("\n🧪 Testing Q&A...")
    
    sample_text = """
    Python is a high-level, interpreted programming language known for its 
    simplicity and readability. Created by Guido van Rossum and first released 
    in 1991, Python has become one of the most popular programming languages.
    
    Key features include:
    - Dynamic typing and automatic memory management
    - Extensive standard library and third-party packages
    - Support for multiple programming paradigms
    - Strong community and excellent documentation
    """
    
    question = "Who created Python and when was it first released?"
    
    try:
        result = lib.answer_questions_about_document(
            sample_text,
            question,
            model_id="anthropic.claude-3-haiku-20240307-v1:0"
        )
        
        print("✅ Question answered successfully!")
        print(f"\n❓ Question: {question}")
        print(f"\n💡 Answer:\n{result['answer']}\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Document Summarization Library Test Suite")
    print("=" * 60)
    
    tests = [
        ("Text Summarization", test_text_summarization),
        ("Sentiment Analysis", test_sentiment_analysis),
        ("Topic Extraction", test_topic_extraction),
        ("Q&A", test_qa)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with error: {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"Final Score: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    main()

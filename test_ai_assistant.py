#!/usr/bin/env python3
"""
Simple test script for AI Assistant functionality
Tests the core AI response system without the web interface
"""

import sys
import os

# Add the callcenter_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'callcenter_app'))

def test_ai_assistant():
    """Test AI Assistant functionality"""
    try:
        # Import AI assistant functions
        from pages.ai_assistant import get_ai_response, analyze_user_intent
        
        print("🤖 AI Assistant Test Suite")
        print("=" * 50)
        
        # Test cases
        test_questions = [
            "What's our revenue growth status?",
            "How is our call volume doing?",
            "Tell me about customer satisfaction",
            "What's our profit margin?",
            "Give me an overall summary",
            "Help me understand the dashboard"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📝 Test {i}: {question}")
            print("-" * 40)
            
            # Test intent analysis
            intent = analyze_user_intent(question)
            print(f"🎯 Intent: {intent}")
            
            # Test AI response
            try:
                response = get_ai_response(question)
                print(f"🤖 Response: {response[:200]}..." if len(response) > 200 else f"🤖 Response: {response}")
                print("✅ Success")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\n🎉 AI Assistant test completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize AI Assistant: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_ai_assistant()

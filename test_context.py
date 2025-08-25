#!/usr/bin/env python3
"""
Test script to verify conversation context memory
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from callcenter_app.pages.ai_assistant import get_ai_response, analyze_user_intent_with_history
from dash import html

def test_conversation_flow():
    """Test the conversation flow that was failing"""
    print("🧪 Testing Conversation Context Memory")
    print("=" * 50)
    
    # Simulate conversation history after asking about revenue
    mock_revenue_response = html.Div([
        "📊 **Performance Status:** Current revenue stands at RM 1,400,000, which is RM 100,000 (6.7%) below the target of RM 1,500,000. "
        "💡 **Key recommendations:** • **Business Critical:** Yes - The revenue shortfall could impact operational sustainability and growth targets."
    ])
    
    conversation_history = [mock_revenue_response]
    
    # Test 1: Ask about revenue initially
    print("\n1️⃣ Initial question: 'tell me about our revenue'")
    response1 = get_ai_response("tell me about our revenue", [])
    print(f"✅ Response: {response1[:100]}...")
    
    # Test 2: Follow-up question that should use context
    print("\n2️⃣ Follow-up question: 'Last quarter summary?'")
    
    # Check intent analysis first
    intent = analyze_user_intent_with_history("Last quarter summary?", conversation_history)
    print(f"🧠 Intent Analysis: {intent}")
    
    response2 = get_ai_response("Last quarter summary?", conversation_history)
    print(f"✅ Response: {response2[:200]}...")
    
    # Test 3: Another contextual question
    print("\n3️⃣ Contextual question: 'What about the performance?'")
    intent2 = analyze_user_intent_with_history("What about the performance?", conversation_history)
    print(f"🧠 Intent Analysis: {intent2}")
    
    response3 = get_ai_response("What about the performance?", conversation_history)
    print(f"✅ Response: {response3[:200]}...")
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")

if __name__ == "__main__":
    test_conversation_flow()

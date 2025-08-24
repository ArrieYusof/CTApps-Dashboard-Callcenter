#!/usr/bin/env python3
"""
Test script to verify sidebar toggle functionality
"""
import sys
import os
sys.path.append('/Users/obie/Dev/AI/CTApps/CallCenter/callcenter_app')

from app import toggle_sidebar

def test_toggle_sidebar():
    print("Testing sidebar toggle functionality...")
    
    # Test initial state (n_clicks=None)
    print("\n1. Testing initial state (n_clicks=None):")
    s_style, c_style = toggle_sidebar(None)
    print(f"   Sidebar left: {s_style.get('left', 'not set')}")
    print(f"   Sidebar display: {s_style.get('display', 'not set')}")
    print(f"   Content left: {c_style.get('left', 'not set')}")
    print(f"   Content width: {c_style.get('width', 'not set')}")
    
    # Test first click (n_clicks=1) - should show sidebar
    print("\n2. Testing first click (n_clicks=1):")
    s_style, c_style = toggle_sidebar(1)
    print(f"   Sidebar left: {s_style.get('left', 'not set')}")
    print(f"   Sidebar display: {s_style.get('display', 'not set')}")
    print(f"   Content left: {c_style.get('left', 'not set')}")
    print(f"   Content width: {c_style.get('width', 'not set')}")
    
    # Test second click (n_clicks=2) - should hide sidebar
    print("\n3. Testing second click (n_clicks=2):")
    s_style, c_style = toggle_sidebar(2)
    print(f"   Sidebar left: {s_style.get('left', 'not set')}")
    print(f"   Sidebar display: {s_style.get('display', 'not set')}")
    print(f"   Content left: {c_style.get('left', 'not set')}")
    print(f"   Content width: {c_style.get('width', 'not set')}")
    
    # Test third click (n_clicks=3) - should show sidebar again
    print("\n4. Testing third click (n_clicks=3):")
    s_style, c_style = toggle_sidebar(3)
    print(f"   Sidebar left: {s_style.get('left', 'not set')}")
    print(f"   Sidebar display: {s_style.get('display', 'not set')}")
    print(f"   Content left: {c_style.get('left', 'not set')}")
    print(f"   Content width: {c_style.get('width', 'not set')}")

if __name__ == "__main__":
    test_toggle_sidebar()

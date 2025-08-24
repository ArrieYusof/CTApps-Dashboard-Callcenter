#!/usr/bin/env python3

# Simple test of toggle logic
def test_toggle_logic():
    print("Testing toggle logic:")
    
    test_cases = [None, 0, 1, 2, 3, 4, 5]
    
    for n_clicks in test_cases:
        if n_clicks is None or n_clicks % 2 == 0:
            result = "HIDDEN"
        else:
            result = "VISIBLE"
        
        print(f"  n_clicks={n_clicks} → {result}")

if __name__ == "__main__":
    test_toggle_logic()

#!/usr/bin/env python3
"""
Test Gemini API Integration
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*80)
print("TESTING GEMINI API")
print("="*80 + "\n")

api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key: {api_key[:20]}... (loaded from .env)")

try:
    import google.generativeai as genai
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Test with gemini-2.0-flash-exp (latest)
    print(f"\nTesting Model: gemini-2.0-flash-exp")
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    response = model.generate_content("Extract one obligation from this text: 'All banks must implement enhanced KYC by Dec 31, 2024.' Return as JSON with fields: text, deadline, type.")
    
    print(f"\n✅ Gemini API Working!")
    print(f"\nResponse:")
    print(response.text)
    
    print(f"\nUsage:")
    print(f"  Input tokens: {response.usage_metadata.prompt_token_count}")
    print(f"  Output tokens: {response.usage_metadata.candidates_token_count}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTrying fallback model: gemini-1.5-pro")
    
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Say 'Gemini working' in 2 words")
        print(f"✅ Fallback model working: {response.text}")
    except Exception as e2:
        print(f"❌ Fallback also failed: {e2}")

print("\n" + "="*80)
print("Test Complete")
print("="*80)

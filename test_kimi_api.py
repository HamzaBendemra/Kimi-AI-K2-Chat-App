#!/usr/bin/env python3
"""
Test script to verify Kimi AI API integration
"""

import openai
import os
import sys
from typing import List, Dict

def test_kimi_api(api_key: str) -> bool:
    """Test Kimi AI API connectivity and basic functionality"""
    
    print("🧪 Testing Kimi AI API Integration...")
    print("=" * 50)
    
    try:
        # Initialize OpenAI client with Kimi configuration
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1"
        )
        print("✅ OpenAI client initialized successfully")
        
        # Test basic chat completion
        test_messages = [
            {"role": "system", "content": "You are Kimi, an AI assistant. Provide a brief greeting."},
            {"role": "user", "content": "Hello! Can you hear me?"}
        ]
        
        print("🤖 Sending test message to Kimi AI...")
        
        response = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=test_messages,
            temperature=0.6,
            max_tokens=100
        )
        
        # Extract response
        reply = response.choices[0].message.content
        print(f"✅ API Response received successfully")
        print(f"📨 Kimi's response: {reply}")
        
        # Test model listing (if available)
        try:
            models = client.models.list()
            print(f"✅ Available models retrieved: {len(models.data)} models found")
            
            # Show first few model IDs
            for i, model in enumerate(models.data[:3]):
                print(f"   - {model.id}")
            if len(models.data) > 3:
                print(f"   ... and {len(models.data) - 3} more")
                
        except Exception as e:
            print(f"ℹ️  Model listing not available: {str(e)}")
        
        print("\n🎉 All tests passed! Kimi AI API is working correctly.")
        return True
        
    except openai.APIError as e:
        print(f"❌ API Error: {str(e)}")
        print("💡 Check your API key and ensure you have sufficient credits")
        return False
    
    except openai.APIConnectionError as e:
        print(f"❌ Connection Error: {str(e)}")
        print("💡 Check your internet connection and firewall settings")
        return False
    
    except openai.RateLimitError as e:
        print(f"❌ Rate Limit Error: {str(e)}")
        print("💡 You've hit the rate limit. Wait a moment and try again")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        print("💡 Please check your API key and try again")
        return False

def main():
    """Main test function"""
    
    print("🔑 Kimi AI API Test Tool")
    print("=" * 50)
    print("This tool will test your Kimi AI API integration")
    print()
    
    # Get API key from user
    api_key = input("Enter your Kimi AI API key: ").strip()
    
    if not api_key:
        print("❌ API key is required!")
        sys.exit(1)
    
    # Run tests
    success = test_kimi_api(api_key)
    
    if success:
        print("\n✨ Your Kimi AI API is ready to use!")
        print("🚀 You can now run: streamlit run kimi_chat_app.py")
    else:
        print("\n❌ There was an issue with your API setup.")
        print("📝 Please check the error messages above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
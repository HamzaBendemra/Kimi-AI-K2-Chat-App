import streamlit as st
import openai
import os
from typing import List, Dict, Any
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Kimi AI Chat - Professional AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://platform.moonshot.cn/docs',
        'Report a bug': None,
        'About': "# Kimi AI Chat\nProfessional AI Assistant powered by Moonshot AI"
    }
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .message {
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .assistant-message {
        background: #f0f2f5;
        color: #333;
        margin-right: auto;
    }
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 12px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    .sidebar .element-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'model_name' not in st.session_state:
    st.session_state.model_name = "kimi-k2-turbo-preview"
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.6
if 'max_tokens' not in st.session_state:
    st.session_state.max_tokens = 2000

def initialize_openai_client(api_key: str) -> openai.OpenAI:
    """Initialize OpenAI client with Kimi API configuration"""
    try:
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1"
        )
        return client
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {str(e)}")
        return None

def get_kimi_response(client: openai.OpenAI, messages: List[Dict[str, str]], 
                     model: str, temperature: float, max_tokens: int) -> str:
    """Get response from Kimi AI API"""
    try:
        # Add system message if not present
        if not messages or messages[0].get("role") != "system":
            system_message = {
                "role": "system", 
                "content": "You are Kimi, an AI assistant provided by Moonshot AI. You are to provide helpful and accurate answers."
            }
            messages = [system_message] + messages
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        return f"API Error: {str(e)}"
    except openai.APIConnectionError as e:
        return f"Connection Error: {str(e)}"
    except openai.RateLimitError as e:
        return f"Rate Limit Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

def display_chat_message(role: str, content: str, avatar: str = None):
    """Display a chat message with styling"""
    if role == "user":
        st.markdown(f"""
            <div class="message user-message">
                <strong>You:</strong> {content}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="message assistant-message">
                <strong>Kimi 🤖:</strong> {content}
            </div>
        """, unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # API Key input
    api_key_input = st.text_input(
        "API Key",
        type="password",
        placeholder="Enter your Kimi AI API key...",
        help="Get your API key from platform.moonshot.ai"
    )
    
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    # Model selection
    model_options = [
        "kimi-k2-turbo-preview",
        "kimi-k2-0711-preview", 
        "kimi-k2-0905-preview",
        "moonshot-v1-8k",
        "moonshot-v1-32k",
        "moonshot-v1-128k"
    ]
    st.session_state.model_name = st.selectbox(
        "Model",
        model_options,
        help="Select the Kimi AI model to use"
    )
    
    # Temperature slider
    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.1,
        help="Controls randomness in responses (0.0 = deterministic, 1.0 = creative)"
    )
    
    # Max tokens slider
    st.session_state.max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=4000,
        value=2000,
        step=100,
        help="Maximum number of tokens in the response"
    )
    
    # Clear chat button
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Instructions
    with st.expander("📖 Instructions"):
        st.markdown("""
        ### How to use Kimi Chat:
        
        1. **Get API Key**: Visit [platform.moonshot.ai](https://platform.moonshot.ai) to get your API key
        2. **Enter API Key**: Paste your API key in the sidebar
        3. **Configure Settings**: Choose your preferred model and parameters
        4. **Start Chatting**: Type your message and press Enter
        
        ### Features:
        - 💬 Real-time chat with Kimi AI
        - 🎯 Multiple model options
        - ⚡ Fast response times
        - 💾 Conversation memory
        - 🎨 Modern UI design
        
        ### Tips:
        - Use lower temperature (0.1-0.3) for factual answers
        - Use higher temperature (0.7-1.0) for creative responses
        - The app maintains conversation context
        """)

# Main chat interface
st.title("🤖 Kimi AI Chat")
st.markdown("#### Chat with Kimi AI - Powered by Moonshot AI")

# Check if API key is provided
if not st.session_state.api_key:
    st.warning("⚠️ Please enter your Kimi AI API key in the sidebar to start chatting!")
    st.info("Get your API key from [platform.moonshot.ai](https://platform.moonshot.ai)")
else:
    # Initialize client
    client = initialize_openai_client(st.session_state.api_key)
    
    if client:
        # Display chat container
        chat_container = st.container()
        
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Display chat history
            message_container = st.container()
            with message_container:
                for message in st.session_state.messages:
                    display_chat_message(message["role"], message["content"])
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Type your message here...", key="user_input")
        
        if user_input:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Display user message
            with message_container:
                display_chat_message("user", user_input)
            
            # Get Kimi response
            with st.spinner("🤖 Kimi is thinking..."):
                # Prepare messages for API (exclude system message if already added)
                api_messages = st.session_state.messages.copy()
                
                response = get_kimi_response(
                    client, 
                    api_messages,
                    st.session_state.model_name,
                    st.session_state.temperature,
                    st.session_state.max_tokens
                )
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display assistant response
            with message_container:
                display_chat_message("assistant", response)
            
            # Rerun to update the display
            st.rerun()

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Powered by Kimi AI from Moonshot AI")
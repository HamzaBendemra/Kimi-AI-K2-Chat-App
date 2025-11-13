import streamlit as st
import openai
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Custom CSS for professional, modern styling
st.markdown("""
    <style>
    /* Main app background with soft gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        min-width: 350px !important;
        width: 350px !important;
    }
    
    /* Hide sidebar collapse button */
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    button[kind="header"] {
        display: none;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #ffffff;
        font-weight: 700;
    }
    
    /* Input fields in sidebar */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #334155;
        color: #f1f5f9;
        border: 1px solid #475569;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #818cf8;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2);
    }
    
    /* Selectbox in sidebar */
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: #334155;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background-color: #334155;
        color: #f1f5f9;
        border-color: #475569;
    }
    
    /* Slider in sidebar */
    [data-testid="stSidebar"] .stSlider {
        padding: 1rem 0;
    }
    
    /* Main title styling */
    h1 {
        color: #1e293b;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(255, 255, 255, 0.5);
    }
    
    h4 {
        color: #475569;
        font-weight: 400;
        margin-top: 0;
    }
    
    /* Chat messages container */
    .chat-message {
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 16px;
        animation: fadeIn 0.3s ease-in;
        max-width: 85%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .assistant-message {
        background: #ffffff;
        color: #1e293b;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    }
    
    .message-header {
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .message-content {
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .user-message .message-content {
        color: #ffffff;
    }
    
    .assistant-message .message-content {
        color: #334155;
    }
    
    /* Chat input styling */
    .stChatInput {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stChatInput > div {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    
    .stChatInput > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stChatInput textarea {
        font-size: 1rem;
        padding: 0.75rem;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.875rem;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Primary button (Clear Chat) */
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    }
    
    /* Main content area buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46a0 100%);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Warning and info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    .stSpinner > div > div {
        color: #667eea !important;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #475569;
        padding: 2rem 0 1rem 0;
        font-size: 0.9rem;
        border-top: 1px solid rgba(203, 213, 225, 0.5);
        margin-top: 3rem;
    }
    
    /* Stats badges */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    
    .stat-badge {
        background: rgba(255, 255, 255, 0.8);
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        color: #334155;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid rgba(203, 213, 225, 0.6);
        backdrop-filter: blur(10px);
    }
    
    .stat-badge strong {
        color: #667eea;
        margin-right: 0.5rem;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 16px;
        margin: 2rem 0;
        border: 2px dashed #94a3b8;
        backdrop-filter: blur(10px);
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .empty-state-text {
        color: #1e293b;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .empty-state-subtext {
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Code blocks in messages */
    .message-content code {
        background: rgba(0, 0, 0, 0.1);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    
    .assistant-message code {
        background: #f1f5f9;
    }
    
    /* Links in messages */
    .message-content a {
        color: inherit;
        text-decoration: underline;
        font-weight: 500;
    }
    
    .user-message a {
        color: #fff;
    }
    
    .assistant-message a {
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key' not in st.session_state:
    # Try to load from environment variable first
    env_api_key = os.getenv('KIMI_API_KEY', '')
    st.session_state.api_key = env_api_key
if 'model_name' not in st.session_state:
    st.session_state.model_name = "kimi-k2-turbo-preview"
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.6
if 'max_tokens' not in st.session_state:
    st.session_state.max_tokens = 2000
if 'total_messages' not in st.session_state:
    st.session_state.total_messages = 0

def initialize_openai_client(api_key: str) -> openai.OpenAI:
    """Initialize OpenAI client with Kimi API configuration"""
    try:
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.ai/v1"
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
                "content": "You are Kimi, an AI assistant created by Moonshot AI."
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
    except openai.AuthenticationError as e:
        error_msg = "**Authentication Error** ❌\n\n"
        error_msg += "Your API key is invalid or not activated.\n\n"
        error_msg += "**Troubleshooting Steps:**\n"
        error_msg += "1. Verify your API key at [platform.moonshot.ai](https://platform.moonshot.ai)\n"
        error_msg += "2. Ensure your account has credits (minimum $1)\n"
        error_msg += "3. Check if the API key is active and not expired\n"
        error_msg += "4. Try generating a new API key\n\n"
        error_msg += f"_Error details: {str(e)}_"
        return error_msg
    except openai.APIError as e:
        return f"**API Error** ❌\n\n{str(e)}\n\nPlease try again or contact support."
    except openai.APIConnectionError as e:
        return f"**Connection Error** ❌\n\nCouldn't connect to Kimi AI servers.\n\n{str(e)}"
    except openai.RateLimitError as e:
        return f"**Rate Limit Error** ❌\n\nYou've exceeded the rate limit.\n\n{str(e)}"
    except Exception as e:
        return f"**Unexpected Error** ❌\n\n{str(e)}"

def display_chat_message(role: str, content: str):
    """Display a chat message with professional styling"""
    if role == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-header">
                    <span>👤</span>
                    <span>You</span>
                </div>
                <div class="message-content">{content}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-header">
                    <span>🤖</span>
                    <span>Kimi AI</span>
                </div>
                <div class="message-content">{content}</div>
            </div>
        """, unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:    
    # API Key input with better UX
    st.subheader("🔑 API Authentication")
    
    # Show if API key is loaded from .env
    env_api_key = os.getenv('KIMI_API_KEY', '')
    if env_api_key and not st.session_state.get('api_key_input_override'):
        st.success("✓ API Key loaded from .env", icon="✅")
        st.caption(f"Key: {env_api_key[:8]}...{env_api_key[-4:]}")
        if st.button("🔄 Use different key", key="override_env_key"):
            st.session_state.api_key_input_override = True
            st.rerun()
    else:
        api_key_input = st.text_input(
            "API Key",
            type="password",
            placeholder="sk-xxxxxxxxxxxxxxxx",
            help="Get your API key from platform.moonshot.ai or set KIMI_API_KEY in .env",
            label_visibility="collapsed",
            value=st.session_state.api_key if not env_api_key else ""
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.success("✓ API Key configured", icon="✅")
        elif not env_api_key:
            st.info("Enter your API key to start", icon="ℹ️")
    
    st.markdown("---")
    
    # Model selection with descriptions
    st.subheader("🤖 Model Selection")
    model_descriptions = {
        "kimi-k2-turbo-preview": "⚡ Fastest - Best for quick responses (kimi-k2-turbo-preview)",
        "kimi-k2-0711-preview": "🎯 Latest - Enhanced capabilities (kimi-k2-0711-preview)",
        "kimi-k2-0905-preview": "🧠 Advanced - Superior reasoning (kimi-k2-0905-preview)",
        "moonshot-v1-8k": "📝 Standard - 8K context (moonshot-v1-8k)",
        "moonshot-v1-32k": "📚 Extended - 32K context (moonshot-v1-32k)",
        "moonshot-v1-128k": "📖 Maximum - 128K context (moonshot-v1-128k)"
    }
    
    selected_model = st.selectbox(
        "Choose Model",
        options=list(model_descriptions.keys()),
        format_func=lambda x: model_descriptions[x],
        help="Select the AI model that best fits your needs",
        label_visibility="collapsed"
    )
    st.session_state.model_name = selected_model
    
    st.markdown("---")
    
    # Advanced settings in expander
    with st.expander("🎛️ Advanced Settings", expanded=False):
        st.markdown("##### Temperature")
        st.caption("Controls response creativity and randomness")
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.1,
            help="Lower = More focused and deterministic\nHigher = More creative and varied",
            label_visibility="collapsed"
        )
        
        # Temperature indicator
        if st.session_state.temperature <= 0.3:
            st.info("🎯 Factual & Precise", icon="💡")
        elif st.session_state.temperature <= 0.6:
            st.info("⚖️ Balanced", icon="💡")
        else:
            st.info("🎨 Creative & Varied", icon="💡")
        
        st.markdown("##### Max Response Length")
        st.caption("Maximum tokens in AI response")
        st.session_state.max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=2000,
            step=100,
            help="Longer responses require more tokens",
            label_visibility="collapsed"
        )
        
        st.caption(f"~{st.session_state.max_tokens * 0.75:.0f} words maximum")
    
    st.markdown("---")
    
    # Session statistics
    st.subheader("📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Model", st.session_state.model_name.split('-')[1].upper())
    
    st.markdown("---")
    
    # Action buttons
    if st.button("🗑️ Clear Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.total_messages = 0
        st.rerun()

# Main chat interface

# Display current configuration
if st.session_state.api_key:
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-badge"><strong>Model:</strong> {st.session_state.model_name}</div>
            <div class="stat-badge"><strong>Temperature:</strong> {st.session_state.temperature}</div>
            <div class="stat-badge"><strong>Max Tokens:</strong> {st.session_state.max_tokens}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Check if API key is provided
if not st.session_state.api_key:
    # Empty state with better design
    st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🔐</div>
            <div class="empty-state-text">API Key Required</div>
            <div class="empty-state-subtext">Please enter your Kimi AI API key in the sidebar to start chatting</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **New to Kimi AI?** Visit [platform.moonshot.ai](https://platform.moonshot.ai) to create an account and get your API key.", icon="ℹ️")
    
    # Quick start guide
    with st.expander("🚀 Quick Start Guide"):
        st.markdown("""
        ### Get Started in 3 Steps:
        
        1. **Create Account**
           - Visit [platform.moonshot.ai](https://platform.moonshot.ai)
           - Sign up for a free account
        
        2. **Get API Key**
           - Navigate to API Keys section
           - Generate a new API key
           - Copy the key (starts with `sk-`)
        
        3. **Add Credits**
           - Go to billing section
           - Add minimum $1 credit
           - Start chatting!
        
        ### Need Help?
        - 📚 [Documentation](https://platform.moonshot.cn/docs)
        - 💬 [Community Forum](https://platform.moonshot.ai)
        - 📧 Support: support@moonshot.ai
        """)
else:
    # Initialize client
    client = initialize_openai_client(st.session_state.api_key)
    
    if client:
        # Display chat messages or empty state
        if len(st.session_state.messages) == 0:
            
            # Suggested prompts
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📝 Write an email", use_container_width=True):
                    st.session_state.suggested_prompt = "Help me write a professional email"
            
            with col2:
                if st.button("💻 Explain code", use_container_width=True):
                    st.session_state.suggested_prompt = "Explain what async/await means in programming"
            
            with col3:
                if st.button("🎨 Creative ideas", use_container_width=True):
                    st.session_state.suggested_prompt = "Give me creative project ideas"
        else:
            # Display chat history
            for message in st.session_state.messages:
                display_chat_message(message["role"], message["content"])
        
        # Chat input
        user_input = st.chat_input(
            "Type your message here..." if len(st.session_state.messages) > 0 else "Start your conversation...",
            key="user_input"
        )
        
        # Handle suggested prompts
        if 'suggested_prompt' in st.session_state:
            user_input = st.session_state.suggested_prompt
            del st.session_state.suggested_prompt
        
        if user_input:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.total_messages += 1
            
            # Get Kimi response with better loading state
            with st.spinner("🤖 Kimi AI is thinking..."):
                # Prepare messages for API
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
            st.session_state.total_messages += 1
            
            # Rerun to update the display
            st.rerun()
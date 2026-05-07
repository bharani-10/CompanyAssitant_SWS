"""
Streamlit frontend for the RAG chatbot
"""
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from typing import List, Dict
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SWS AI Company Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .chat-message {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4CAF50;
    }
    .source-box {
        background-color: #fff9c4;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .header-title {
        color: #4CAF50;
        font-weight: bold;
        font-size: 2.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# API configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_ready" not in st.session_state:
    st.session_state.api_ready = False


def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def query_chatbot(question: str) -> tuple[str, List[Dict]]:
    """Send question to API and get response"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"question": question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["answer"], data.get("sources", [])
        else:
            error_detail = response.json().get("detail", "Unknown error")
            return f"Error: {error_detail}", []
    
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again.", []
    except requests.exceptions.ConnectionError:
        return f"Error: Cannot connect to API at {API_URL}. Make sure the backend is running.", []
    except Exception as e:
        return f"Error: {str(e)}", []


def display_message(role: str, content: str, sources: List[Dict] = None):
    """Display a chat message"""
    message_class = "user-message" if role == "user" else "assistant-message"
    icon = "👤" if role == "user" else "🤖"
    
    st.markdown(f"""
        <div class="chat-message {message_class}">
            <strong>{icon} {role.capitalize()}:</strong><br/>
            {content}
        </div>
    """, unsafe_allow_html=True)
    
    # Display sources if available
    if sources and role == "assistant":
        with st.expander("📚 Sources Used"):
            for i, source in enumerate(sources, 1):
                st.markdown(f"""
                    <div class="source-box">
                        <strong>Source {i}: {source.get('source', 'Unknown')}</strong><br/>
                        <em>Page: {source.get('page', 'N/A')}</em><br/>
                        <small>{source.get('content', '')}</small>
                    </div>
                """, unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    st.markdown("### API Configuration")
    api_status = check_api_health()
    
    if api_status:
        st.success("✅ API Connected")
        st.session_state.api_ready = True
    else:
        st.error("❌ API Not Connected")
        st.warning(f"Cannot reach API at {API_URL}")
        st.session_state.api_ready = False
    
    st.markdown("---")
    
    st.markdown("### About")
    st.info(
        """
        **SWS AI Company Assistant**
        
        Ask questions about company policies including:
        - Leave & Time Off
        - HR Policies
        - IT Security
        - Code of Conduct
        - Benefits & Compensation
        - And more...
        
        Answers are sourced directly from company documents.
        """
    )
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Main content
st.markdown(
    '<p class="header-title">🤖 SWS AI Company Assistant</p>',
    unsafe_allow_html=True
)

st.markdown("""
---
Welcome to the **SWS AI Company Assistant**! Ask me anything about company policies, HR, IT security, benefits, and more. 
I'll search our company documents to provide accurate, grounded answers.

**Sample Questions to Try:**
- *What is the annual leave policy at SWS AI?*
- *How many days of sick leave do employees get?*
- *What is the notice period for resignation?*
- *What are the WFH guidelines?*
- *What health insurance benefits do we have?*
""")

st.markdown("---")

# Display chat history
st.markdown("### 💬 Conversation")

for message in st.session_state.messages:
    display_message(
        message["role"],
        message["content"],
        message.get("sources", [])
    )

# Input area
st.markdown("---")

col1, col2 = st.columns([0.9, 0.1])

with col1:
    user_input = st.text_input(
        "Ask about company policies...",
        placeholder="Type your question here",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    submit_button = st.button("📤 Send", use_container_width=True)

# Process user input
if submit_button and user_input:
    if not st.session_state.api_ready:
        st.error("❌ API is not connected. Please start the backend server.")
    else:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        display_message("user", user_input)
        
        # Get response from API
        with st.spinner("🔍 Searching documents and generating response..."):
            answer, sources = query_chatbot(user_input)
        
        # Add assistant message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })
        
        # Display assistant message with sources
        display_message("assistant", answer, sources)
        
        # Clear input
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9rem;">
    <p>💡 <strong>How it works:</strong> Your questions are searched against company documents using AI embeddings. 
    Answers are generated using an LLM and grounded in the actual documents.</p>
    <p>🔒 All answers are sourced from company policy documents only.</p>
</div>
""", unsafe_allow_html=True)

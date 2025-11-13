"""
Streamlit RAG Application with Amazon Kendra and AWS Bedrock
Main application entry point
"""

import streamlit as st
from utils.session_manager import initialize_session_state
from pages import home, chat, analytics, settings

# Page configuration
st.set_page_config(
    page_title="RAG Application - Kendra & Bedrock",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Sidebar navigation
with st.sidebar:
    st.title("🤖 RAG Application")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "💬 Chat", "📊 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    st.metric("Documents Uploaded", st.session_state.get('doc_count', 0))
    st.metric("Queries Made", st.session_state.get('query_count', 0))
    
    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("- Amazon Kendra")
    st.markdown("- AWS Bedrock")
    st.markdown("- Streamlit")

# Route to appropriate page
if page == "🏠 Home":
    home.render()
elif page == "💬 Chat":
    chat.render()
elif page == "📊 Analytics":
    analytics.render()
elif page == "⚙️ Settings":
    settings.render()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit")

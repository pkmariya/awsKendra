"""
Session state management for Streamlit application
"""
import streamlit as st
from datetime import datetime

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Configuration state
    if 'config_validated' not in st.session_state:
        st.session_state.config_validated = False
    
    # Document management
    if 'uploaded_documents' not in st.session_state:
        st.session_state.uploaded_documents = []
    
    if 'doc_count' not in st.session_state:
        st.session_state.doc_count = 0
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_conversation' not in st.session_state:
        st.session_state.current_conversation = []
    
    # Query tracking
    if 'query_count' not in st.session_state:
        st.session_state.query_count = 0
    
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    # Analytics data
    if 'analytics_data' not in st.session_state:
        st.session_state.analytics_data = {
            'queries': [],
            'confidence_scores': [],
            'response_times': [],
            'sources_used': [],
            'user_feedback': []
        }
    
    # AWS clients cache
    if 'kendra_client' not in st.session_state:
        st.session_state.kendra_client = None
    
    if 'bedrock_client' not in st.session_state:
        st.session_state.bedrock_client = None
    
    # UI state
    if 'show_sources' not in st.session_state:
        st.session_state.show_sources = True
    
    if 'streaming_enabled' not in st.session_state:
        st.session_state.streaming_enabled = True

def add_to_chat_history(role, content, sources=None, confidence=None):
    """Add a message to chat history"""
    message = {
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat(),
        'sources': sources or [],
        'confidence': confidence
    }
    st.session_state.chat_history.append(message)
    st.session_state.current_conversation.append(message)

def clear_chat_history():
    """Clear current conversation"""
    st.session_state.current_conversation = []

def increment_query_count():
    """Increment query counter"""
    st.session_state.query_count += 1

def add_uploaded_document(doc_info):
    """Add document to uploaded documents list"""
    st.session_state.uploaded_documents.append(doc_info)
    st.session_state.doc_count = len(st.session_state.uploaded_documents)

def record_analytics(query, confidence, response_time, sources, feedback=None):
    """Record analytics data"""
    st.session_state.analytics_data['queries'].append({
        'query': query,
        'timestamp': datetime.now().isoformat()
    })
    st.session_state.analytics_data['confidence_scores'].append(confidence)
    st.session_state.analytics_data['response_times'].append(response_time)
    st.session_state.analytics_data['sources_used'].extend(sources)
    
    if feedback:
        st.session_state.analytics_data['user_feedback'].append({
            'query': query,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        })

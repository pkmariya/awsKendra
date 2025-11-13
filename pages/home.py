"""
Home page - Document upload and management
"""
import streamlit as st
from utils.document_processor import DocumentProcessor
from utils.session_manager import add_uploaded_document
from services.kendra_service import KendraService
from config.config import Config
import time
def render():
    """Render the home page"""
    st.title("📤 Document Upload & Management")
    st.markdown("Upload your documents to enable intelligent search and Q&A")
    
    # Check configuration
    is_valid, message = Config.validate()
    if not is_valid:
        st.error(f"⚠️ Configuration Error: {message}")
        st.info("Please configure AWS credentials in the Settings page")
        return
    
    # File upload section
    st.markdown("### Upload Documents")
    st.markdown("Supported formats: PDF, TXT, DOCX, CSV, JSON")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['pdf', 'txt', 'docx', 'csv', 'json'],
        accept_multiple_files=True,
        help="Upload one or more documents to analyze"
    )
    
    if uploaded_files:
        process_uploaded_files(uploaded_files)
    
    # Display uploaded documents
    st.markdown("---")
    st.markdown("### Uploaded Documents")
    
    if st.session_state.uploaded_documents:
        display_uploaded_documents()
    else:
        st.info("No documents uploaded yet. Upload files above to get started.")
def process_uploaded_files(uploaded_files):
    """Process and validate uploaded files"""
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🚀 Process All", type="primary", use_container_width=True):
            process_files(uploaded_files)
def process_files(uploaded_files):
    """Process multiple uploaded files"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    processor = DocumentProcessor()
    kendra_service = KendraService()
    
    total_files = len(uploaded_files)
    successful = 0
    failed = 0
    
    for idx, uploaded_file in enumerate(uploaded_files):
        try:
            # Update progress
            progress = (idx + 1) / total_files
            progress_bar.progress(progress)
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # Validate file
            is_valid, error_msg = processor.validate_file(
                uploaded_file, 
                Config.MAX_FILE_SIZE_MB
            )
            
            if not is_valid:
                st.warning(f"❌ {uploaded_file.name}: {error_msg}")
                failed += 1
                continue
            
            # Process file
            text_content, metadata = processor.process_file(uploaded_file)
            
            # Chunk text for better retrieval
            chunks = processor.chunk_text(text_content)
            
            # Upload to Kendra (optional - depends on your Kendra setup)
            # kendra_service.index_document(uploaded_file.name, chunks, metadata)
            
            # Add to session state
            doc_info = {
                'filename': uploaded_file.name,
                'size': uploaded_file.size,
                'type': metadata['format'],
                'metadata': metadata,
                'content': text_content,
                'chunks': len(chunks),
                'timestamp': time.time()
            }
            
            add_uploaded_document(doc_info)
            successful += 1
            
            st.success(f"✅ {uploaded_file.name} processed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            failed += 1
    
    # Final status
    status_text.text(f"Completed: {successful} successful, {failed} failed")
    progress_bar.progress(1.0)
    
    if successful > 0:
        st.balloons()
        time.sleep(2)
        st.rerun()
def display_uploaded_documents():
    """Display list of uploaded documents"""
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", len(st.session_state.uploaded_documents))
    
    with col2:
        total_size = sum(doc['size'] for doc in st.session_state.uploaded_documents)
        st.metric("Total Size", f"{total_size / (1024*1024):.2f} MB")
    
    with col3:
        file_types = set(doc['type'] for doc in st.session_state.uploaded_documents)
        st.metric("File Types", len(file_types))
    
    with col4:
        total_chunks = sum(doc.get('chunks', 0) for doc in st.session_state.uploaded_documents)
        st.metric("Total Chunks", total_chunks)
    
    st.markdown("---")
    
    # Document list
    for idx, doc in enumerate(st.session_state.uploaded_documents):
        with st.expander(f"📄 {doc['filename']} ({doc['type']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**File Size:** {doc['size'] / 1024:.2f} KB")
                st.markdown(f"**Type:** {doc['type']}")
                st.markdown(f"**Chunks:** {doc.get('chunks', 0)}")
                
                # Display metadata
                if 'metadata' in doc:
                    st.markdown("**Metadata:**")
                    for key, value in doc['metadata'].items():
                        if key not in ['filename', 'file_size', 'file_type']:
                            st.text(f"  • {key}: {value}")
            
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{idx}"):
                    st.session_state.uploaded_documents.pop(idx)
                    st.session_state.doc_count = len(st.session_state.uploaded_documents)
                    st.rerun()
                
                if st.button("👁️ Preview", key=f"preview_{idx}"):
                    st.session_state[f'show_preview_{idx}'] = True
            
            # Show preview if requested
            if st.session_state.get(f'show_preview_{idx}', False):
                st.markdown("**Content Preview:**")
                preview_text = doc['content'][:500] + "..." if len(doc['content']) > 500 else doc['content']
                st.text_area("", preview_text, height=200, key=f"preview_text_{idx}")
                
                if st.button("Close Preview", key=f"close_preview_{idx}"):
                    st.session_state[f'show_preview_{idx}'] = False
                    st.rerun()
    
    # Clear all button
    st.markdown("---")
    if st.button("🗑️ Clear All Documents", type="secondary"):
        if st.session_state.uploaded_documents:
            st.session_state.uploaded_documents = []
            st.session_state.doc_count = 0
            st.rerun()
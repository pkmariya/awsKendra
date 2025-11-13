"""
Amazon Kendra Service for document indexing and semantic search
"""
import boto3
from typing import List, Dict, Optional
from config.config import Config
import streamlit as st

class KendraService:
    """Service class for Amazon Kendra operations"""
    
    def __init__(self):
        """Initialize Kendra client"""
        self.client = None
        self.index_id = Config.KENDRA_INDEX_ID
        
    def initialize_client(self, aws_credentials: Optional[Dict] = None):
        """Initialize Kendra client with credentials
        
        Args:
            aws_credentials: Dict with AWS credentials (optional)
        """
        try:
            if aws_credentials:
                self.client = boto3.client('kendra', **aws_credentials)
            else:
                self.client = boto3.client(
                    'kendra',
                    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                    region_name=Config.AWS_DEFAULT_REGION
                )
            return True, "Kendra client initialized successfully"
        except Exception as e:
            return False, f"Failed to initialize Kendra client: {str(e)}"
    
    def query(self, query_text: str, max_results: int = None) -> Dict:
        """Query Kendra index for relevant documents
        
        Args:
            query_text: The search query
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with query results
        """
        if not self.client:
            raise Exception("Kendra client not initialized. Call initialize_client() first.")
        
        if max_results is None:
            max_results = Config.KENDRA_MAX_RESULTS
        
        try:
            response = self.client.query(
                IndexId=self.index_id,
                QueryText=query_text,
                PageSize=max_results
            )
            
            # Process results
            results = {
                'query': query_text,
                'total_results': len(response.get('ResultItems', [])),
                'items': []
            }
            
            for item in response.get('ResultItems', []):
                result_item = {
                    'id': item.get('Id', ''),
                    'type': item.get('Type', ''),
                    'score': item.get('ScoreAttributes', {}).get('ScoreConfidence', 'UNKNOWN'),
                    'document_title': item.get('DocumentTitle', {}).get('Text', 'Untitled'),
                    'document_excerpt': item.get('DocumentExcerpt', {}).get('Text', ''),
                    'document_uri': item.get('DocumentURI', ''),
                    'attributes': item.get('DocumentAttributes', [])
                }  
                results['items'].append(result_item)
            
            return results
            
        except Exception as e:
            raise Exception(f"Kendra query failed: {str(e)}")
    
    def batch_put_document(self, documents: List[Dict]) -> Dict:
        """Batch upload documents to Kendra index
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Upload results
        """
        if not self.client:
            raise Exception("Kendra client not initialized. Call initialize_client() first.")
        
        try:
            response = self.client.batch_put_document(
                IndexId=self.index_id,
                Documents=documents
            )
            
            return {
                'success': True,
                'failed_documents': response.get('FailedDocuments', [])
            }
            
        except Exception as e:
            raise Exception(f"Batch document upload failed: {str(e)}")
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from Kendra index
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            Success status
        """
        if not self.client:
            raise Exception("Kendra client not initialized. Call initialize_client() first.")
        
        try:
            self.client.batch_delete_document(
                IndexId=self.index_id,
                DocumentIdList=[document_id]
            )
            return True
            
        except Exception as e:
            raise Exception(f"Document deletion failed: {str(e)}")
    
    def get_query_suggestions(self, query_text: str, max_suggestions: int = 5) -> List[str]:
        """Get query suggestions from Kendra
        
        Args:
            query_text: Partial query text
            max_suggestions: Maximum number of suggestions
            
        Returns:
            List of query suggestions
        """
        if not self.client:
            return []
        
        try:
            response = self.client.get_query_suggestions(
                IndexId=self.index_id,
                QueryText=query_text,
                MaxSuggestionsCount=max_suggestions
            )
            
            suggestions = [
                item.get('Value', {}).get('Text', {}).get('Text', '')
                for item in response.get('Suggestions', [])
            ]
            
            return suggestions
            
        except Exception as e:
            st.warning(f"Failed to get suggestions: {str(e)}")
            return []
    
    def describe_index(self) -> Dict:
        """Get information about the Kendra index
        
        Returns:
            Index information dictionary
        """
        if not self.client:
            raise Exception("Kendra client not initialized. Call initialize_client() first.")
        
        try:
            response = self.client.describe_index(
                Id=self.index_id
            )
            
            return {
                'name': response.get('Name', ''),
                'status': response.get('Status', ''),
                'description': response.get('Description', ''),
                'created_at': response.get('CreatedAt', ''),
                'updated_at': response.get('UpdatedAt', '')
            }
            
        except Exception as e:
            raise Exception(f"Failed to describe index: {str(e)}")
    
    @staticmethod
    def format_document_for_kendra(doc_id: str, title: str, content: str, 
                                   attributes: Optional[Dict] = None) -> Dict:
        """Format a document for Kendra ingestion
        
        Args:
            doc_id: Unique document ID
            title: Document title
            content: Document content
            attributes: Optional document attributes
            
        Returns:
            Formatted document dictionary
        """
        document = {
            'Id': doc_id,
            'Title': title,
            'Blob': content.encode('utf-8'),
            'ContentType': 'PLAIN_TEXT'
        }
        
        if attributes:
            document['Attributes'] = [
                {
                    'Key': key,
                    'Value': {'StringValue': str(value)}
                }
                for key, value in attributes.items()
            ]
        
        return document

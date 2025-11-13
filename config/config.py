"""
Configuration management for the RAG application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    # Amazon Kendra Configuration
    KENDRA_INDEX_ID = os.getenv('KENDRA_INDEX_ID', '')
    
    # AWS Bedrock Configuration
    BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
    BEDROCK_REGION = os.getenv('BEDROCK_REGION', 'us-east-1')
    
    # OpenAI Configuration (Fallback)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Application Settings
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 10))
    TEMP_UPLOAD_DIR = os.getenv('TEMP_UPLOAD_DIR', './temp_uploads')
    ANALYTICS_DB_PATH = os.getenv('ANALYTICS_DB_PATH', './data/analytics.db')
    
    # Supported file types
    SUPPORTED_FILE_TYPES = ['pdf', 'txt', 'docx', 'csv', 'json']
    
    # Kendra query configuration
    KENDRA_MAX_RESULTS = 5
    KENDRA_CONFIDENCE_THRESHOLD = 0.7
    
    # Bedrock configuration
    BEDROCK_MAX_TOKENS = 2048
    BEDROCK_TEMPERATURE = 0.7
    BEDROCK_TOP_P = 0.9
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_fields = [
            ('AWS_ACCESS_KEY_ID', cls.AWS_ACCESS_KEY_ID),
            ('AWS_SECRET_ACCESS_KEY', cls.AWS_SECRET_ACCESS_KEY),
            ('KENDRA_INDEX_ID', cls.KENDRA_INDEX_ID),
        ]
        
        missing_fields = [field for field, value in required_fields if not value]
        
        if missing_fields:
            return False, f"Missing required configuration: {', '.join(missing_fields)}"
        
        return True, "Configuration valid"
    
    @classmethod
    def get_aws_credentials(cls):
        """Get AWS credentials as dictionary"""
        return {
            'aws_access_key_id': cls.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': cls.AWS_SECRET_ACCESS_KEY,
            'region_name': cls.AWS_DEFAULT_REGION
        }

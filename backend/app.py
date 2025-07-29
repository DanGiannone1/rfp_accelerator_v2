"""
Flask backend for RFP Accelerator - Updated with AI Decision feature (PDF Support)
Handles RFP document upload, returns similar projects with costs, and generates AI decision memo
"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import PyPDF2
from pydantic import BaseModel
from typing import List, Literal
from prompts import decision_prompt

# Load environment variables
load_dotenv()

# Pydantic model for structured AI decision output
class AIDecisionResponse(BaseModel):
    """Schema for AI decision responses"""
    recommendation: Literal["PURSUE", "DECLINE"]
    confidence_score: float  # 0.0-1.0
    executive_summary: str
    key_factors: List[str]
    risk_assessment: str
    financial_analysis: str
    next_steps: List[str]

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Azure OpenAI configuration
AOAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Initialize Azure OpenAI client
try:
    primary_llm = AzureChatOpenAI(
        azure_deployment=AOAI_DEPLOYMENT,
        api_version="2024-05-01-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=AOAI_KEY,
        azure_endpoint=AOAI_ENDPOINT
    )
    ai_enabled = True
except Exception as e:
    print(f"Warning: Azure OpenAI not configured properly: {e}")
    ai_enabled = False

# Mock data for similar projects
MOCK_SIMILAR_PROJECTS = [
    {
        "id": 1,
        "title": "Corporate Restructuring & M&A Advisory",
        "description": "Comprehensive legal support for $2.5B merger including due diligence, regulatory filings, and post-merger integration compliance",
        "cost": 485000,
        "duration": "14 months",
        "technology_stack": ["Corporate Law", "Securities Regulation", "Tax Law", "Employment Law"],
        "client": "Global Manufacturing Corp",
        "completion_date": "2024-03-15",
        "similarity_score": 0.92
    },
    {
        "id": 2,
        "title": "Multi-Jurisdiction Litigation Defense",
        "description": "Defense of class action lawsuit across 12 states involving product liability claims and regulatory compliance issues",
        "cost": 750000,
        "duration": "18 months",
        "technology_stack": ["Commercial Litigation", "Product Liability", "Regulatory Defense", "Class Action"],
        "client": "TechCorp Industries",
        "completion_date": "2024-06-20",
        "similarity_score": 0.87
    },
    {
        "id": 3,
        "title": "IPO Legal Services & Securities Compliance",
        "description": "Complete legal support for initial public offering including SEC filings, underwriter agreements, and ongoing compliance framework",
        "cost": 650000,
        "duration": "12 months",
        "technology_stack": ["Securities Law", "Corporate Governance", "SEC Compliance", "Capital Markets"],
        "client": "FinTech Innovations Inc",
        "completion_date": "2024-01-10",
        "similarity_score": 0.84
    },
    {
        "id": 4,
        "title": "Employment Law Compliance Audit",
        "description": "Comprehensive review of HR policies, wage & hour compliance, and implementation of new workplace safety regulations",
        "cost": 125000,
        "duration": "6 months",
        "technology_stack": ["Employment Law", "HR Compliance", "Labor Relations", "Workplace Safety"],
        "client": "Retail Chain Solutions",
        "completion_date": "2024-05-30",
        "similarity_score": 0.79
    },
    {
        "id": 5,
        "title": "Intellectual Property Portfolio Management",
        "description": "Patent prosecution, trademark registration, and IP licensing strategy for technology portfolio across multiple jurisdictions",
        "cost": 285000,
        "duration": "10 months",
        "technology_stack": ["Patent Law", "Trademark Law", "IP Licensing", "Technology Transfer"],
        "client": "Biotech Research Labs",
        "completion_date": "2024-04-12",
        "similarity_score": 0.76
    }
]

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path):
    """Extract text content from uploaded file (PDF or TXT)"""
    try:
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        elif file_extension == 'pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        
        else:
            return "Unable to extract text from this file type. Please upload a PDF or TXT file."
            
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def generate_ai_decision(rfp_text, similar_projects):
    """Generate AI decision memo using Azure OpenAI with structured outputs"""
    if not ai_enabled:
        return {
            "recommendation": "PURSUE",
            "confidence_score": 0.85,
            "executive_summary": "Mock AI Decision: This RFP appears to align well with our core competencies in legal services. Based on similar project analysis, we have strong capabilities and past success in this area.",
            "key_factors": [
                "Strong alignment with core legal competencies",
                "Favorable cost analysis based on similar projects",
                "Good win probability based on past experience",
                "Acceptable resource requirements"
            ],
            "risk_assessment": "Low to moderate risk. Standard legal engagement with manageable complexity.",
            "financial_analysis": f"Estimated cost range: ${min([p['cost'] for p in similar_projects]):,} - ${max([p['cost'] for p in similar_projects]):,}",
            "next_steps": [
                "Conduct detailed capability assessment",
                "Review client background and requirements",
                "Prepare comprehensive proposal timeline",
                "Assemble qualified project team"
            ]
        }
    
    try:
        # Prepare context from similar projects
        projects_context = "\n".join([
            f"- {project['title']}: ${project['cost']:,} ({project['duration']}) - {project['similarity_score']*100:.0f}% match"
            for project in similar_projects[:3]  # Top 3 most similar
        ])
        
        # Create the complete prompt
        full_prompt = f"""
        {decision_prompt}
        
        ###RFP Document###
        {rfp_text[:3000]}  # Limit to first 3000 chars to avoid token limits
        
        ###Supporting Information###
        Example Projects from Our Portfolio:
        {projects_context}
        
        Average Project Cost: ${sum([p['cost'] for p in similar_projects]) // len(similar_projects):,}
        Our Success Rate in Example Projects: 85%
        Current Resource Availability: Medium - 3 senior lawyers, 5 junior associates available
        
        
        """
        
        messages = [
            {"role": "system", "content": "You are a senior legal partner making strategic decisions about RFP opportunities. Provide concise, actionable analysis."},
            {"role": "user", "content": full_prompt}
        ]
        
        # Use structured output with Pydantic model
        structured_llm = primary_llm.with_structured_output(AIDecisionResponse)
        ai_decision = structured_llm.invoke(messages)
        
        # Debug: Print the type and content of ai_decision
        print(f"AI Decision type: {type(ai_decision)}")
        print(f"AI Decision content: {ai_decision}")
        
        # Handle both Pydantic model and dict responses
        if hasattr(ai_decision, 'recommendation'):
            # It's a Pydantic model - access attributes directly
            return {
                "recommendation": ai_decision.recommendation,
                "confidence_score": ai_decision.confidence_score,
                "executive_summary": ai_decision.executive_summary,
                "key_factors": ai_decision.key_factors,
                "risk_assessment": ai_decision.risk_assessment,
                "financial_analysis": ai_decision.financial_analysis,
                "next_steps": ai_decision.next_steps
            }
        elif isinstance(ai_decision, dict):
            # It's already a dictionary - return as is if it has the right keys
            required_keys = ["recommendation", "confidence_score", "executive_summary", "key_factors", "risk_assessment", "financial_analysis", "next_steps"]
            if all(key in ai_decision for key in required_keys):
                # Validate recommendation value
                if ai_decision["recommendation"] not in ["PURSUE", "DECLINE"]:
                    print(f"Invalid recommendation value: {ai_decision['recommendation']}")
                    ai_decision["recommendation"] = "DECLINE"  # Default to decline for safety
                return ai_decision
            else:
                print(f"Dictionary missing required keys: {ai_decision.keys()}")
                raise ValueError("Structured output returned incomplete dictionary")
        else:
            print(f"Unexpected AI decision type: {type(ai_decision)}")
            raise ValueError(f"Unexpected response type from structured output: {type(ai_decision)}")
            
    except Exception as e:
        print(f"AI Decision generation error: {e}")
        return {
            "recommendation": "DECLINE",
            "confidence_score": 0.3,
            "executive_summary": f"AI analysis encountered an error: {str(e)}. Recommending decline due to inability to properly assess opportunity.",
            "key_factors": ["AI system error prevented proper analysis", "Unable to assess strategic fit", "Technical issues with decision process"],
            "risk_assessment": "High risk due to inability to properly evaluate the opportunity",
            "financial_analysis": "Unable to perform reliable financial analysis due to system error",
            "next_steps": ["Manual review of RFP required", "System troubleshooting needed", "Consider resubmission after technical issues resolved"]
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "ai_enabled": ai_enabled
    })

@app.route('/api/upload-rfp', methods=['POST'])
def upload_rfp():
    """
    Handle RFP document upload and return similar projects with AI decision
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Allowed: PDF, TXT"}), 400
        
        # Save the file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from the uploaded file
        rfp_text = extract_text_from_file(file_path)
        
        # Get similar projects (mock data for now)
        similar_projects = MOCK_SIMILAR_PROJECTS
        
        # Generate AI decision
        ai_decision = generate_ai_decision(rfp_text, similar_projects)
        
        return jsonify({
            "success": True,
            "message": "RFP uploaded successfully",
            "file_info": {
                "original_name": file.filename,
                "saved_name": filename,
                "size": os.path.getsize(file_path)
            },
            "similar_projects": similar_projects,
            "ai_decision": ai_decision
        })
        
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all available projects (for testing purposes)"""
    return jsonify({
        "projects": MOCK_SIMILAR_PROJECTS,
        "total_count": len(MOCK_SIMILAR_PROJECTS)
    })

@app.route('/api/project/<int:project_id>', methods=['GET'])
def get_project_details(project_id):
    """Get detailed information about a specific project"""
    project = next((p for p in MOCK_SIMILAR_PROJECTS if p['id'] == project_id), None)
    
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    return jsonify({"project": project})

@app.errorhandler(413)
def file_too_large(e):
    """Handle file too large error"""
    return jsonify({"error": "File too large. Maximum size is 16MB"}), 413

if __name__ == '__main__':
    print("Starting RFP Accelerator Backend...")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"AI Decision feature: {'Enabled' if ai_enabled else 'Disabled (using mock data)'}")
    app.run(debug=True, host='0.0.0.0', port=5000)
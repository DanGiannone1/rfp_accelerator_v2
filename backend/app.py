"""
Flask backend for RFP Accelerator - Basic demo version
Handles RFP document upload and returns similar projects with costs
"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock data for similar projects (will be replaced with actual backend logic)
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/upload-rfp', methods=['POST'])
def upload_rfp():
    """
    Handle RFP document upload and return similar projects
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
            return jsonify({"error": "Invalid file type. Allowed: txt, pdf, doc, docx"}), 400
        
        # Save the file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # TODO: In actual implementation, here we would:
        # 1. Extract text from the uploaded document
        # 2. Process the RFP content using Azure AI
        # 3. Search for similar projects using Azure Search
        # 4. Calculate similarity scores
        
        # For now, return mock similar projects
        similar_projects = MOCK_SIMILAR_PROJECTS
        
        return jsonify({
            "success": True,
            "message": "RFP uploaded successfully",
            "file_info": {
                "original_name": file.filename,
                "saved_name": filename,
                "size": os.path.getsize(file_path)
            },
            "similar_projects": similar_projects
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
    app.run(debug=True, host='0.0.0.0', port=5000)

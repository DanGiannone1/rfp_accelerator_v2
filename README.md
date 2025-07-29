# RFP Accelerator

A demo application for uploading RFP documents and finding similar projects with cost estimates.

## Project Structure

```
rfp_accelerator_v2/
├── backend/          # Python Flask API
│   ├── app.py       # Main Flask application
│   ├── test.py      # Azure integration test file
│   └── requirements.txt
└── frontend/         # React TypeScript application
    ├── src/
    │   ├── components/
    │   ├── types.ts
    │   └── App.tsx
    └── package.json
```

## Features

- 📁 **File Upload**: Drag & drop RFP documents (PDF, DOC, DOCX, TXT)
- 🔍 **Project Matching**: Find similar projects based on uploaded RFP
- 💰 **Cost Estimation**: View detailed cost information for similar projects
- 📊 **Analytics**: Cost analysis and project statistics
- 🎯 **Similarity Scoring**: Projects ranked by similarity percentage

## Quick Start

### Backend (Flask)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

   The backend will be available at `http://localhost:5000`

### Frontend (React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/upload-rfp` - Upload RFP document and get similar projects
- `GET /api/projects` - Get all available projects
- `GET /api/project/<id>` - Get specific project details

## Current Implementation

This is a **demo version** with mock data. The actual backend logic for document processing, AI analysis, and project matching will be implemented in future iterations.

### Mock Data Features:
- 5 sample projects with realistic cost ranges ($95k - $200k)
- Technology stacks (React, Python, Azure, etc.)
- Similarity scores and project details
- Client information and completion dates

## Future Enhancements

- Azure AI Document Intelligence integration
- Azure Cognitive Search for project matching
- OpenAI/Azure OpenAI for content analysis
- Real project database integration
- User authentication and project management
- Advanced filtering and search capabilities

## Technologies Used

### Backend:
- Python 3.12
- Flask
- Flask-CORS
- Azure SDK (ready for integration)

### Frontend:
- React 18
- TypeScript
- Axios for API calls
- React Dropzone for file uploads
- CSS3 with modern styling

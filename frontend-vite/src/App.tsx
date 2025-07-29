import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ExecutiveMemo from './components/ExecutiveMemo';
import ProjectList from './components/ProjectList';
import type { Project, AIDecision } from './types';

function App() {
  const [similarProjects, setSimilarProjects] = useState<Project[]>([]);
  const [aiDecision, setAiDecision] = useState<AIDecision | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);

  const handleUploadSuccess = (projects: Project[], fileName: string, decision: AIDecision) => {
    setSimilarProjects(projects);
    setAiDecision(decision);
    setUploadedFile(fileName);
    setIsLoading(false);
  };

  const handleUploadStart = () => {
    setIsLoading(true);
    setSimilarProjects([]);
    setAiDecision(null);
    setUploadedFile(null);
  };

  const handleUploadError = () => {
    setIsLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>RFP Accelerator</h1>
        <p>Upload your RFP document to get AI-powered analysis and find similar projects with cost estimates</p>
      </header>
      
      <main className="App-main">
        <div className="upload-section">
          <FileUpload 
            onUploadStart={handleUploadStart}
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
            isLoading={isLoading}
          />
        </div>

        {uploadedFile && (
          <div className="upload-status">
            <p>✅ Successfully uploaded: <strong>{uploadedFile}</strong></p>
          </div>
        )}

        {isLoading && (
          <div className="loading">
            <p>🤖 Analyzing your RFP with AI and finding similar projects...</p>
          </div>
        )}

        {aiDecision && uploadedFile && (
          <div className="ai-decision-section">
            <ExecutiveMemo aiDecision={aiDecision} fileName={uploadedFile} />
          </div>
        )}

        {similarProjects.length > 0 && (
          <div className="results-section">
            <h2>📊 Similar Projects Analysis</h2>
            <ProjectList projects={similarProjects} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
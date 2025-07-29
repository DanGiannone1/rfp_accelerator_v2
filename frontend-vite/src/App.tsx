import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ProjectList from './components/ProjectList';
import type { Project } from './types';

function App() {
  const [similarProjects, setSimilarProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);

  const handleUploadSuccess = (projects: Project[], fileName: string) => {
    setSimilarProjects(projects);
    setUploadedFile(fileName);
    setIsLoading(false);
  };

  const handleUploadStart = () => {
    setIsLoading(true);
    setSimilarProjects([]);
    setUploadedFile(null);
  };

  const handleUploadError = () => {
    setIsLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>RFP Accelerator</h1>
        <p>Upload your RFP document to find similar projects and cost estimates</p>
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
            <p>🔍 Analyzing your RFP and finding similar projects...</p>
          </div>
        )}

        {similarProjects.length > 0 && (
          <div className="results-section">
            <h2>Similar Projects Found</h2>
            <ProjectList projects={similarProjects} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

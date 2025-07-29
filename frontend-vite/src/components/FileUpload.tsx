import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import type { Project, UploadResponse, ApiError } from '../types';
import './FileUpload.css';

interface FileUploadProps {
  onUploadStart: () => void;
  onUploadSuccess: (projects: Project[], fileName: string) => void;
  onUploadError: () => void;
  isLoading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onUploadStart,
  onUploadSuccess,
  onUploadError,
  isLoading
}) => {
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append('file', file);

    onUploadStart();

    try {
      const response = await axios.post<UploadResponse>(
        'http://localhost:5000/api/upload-rfp',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (response.data.success) {
        onUploadSuccess(response.data.similar_projects, response.data.file_info.original_name);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      onUploadError();
      
      if (axios.isAxiosError(error) && error.response) {
        const errorData = error.response.data as ApiError;
        alert(`Upload failed: ${errorData.error || 'Unknown error'}`);
      } else {
        alert('Upload failed. Please make sure the backend server is running.');
      }
    }
  }, [onUploadStart, onUploadSuccess, onUploadError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    multiple: false,
    disabled: isLoading
  });

  return (
    <div className="file-upload">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''} ${isLoading ? 'disabled' : ''}`}
      >
        <input {...getInputProps()} />
        {isLoading ? (
          <div className="upload-content">
            <div className="spinner"></div>
            <p>Processing your RFP...</p>
          </div>
        ) : isDragActive ? (
          <div className="upload-content">
            <p>📁 Drop the RFP document here...</p>
          </div>
        ) : (
          <div className="upload-content">
            <div className="upload-icon">📄</div>
            <h3>Upload RFP Document</h3>
            <p>Drag & drop your RFP document here, or click to select</p>
            <p className="file-types">Supported formats: PDF, DOC, DOCX, TXT</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;

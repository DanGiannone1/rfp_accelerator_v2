import React from 'react';
import type { Project } from '../types';
import './ProjectCard.css';

interface ProjectCardProps {
  project: Project;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.9) return '#4CAF50'; // Green
    if (score >= 0.8) return '#FF9800'; // Orange
    return '#f44336'; // Red
  };

  const getScoreLabel = (score: number) => {
    if (score >= 0.9) return 'Excellent Match';
    if (score >= 0.8) return 'Good Match';
    return 'Fair Match';
  };

  return (
    <div className="project-card">
      <div className="project-header">
        <h3 className="project-title">{project.title}</h3>
        <div 
          className="similarity-badge"
          style={{ backgroundColor: getScoreColor(project.similarity_score) }}
        >
          {Math.round(project.similarity_score * 100)}% Match
        </div>
      </div>

      <p className="project-description">{project.description}</p>

      <div className="project-details">
        <div className="detail-row">
          <span className="detail-label">💰 Cost:</span>
          <span className="detail-value cost-highlight">
            ${project.cost.toLocaleString()}
          </span>
        </div>

        <div className="detail-row">
          <span className="detail-label">⏱️ Duration:</span>
          <span className="detail-value">{project.duration}</span>
        </div>

        <div className="detail-row">
          <span className="detail-label">🏢 Client:</span>
          <span className="detail-value">{project.client}</span>
        </div>

        <div className="detail-row">
          <span className="detail-label">📅 Completed:</span>
          <span className="detail-value">{formatDate(project.completion_date)}</span>
        </div>

        <div className="detail-row">
          <span className="detail-label">🔗 Similarity:</span>
          <span className="detail-value" style={{ color: getScoreColor(project.similarity_score) }}>
            {getScoreLabel(project.similarity_score)}
          </span>
        </div>
      </div>

      <div className="technology-stack">
        <span className="tech-label">⚖️ Legal Services:</span>
        <div className="tech-tags">
          {project.technology_stack.map((tech, index) => (
            <span key={index} className="tech-tag">
              {tech}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;

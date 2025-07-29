import React from 'react';
import type { Project } from '../types';
import ProjectCard from './ProjectCard';
import './ProjectList.css';

interface ProjectListProps {
  projects: Project[];
}

const ProjectList: React.FC<ProjectListProps> = ({ projects }) => {
  const totalEstimatedCost = projects.reduce((sum, project) => sum + project.cost, 0);
  const averageCost = totalEstimatedCost / projects.length;

  return (
    <div className="project-list">
      <div className="project-summary">
        <div className="summary-card">
          <h3>📊 Cost Analysis</h3>
          <div className="cost-stats">
            <div className="cost-item">
              <span className="label">Projects Found:</span>
              <span className="value">{projects.length}</span>
            </div>
            <div className="cost-item">
              <span className="label">Average Cost:</span>
              <span className="value cost">${averageCost.toLocaleString()}</span>
            </div>
            <div className="cost-item">
              <span className="label">Cost Range:</span>
              <span className="value cost">
                ${Math.min(...projects.map(p => p.cost)).toLocaleString()} - 
                ${Math.max(...projects.map(p => p.cost)).toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="projects-grid">
        {projects
          .sort((a, b) => b.similarity_score - a.similarity_score)
          .map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
      </div>
    </div>
  );
};

export default ProjectList;

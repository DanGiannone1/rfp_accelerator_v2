export interface Project {
  id: number;
  title: string;
  description: string;
  cost: number;
  duration: string;
  technology_stack: string[];
  client: string;
  completion_date: string;
  similarity_score: number;
}

export interface AIDecision {
  recommendation: 'PURSUE' | 'DECLINE' | 'REVIEW_REQUIRED';
  confidence_score: number;
  executive_summary: string;
  key_factors: string[];
  risk_assessment: string;
  financial_analysis: string;
  next_steps: string[];
}

export interface UploadResponse {
  success: boolean;
  message: string;
  file_info: {
    original_name: string;
    saved_name: string;
    size: number;
  };
  similar_projects: Project[];
  ai_decision: AIDecision;
}

export interface ApiError {
  error: string;
}
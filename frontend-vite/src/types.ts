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

export interface UploadResponse {
  success: boolean;
  message: string;
  file_info: {
    original_name: string;
    saved_name: string;
    size: number;
  };
  similar_projects: Project[];
}

export interface ApiError {
  error: string;
}

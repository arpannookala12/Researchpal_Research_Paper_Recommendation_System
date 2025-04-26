import axios from 'axios';

// Create an Axios instance with base URL from environment
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Paper interface
export interface Paper {
  id: string;
  title: string;
  abstract: string;
  authors: string[];
  categories: string;
  comments?: string;
  update_date?: string;
  created_at: string;
  updated_at: string;
}

// Recommendation interface
export interface Recommendation {
  id: string;
  source_paper: string;
  recommended_paper: string;
  recommended_paper_details: Paper;
  similarity_score: number;
  recommendation_date: string;
  model_name: string;
}

// Explanation API
export const explanationService = {
    // Get explanation for a recommendation
    async getExplanation(sourcePaperId: string, recommendedPaperId: string) {
      const response = await api.post<{ explanation: string }>('/rag/explain_recommendation/', {
        source_paper_id: sourcePaperId,
        recommended_paper_id: recommendedPaperId
      });
      return response.data.explanation;
    }
  };

// Paper API service
export const paperService = {
  // Get all papers with optional filtering
  async getPapers(params: { page?: number; category?: string; search?: string } = {}) {
    const response = await api.get<{ count: number; results: Paper[] }>('/papers/', { params });
    return response.data;
  },
  
  // Get a single paper by ID
  async getPaper(id: string) {
    const response = await api.get<Paper>(\`/papers/\${id}/\`);
    return response.data;
  },
  
  // Get recommendations for a paper
  async getRecommendations(id: string) {
    const response = await api.get<Recommendation[]>(\`/papers/\${id}/recommendations/\`);
    return response.data;
  },
  
  // Search for papers
  async searchPapers(query: string) {
    const response = await api.get<Paper[]>('/papers/search/', { params: { q: query } });
    return response.data;
  },
};

export default api;
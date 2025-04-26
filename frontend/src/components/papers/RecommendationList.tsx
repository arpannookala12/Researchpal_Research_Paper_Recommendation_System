import React, { useState } from 'react';
import { Recommendation, Paper, explanationService } from '@/services/api';
import PaperCard from './PaperCard';
import ExplanationModal from './ExplanationModal';

interface RecommendationListProps {
  recommendations: Recommendation[];
  isLoading: boolean;
  sourcePaperId: string;
}

const RecommendationList: React.FC<RecommendationListProps> = ({ 
  recommendations, 
  isLoading,
  sourcePaperId
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedPaper, setSelectedPaper] = useState<Paper | null>(null);
  const [explanation, setExplanation] = useState<string | null>(null);
  const [isExplaining, setIsExplaining] = useState(false);
  
  const handleExplain = async (paper: Paper) => {
    setSelectedPaper(paper);
    setIsModalOpen(true);
    setIsExplaining(true);
    setExplanation(null);
    
    try {
      const explanationText = await explanationService.getExplanation(
        sourcePaperId,
        paper.id
      );
      setExplanation(explanationText);
    } catch (error) {
      console.error('Error fetching explanation:', error);
      setExplanation('Failed to load explanation. Please try again later.');
    } finally {
      setIsExplaining(false);
    }
  };
  
  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-40 bg-gray-200 rounded-lg"></div>
          </div>
        ))}
      </div>
    );
  }
  
  if (recommendations.length === 0) {
    return (
      <div className="rounded-lg border border-gray-200 p-6 text-center">
        <p className="text-gray-500">No recommendations found for this paper.</p>
      </div>
    );
  }
  
  // Get source paper from the first recommendation if available
  const sourcePaper = recommendations.length > 0 
    ? { id: sourcePaperId, title: 'Source Paper' } as Paper
    : null;
  
  return (
    <>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {recommendations.map((recommendation) => (
          <PaperCard
            key={recommendation.id}
            paper={recommendation.recommended_paper_details}
            similarityScore={recommendation.similarity_score}
            sourcePaperId={sourcePaperId}
            onExplain={handleExplain}
            showExplainButton={true}
          />
        ))}
      </div>
      
      <ExplanationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        sourcePaper={sourcePaper}
        recommendedPaper={selectedPaper}
        explanation={explanation}
        isLoading={isExplaining}
      />
    </>
  );
};

export default RecommendationList;
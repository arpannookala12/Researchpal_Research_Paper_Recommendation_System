import React from 'react';
import Link from 'next/link';
import { Paper } from '@/services/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';

interface PaperCardProps {
  paper: Paper;
  similarityScore?: number;
  sourcePaperId?: string;
  onExplain?: (paper: Paper) => void;
  showExplainButton?: boolean;
}
const PaperCard: React.FC<PaperCardProps> = ({ 
    paper, 
    similarityScore,
    sourcePaperId,
    onExplain,
    showExplainButton = false
  }) => {
    // Truncate abstract for display
    const truncatedAbstract = paper.abstract.length > 200 
      ? `${paper.abstract.substring(0, 200)}...` 
      : paper.abstract;
    
    return (
      <Card className="h-full transition-shadow hover:shadow-md">
        <Card.Header>
          <Link href={`/papers/${paper.id}`} className="block">
            <h3 className="text-lg font-semibold text-gray-900 hover:text-blue-600">{paper.title}</h3>
          </Link>
          <div className="mt-1 flex flex-wrap items-center text-sm text-gray-500">
            <span className="mr-2 mt-1 rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">
              {paper.categories}
            </span>
            {similarityScore !== undefined && (
              <span className="mr-2 mt-1 rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800">
                Similarity: {(similarityScore * 100).toFixed(1)}%
              </span>
            )}
            {paper.update_date && (
              <span className="mt-1 text-xs text-gray-500">
                Updated: {new Date(paper.update_date).toLocaleDateString()}
              </span>
            )}
          </div>
        </Card.Header>
        <Card.Body>
          <p className="text-sm text-gray-600">{truncatedAbstract}</p>
          <div className="mt-3">
            <p className="text-xs text-gray-500">
              Authors: {Array.isArray(paper.authors) ? paper.authors.join(', ') : paper.authors}
            </p>
          </div>
        </Card.Body>
        <Card.Footer className="flex justify-between items-center">
          <Link href={`/papers/${paper.id}`} className="text-sm font-medium text-blue-600 hover:text-blue-800">
            View details →
          </Link>
          
          {showExplainButton && onExplain && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={(e) => {
                e.preventDefault();
                onExplain(paper);
              }}
            >
              Explain
            </Button>
          )}
        </Card.Footer>
      </Card>
    );
  };
  
  export default PaperCard;
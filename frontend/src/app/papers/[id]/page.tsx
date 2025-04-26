"use client";

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { paperService, Paper, Recommendation } from '@/services/api';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import RecommendationList from '@/components/papers/RecommendationList';

export default function PaperDetail() {
  const params = useParams();
  const paperId = params?.id as string;
  
  const [paper, setPaper] = useState<Paper | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchPaperAndRecommendations = async () => {
      if (!paperId) return;
      
      try {
        setLoading(true);
        
        // Fetch paper details
        const paperData = await paperService.getPaper(paperId);
        setPaper(paperData);
        
        // Fetch recommendations
        const recommendationsData = await paperService.getRecommendations(paperId);
        setRecommendations(recommendationsData);
        
        setError(null);
      } catch (err) {
        console.error('Error fetching paper details:', err);
        setError('Failed to load paper details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchPaperAndRecommendations();
  }, [paperId]);
  
  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse space-y-6">
          <div className="h-10 w-3/4 bg-gray-200 rounded"></div>
          <div className="h-4 w-1/4 bg-gray-200 rounded"></div>
          <div className="h-40 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }
  
  if (error || !paper) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
          {error || 'Paper not found'}
        </div>
      </div>
    );
  }
  
  return (
    <main className="container mx-auto px-4 py-8">
      <Button
        variant="outline"
        size="sm"
        className="mb-6"
        onClick={() => window.history.back()}
      >
        ← Back
      </Button>
      
      <Card className="mb-8">
        <Card.Header>
          <h1 className="text-2xl font-bold text-gray-900">{paper.title}</h1>
          <div className="mt-2 flex flex-wrap items-center text-sm text-gray-500">
            <span className="mr-2 mt-1 rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">
              {paper.categories}
            </span>
            {paper.update_date && (
              <span className="mt-1 text-xs text-gray-500">
                Updated: {new Date(paper.update_date).toLocaleDateString()}
              </span>
            )}
          </div>
        </Card.Header>
        <Card.Body>
          <div className="mb-4">
            <h2 className="mb-2 text-lg font-medium">Abstract</h2>
            <p className="text-gray-700 whitespace-pre-line">{paper.abstract}</p>
          </div>
          
          <div className="mb-4">
            <h2 className="mb-2 text-lg font-medium">Authors</h2>
            <p className="text-gray-700">
              {Array.isArray(paper.authors) ? paper.authors.join(', ') : paper.authors}
            </p>
          </div>
          
          {paper.comments && (
            <div>
              <h2 className="mb-2 text-lg font-medium">Comments</h2>
              <p className="text-gray-700">{paper.comments}</p>
            </div>
          )}
        </Card.Body>
      </Card>
      
      <section className="mb-8">
        <h2 className="mb-6 text-2xl font-bold">Similar Papers</h2>
        <RecommendationList 
          recommendations={recommendations} 
          isLoading={loading}
          sourcePaperId={paper.id}
        />
      </section>
    </main>
  );
}
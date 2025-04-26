"use client";

import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { paperService, Paper } from '@/services/api';
import PaperCard from '@/components/papers/PaperCard';
import SearchBar from '@/components/papers/SearchBar';
import Button from '@/components/ui/Button';

export default function Search() {
  const searchParams = useSearchParams();
  const query = searchParams?.get('q') || '';
  
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const searchPapers = async () => {
      if (!query) {
        setPapers([]);
        setLoading(false);
        return;
      }
      
      try {
        setLoading(true);
        const results = await paperService.searchPapers(query);
        setPapers(results);
        setError(null);
      } catch (err) {
        console.error('Error searching papers:', err);
        setError('Failed to search papers. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    searchPapers();
  }, [query]);
  
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="mb-4 text-2xl font-bold">Search Results</h1>
        <SearchBar />
      </div>
      
      {query && (
        <div className="mb-6">
          <p className="text-gray-600">
            Showing results for: <span className="font-medium">{query}</span>
          </p>
        </div>
      )}
      
      {loading && (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="animate-pulse rounded-lg border border-gray-200 p-6">
              <div className="h-6 w-3/4 bg-gray-200 rounded mb-4"></div>
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 w-1/2 bg-gray-200 rounded"></div>
            </div>
          ))}
        </div>
      )}
      
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      )}
      
      {!loading && !error && papers.length === 0 && (
        <div className="rounded-lg border border-gray-200 bg-gray-50 p-6 text-center">
          <p className="text-gray-500">
            {query
              ? `No papers found matching "${query}". Please try a different search term.`
              : 'Please enter a search term to find papers.'}
          </p>
        </div>
      )}
      
      {!loading && !error && papers.length > 0 && (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {papers.map((paper) => (
            <PaperCard key={paper.id} paper={paper} />
          ))}
        </div>
      )}
      
      <div className="mt-8 flex justify-center">
        <Button
          variant="outline"
          size="sm"
          onClick={() => window.history.back()}
        >
          ← Back
        </Button>
      </div>
    </main>
  );
}
"use client";

import React, { useEffect, useState } from 'react';
import { paperService, Paper } from '@/services/api';
import PaperCard from '@/components/papers/PaperCard';
import SearchBar from '@/components/papers/SearchBar';
import Button from '@/components/ui/Button';

export default function Home() {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  
  useEffect(() => {
    const fetchPapers = async () => {
      try {
        setLoading(true);
        const res = await paperService.getPapers({ page });
        setPapers(res.results);
        setTotalPages(Math.ceil(res.count / 10)); // Assuming 10 items per page
        setError(null);
      } catch (err) {
        console.error('Error fetching papers:', err);
        setError('Failed to load papers. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchPapers();
  }, [page]);
  
  return (
    <main className="container mx-auto px-4 py-8">
      <section className="mb-12 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 p-8 text-white">
        <div className="mx-auto max-w-3xl text-center">
          <h1 className="mb-4 text-4xl font-bold">Research Paper Recommendation System</h1>
          <p className="mb-6 text-lg">
            Discover relevant academic papers based on advanced semantic similarity
          </p>
          <div className="mx-auto max-w-lg">
            <SearchBar />
          </div>
        </div>
      </section>
      
      <section className="mb-8">
        <h2 className="mb-6 text-2xl font-bold">Recent Papers</h2>
        
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
      
      {!loading && !error && (
        <>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {papers.map((paper) => (
              <PaperCard key={paper.id} paper={paper} />
            ))}
          </div>
          
          <div className="mt-8 flex justify-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              disabled={page === 1}
            >
              Previous
            </Button>
            <span className="mx-2 flex items-center text-sm text-gray-600">
              Page {page} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              disabled={page === totalPages}
            >
              Next
            </Button>
          </div>
        </>
      )}
    </section>
  </main>
);
}
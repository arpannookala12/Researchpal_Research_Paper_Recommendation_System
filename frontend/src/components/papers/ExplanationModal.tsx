import React from 'react';
import { Paper } from '@/services/api';

interface ExplanationModalProps {
  isOpen: boolean;
  onClose: () => void;
  sourcePaper: Paper | null;
  recommendedPaper: Paper | null;
  explanation: string | null;
  isLoading: boolean;
}

const ExplanationModal: React.FC<ExplanationModalProps> = ({
  isOpen,
  onClose,
  sourcePaper,
  recommendedPaper,
  explanation,
  isLoading
}) => {
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
      <div className="relative w-full max-w-2xl max-h-[80vh] overflow-hidden rounded-lg bg-white shadow-xl">
        {/* Header */}
        <div className="sticky top-0 z-10 flex items-center justify-between border-b border-gray-200 bg-white p-4">
          <h3 className="text-lg font-medium text-gray-900">
            Why This Paper Is Recommended
          </h3>
          <button
            type="button"
            className="text-gray-400 hover:text-gray-500"
            onClick={onClose}
          >
            <span className="sr-only">Close</span>
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        {/* Body */}
        <div className="overflow-y-auto p-4 max-h-[calc(80vh-8rem)]">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <svg className="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
          ) : (
            <>
              {sourcePaper && recommendedPaper && (
                <div className="mb-4">
                  <div className="mb-2">
                    <h4 className="text-sm font-medium text-gray-500">From Paper</h4>
                    <p className="text-gray-900 font-medium">{sourcePaper.title}</p>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Recommended Paper</h4>
                    <p className="text-gray-900 font-medium">{recommendedPaper.title}</p>
                  </div>
                </div>
              )}
              
              {explanation ? (
                <div className="prose max-w-none">
                  <h4 className="text-base font-medium text-gray-900">Explanation</h4>
                  <div className="mt-2 text-gray-700 whitespace-pre-line">
                    {explanation}
                  </div>
                </div>
              ) : (
                <div className="rounded-md bg-yellow-50 p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-yellow-700">
                        No explanation available for this recommendation. This usually happens when one of the papers could not be found.
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
        
        {/* Footer */}
        <div className="border-t border-gray-200 p-4">
          <button
            type="button"
            className="w-full rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExplanationModal;
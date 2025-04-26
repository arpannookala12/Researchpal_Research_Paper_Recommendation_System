import React from 'react';
import Link from 'next/link';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Research Paper Recommendation System',
  description: 'Discover relevant academic papers based on advanced semantic similarity',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <header className="bg-white shadow">
          <div className="container mx-auto px-4 py-4">
            <nav className="flex items-center justify-between">
              <Link href="/" className="text-xl font-bold text-blue-600">
                Paper Recommender
              </Link>
              <div className="space-x-4">
                <Link href="/" className="text-gray-600 hover:text-blue-600">
                  Home
                </Link>
                <Link href="/search" className="text-gray-600 hover:text-blue-600">
                  Search
                </Link>
              </div>
            </nav>
          </div>
        </header>
        
        {children}
        
        <footer className="bg-gray-100 mt-auto">
          <div className="container mx-auto px-4 py-8">
            <div className="text-center text-gray-500 text-sm">
              <p>Research Paper Recommendation System</p>
              <p className="mt-1">Built with Next.js, Django, and LanceDB</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
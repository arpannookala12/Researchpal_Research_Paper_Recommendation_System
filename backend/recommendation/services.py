import os
import numpy as np
import lancedb
from sentence_transformers import SentenceTransformer
from django.conf import settings
from core.models import Paper, Recommendation
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service for generating paper recommendations."""
    
    def __init__(self, model_name="allenai-specter"):
        """Initialize with the specified model."""
        self.model_name = model_name
        self.embedding_model = SentenceTransformer(model_name)
        
        # Connect to LanceDB
        self.db = lancedb.connect(settings.LANCEDB_PATH)
        self.table_name = "research_papers"
        
        # Check if table exists
        if self.table_name not in self.db.table_names():
            logger.error(f"Table {self.table_name} does not exist in LanceDB")
        else:
            self.table = self.db.open_table(self.table_name)
    
    def generate_embedding(self, text):
        """Generate embedding for a given text."""
        return self.embedding_model.encode(text)
    
    def get_similar_papers(self, paper_id, top_k=10):
        """Get similar papers for a given paper ID."""
        try:
            # Get the paper
            paper = Paper.objects.get(id=paper_id)
            
            # Generate embedding for the paper's abstract
            embedding = self.generate_embedding(paper.abstract)
            
            # Search for similar papers in LanceDB
            results = self.table.search(embedding).metric("cosine").limit(top_k + 1).to_pandas()
            
            # Filter out the query paper itself
            results = results[results['id'] != paper_id]
            
            # Create recommendations in the database
            recommendations = []
            for _, row in results.iterrows():
                try:
                    recommended_paper = Paper.objects.get(id=row['id'])
                    
                    # Create or update recommendation
                    recommendation, created = Recommendation.objects.update_or_create(
                        source_paper=paper,
                        recommended_paper=recommended_paper,
                        model_name=self.model_name,
                        defaults={'similarity_score': 1 - row['_distance']}
                    )
                    
                    recommendations.append(recommendation)
                except Paper.DoesNotExist:
                    logger.warning(f"Paper {row['id']} not found in database")
            
            return recommendations
        
        except Paper.DoesNotExist:
            logger.error(f"Paper {paper_id} not found")
            return []
        
        except Exception as e:
            logger.error(f"Error getting similar papers: {str(e)}")
            return []
    
    def search_papers(self, query, top_k=10):
        """Search for papers based on a query string."""
        try:
            # Generate embedding for the query
            embedding = self.generate_embedding(query)
            
            # Search for similar papers in LanceDB
            results = self.table.search(embedding).metric("cosine").limit(top_k).to_pandas()
            
            # Get paper objects
            paper_ids = results['id'].tolist()
            papers = list(Paper.objects.filter(id__in=paper_ids))
            
            # Sort papers by similarity score
            papers_dict = {str(paper.id): paper for paper in papers}
            sorted_papers = [papers_dict[pid] if pid in papers_dict else None for pid in paper_ids]
            sorted_papers = [p for p in sorted_papers if p is not None]
            
            return sorted_papers
        
        except Exception as e:
            logger.error(f"Error searching papers: {str(e)}")
            return []
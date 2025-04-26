import logging
from sentence_transformers import SentenceTransformer
import lancedb
from django.conf import settings
from core.models import Paper
import numpy as np

logger = logging.getLogger(__name__)

class ContextRetrievalService:
    """Service for retrieving context for RAG."""
    
    def __init__(self, model_name="allenai-specter"):
        """Initialize the context retrieval service."""
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
    
    def get_relevant_papers(self, query_text, k=5):
        """Get relevant papers for a query."""
        try:
            # Generate embedding for the query
            embedding = self.embedding_model.encode(query_text)
            
            # Search for similar papers in LanceDB
            results = self.table.search(embedding).metric("cosine").limit(k).to_pandas()
            
            # Get paper objects
            paper_ids = results['id'].tolist()
            papers = list(Paper.objects.filter(id__in=paper_ids))
            
            # Sort papers by similarity
            papers_dict = {str(paper.id): paper for paper in papers}
            sorted_papers = [papers_dict[pid] if pid in papers_dict else None for pid in paper_ids]
            sorted_papers = [p for p in sorted_papers if p is not None]
            
            return sorted_papers
        
        except Exception as e:
            logger.error(f"Error getting relevant papers: {str(e)}")
            return []
    
    def build_context_for_papers(self, paper1, paper2):
        """Build context for explaining the relationship between two papers."""
        try:
            # Get both papers
            if isinstance(paper1, str):
                paper1 = Paper.objects.get(id=paper1)
            if isinstance(paper2, str):
                paper2 = Paper.objects.get(id=paper2)
            
            # Get query text combining both papers
            query_text = f"{paper1.title} {paper1.abstract} {paper2.title} {paper2.abstract}"
            
            # Get related papers (excluding the input papers)
            related_papers = self.get_relevant_papers(query_text, k=3)
            related_papers = [p for p in related_papers 
                            if str(p.id) != str(paper1.id) and str(p.id) != str(paper2.id)]
            
            # Build context
            context = f"""
            Paper 1: {paper1.title}
            Authors: {', '.join(paper1.authors) if isinstance(paper1.authors, list) else paper1.authors}
            Categories: {paper1.categories}
            Abstract: {paper1.abstract}
            
            Paper 2: {paper2.title}
            Authors: {', '.join(paper2.authors) if isinstance(paper2.authors, list) else paper2.authors}
            Categories: {paper2.categories}
            Abstract: {paper2.abstract}
            """
            
            # Add related papers for additional context
            if related_papers:
                context += "\n\nRelated Papers:\n"
                for i, paper in enumerate(related_papers, 1):
                    context += f"""
                    Related Paper {i}: {paper.title}
                    Authors: {', '.join(paper.authors) if isinstance(paper.authors, list) else paper.authors}
                    Categories: {paper.categories}
                    Abstract: {paper.abstract}
                    """
            
            return context.strip()
        
        except Paper.DoesNotExist:
            logger.error(f"One of the papers not found")
            return ""
        
        except Exception as e:
            logger.error(f"Error building context: {str(e)}")
            return ""
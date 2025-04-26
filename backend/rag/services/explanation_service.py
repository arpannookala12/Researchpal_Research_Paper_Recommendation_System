import logging
import os
from django.conf import settings
from core.models import Paper
from .context_service import ContextRetrievalService

logger = logging.getLogger(__name__)

class ExplanationService:
    """Service for generating explanations for recommendations."""
    
    def __init__(self):
        """Initialize the explanation service."""
        self.context_service = ContextRetrievalService()
        
        # In a real production system, you would use a language model here
        # For now, we'll implement a simple template-based approach
    
    def explain_recommendation(self, source_paper_id, recommended_paper_id):
        """Generate an explanation for why a paper is recommended."""
        try:
            # Get papers
            source_paper = Paper.objects.get(id=source_paper_id)
            recommended_paper = Paper.objects.get(id=recommended_paper_id)
            
            # Build explanation based on shared categories and content
            shared_categories = []
            if hasattr(source_paper, 'categories') and hasattr(recommended_paper, 'categories'):
                source_categories = source_paper.categories.split() if isinstance(source_paper.categories, str) else source_paper.categories
                recommended_categories = recommended_paper.categories.split() if isinstance(recommended_paper.categories, str) else recommended_paper.categories
                
                if isinstance(source_categories, list) and isinstance(recommended_categories, list):
                    shared_categories = [cat for cat in source_categories if cat in recommended_categories]
            
            explanation = f"""
            This paper is recommended because it shares relevant research themes with "{source_paper.title}".
            """
            
            if shared_categories:
                explanation += f"\n\nBoth papers belong to the {', '.join(shared_categories)} {'category' if len(shared_categories) == 1 else 'categories'}."
            
            explanation += f"""
            
            The recommended paper explores {recommended_paper.title}, which appears to be relevant to your interest in {source_paper.title}.
            
            Both papers discuss similar concepts and methodologies that might be valuable for your research.
            """
            
            # In a production system, we would use a language model to generate a more specific explanation
            # based on the context retrieved from the context service
            
            return explanation.strip()
        
        except Paper.DoesNotExist:
            logger.error("One of the papers not found")
            return "Unable to generate explanation because one of the papers was not found."
        
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return "An error occurred while generating the explanation."
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Paper
from .services.explanation_service import ExplanationService

class RAGViewSet(viewsets.ViewSet):
    """ViewSet for RAG functionality."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.explanation_service = ExplanationService()
    
    @action(detail=False, methods=['post'])
    def explain_recommendation(self, request):
        """Explain why a paper is recommended."""
        source_paper_id = request.data.get('source_paper_id')
        recommended_paper_id = request.data.get('recommended_paper_id')
        
        if not source_paper_id or not recommended_paper_id:
            return Response(
                {"error": "Both source_paper_id and recommended_paper_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        explanation = self.explanation_service.explain_recommendation(
            source_paper_id=source_paper_id,
            recommended_paper_id=recommended_paper_id
        )
        
        return Response({"explanation": explanation})
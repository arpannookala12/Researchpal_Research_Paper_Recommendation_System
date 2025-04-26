from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.models import Paper, PaperView, Recommendation
from .serializers import PaperSerializer, PaperViewSerializer, RecommendationSerializer
from recommendation.services import RecommendationService
import logging

logger = logging.getLogger(__name__)

class PaperViewSet(viewsets.ModelViewSet):
    """ViewSet for the Paper model."""
    
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = Paper.objects.all().order_by('-update_date')
        
        # Apply filters if provided
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories=category)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        """Get recommendations for a paper."""
        paper = get_object_or_404(Paper, id=pk)
        
        # Create paper view
        PaperView.objects.create(
            paper=paper,
            session_id=request.session.session_key or 'anonymous',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        # Get existing recommendations or generate new ones
        recommendations = Recommendation.objects.filter(source_paper=paper)
        if not recommendations.exists():
            # Generate recommendations
            recommendation_service = RecommendationService()
            recommendations = recommendation_service.get_similar_papers(paper.id)
        
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search for papers based on a query."""
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Search for papers
        recommendation_service = RecommendationService()
        papers = recommendation_service.search_papers(query)
        
        serializer = PaperSerializer(papers, many=True)
        return Response(serializer.data)

class PaperViewViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the PaperView model."""
    
    queryset = PaperView.objects.all().order_by('-timestamp')
    serializer_class = PaperViewSerializer

class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the Recommendation model."""
    
    queryset = Recommendation.objects.all().order_by('-recommendation_date')
    serializer_class = RecommendationSerializer
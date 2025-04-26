from rest_framework import serializers
from core.models import Paper, PaperView, Recommendation

class PaperSerializer(serializers.ModelSerializer):
    """Serializer for the Paper model."""
    
    class Meta:
        model = Paper
        fields = ['id', 'title', 'abstract', 'authors', 'categories', 
                  'comments', 'update_date', 'created_at', 'updated_at']

class PaperViewSerializer(serializers.ModelSerializer):
    """Serializer for the PaperView model."""
    
    class Meta:
        model = PaperView
        fields = ['id', 'paper', 'session_id', 'timestamp']

class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for the Recommendation model."""
    
    recommended_paper_details = PaperSerializer(source='recommended_paper', read_only=True)
    
    class Meta:
        model = Recommendation
        fields = ['id', 'source_paper', 'recommended_paper', 'recommended_paper_details',
                  'similarity_score', 'recommendation_date', 'model_name']
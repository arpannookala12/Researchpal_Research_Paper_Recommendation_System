from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class Paper(models.Model):
    """Model for research papers."""
    
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    authors = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    categories = models.CharField(max_length=50)
    comments = models.TextField(blank=True, null=True)
    update_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['categories']),
            models.Index(fields=['update_date']),
        ]
    
    def __str__(self):
        return self.title

class PaperView(models.Model):
    """Model for tracking paper views."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='views')
    session_id = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['timestamp']),
        ]

class Recommendation(models.Model):
    """Model for storing recommendations."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='recommendations_made')
    recommended_paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='recommended_for')
    similarity_score = models.FloatField()
    recommendation_date = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=50, default="allenai-specter")
    
    class Meta:
        unique_together = ('source_paper', 'recommended_paper', 'model_name')
        indexes = [
            models.Index(fields=['similarity_score']),
            models.Index(fields=['recommendation_date']),
        ]
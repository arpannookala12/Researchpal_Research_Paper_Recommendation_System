from django.db import models
import uuid
import json
from users.models import User

# Custom JSON field for SQLite compatibility
class JSONField(models.TextField):
    """
    JSONField is a TextField that serializes/deserializes JSON objects.
    This is a simpler implementation for SQLite compatibility.
    """
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, (dict, list)):
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value)

class Paper(models.Model):
    """Model for research papers."""
    
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    # Replace ArrayField with JSONField for SQLite compatibility
    authors = JSONField(default=str([]))
    categories = models.CharField(max_length=100)
    comments = models.TextField(blank=True, null=True)
    journal_ref = models.CharField(max_length=255, blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True)
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

class PaperEmbedding(models.Model):
    """Model to track paper embeddings in vector database."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='embeddings')
    model_name = models.CharField(max_length=100)
    vector_id = models.CharField(max_length=100)
    dimensions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('paper', 'model_name')
        indexes = [
            models.Index(fields=['model_name']),
            models.Index(fields=['vector_id']),
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

class UserPaperInteraction(models.Model):
    """Model for tracking user interactions with papers."""
    
    INTERACTION_TYPES = (
        ('view', 'View'),
        ('save', 'Save'),
        ('download', 'Download'),
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paper_interactions')
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='user_interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['paper', 'interaction_type']),
            models.Index(fields=['timestamp']),
        ]

class UserSearch(models.Model):
    """Model for tracking user search queries."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searches', null=True, blank=True)
    query = models.TextField()
    filters = JSONField(default=dict)  # Using our custom JSONField
    result_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_id']),
            models.Index(fields=['timestamp']),
        ]
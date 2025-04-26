# Complete backend/core/admin.py
from django.contrib import admin
from .models import Paper, PaperView, Recommendation

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'categories', 'update_date')
    search_fields = ('id', 'title', 'abstract', 'categories')
    list_filter = ('categories', 'update_date')

@admin.register(PaperView)
class PaperViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'paper', 'session_id', 'timestamp')
    list_filter = ('timestamp',)

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_paper', 'recommended_paper', 'similarity_score', 'model_name')
    list_filter = ('model_name', 'recommendation_date')
    search_fields = ('source_paper__title', 'recommended_paper__title')
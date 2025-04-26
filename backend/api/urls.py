from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaperViewSet, PaperViewViewSet, RecommendationViewSet
from rag.views import RAGViewSet

# Import RAG ViewSet
from rag.views import RAGViewSet
router = DefaultRouter()
router.register(r'papers', PaperViewSet)
router.register(r'paper-views', PaperViewViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'rag', RAGViewSet, basename='rag')
urlpatterns = [
    path('', include(router.urls)),
]
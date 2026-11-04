"""
Legacy NexusRAG Service compatibility module.
Redirects to DualEngineRAGService.
"""
from app.services.dual_engine_rag_service import DualEngineRAGService, NexusRAGService

__all__ = ["DualEngineRAGService", "NexusRAGService"]

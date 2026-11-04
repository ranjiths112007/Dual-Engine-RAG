from pydantic_settings import BaseSettings
from pydantic import Field, AliasChoices
from functools import lru_cache
from pathlib import Path

# Find .env file - check project root first, fallback for Docker
_candidate = Path(__file__).resolve().parent.parent.parent.parent / ".env"
ENV_FILE = str(_candidate) if _candidate.exists() else ".env"


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Dual-Engine RAG"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Base directory (backend folder)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Database
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5433/nexusrag")

    # LLM Provider: "gemini" | "ollama"
    LLM_PROVIDER: str = Field(default="gemini")

    # Google AI
    GOOGLE_AI_API_KEY: str = Field(default="")

    # Ollama
    OLLAMA_HOST: str = Field(default="http://localhost:11434")
    OLLAMA_MODEL: str = Field(default="gemma3:12b")
    OLLAMA_ENABLE_THINKING: bool = Field(default=False)

    # LLM (fast model for chat + KG extraction — used when provider=gemini)
    LLM_MODEL_FAST: str = Field(default="gemini-3.5-flash")

    # Thinking level for Gemini 3.x+ models: "minimal" | "low" | "medium" | "high"
    LLM_THINKING_LEVEL: str = Field(default="medium")

    # Max output tokens for LLM chat responses (includes thinking tokens)
    LLM_MAX_OUTPUT_TOKENS: int = Field(default=8192)

    # KG Embedding provider (can differ from LLM provider)
    KG_EMBEDDING_PROVIDER: str = Field(default="gemini")
    KG_EMBEDDING_MODEL: str = Field(default="gemini-embedding-001")
    KG_EMBEDDING_DIMENSION: int = Field(default=3072)

    # ChromaDB
    CHROMA_HOST: str = Field(default="localhost")
    CHROMA_PORT: int = Field(default=8002)

    # Dual-Engine RAG Pipeline (supports DUAL_ENGINE_RAG_* with fallback to NEXUSRAG_*)
    DUAL_ENGINE_RAG_ENABLED: bool = Field(default=True, validation_alias=AliasChoices("DUAL_ENGINE_RAG_ENABLED", "NEXUSRAG_ENABLED"))
    DUAL_ENGINE_RAG_ENABLE_KG: bool = Field(default=True, validation_alias=AliasChoices("DUAL_ENGINE_RAG_ENABLE_KG", "NEXUSRAG_ENABLE_KG"))
    DUAL_ENGINE_RAG_ENABLE_IMAGE_EXTRACTION: bool = Field(default=True, validation_alias=AliasChoices("DUAL_ENGINE_RAG_ENABLE_IMAGE_EXTRACTION", "NEXUSRAG_ENABLE_IMAGE_EXTRACTION"))
    DUAL_ENGINE_RAG_ENABLE_IMAGE_CAPTIONING: bool = Field(default=True, validation_alias=AliasChoices("DUAL_ENGINE_RAG_ENABLE_IMAGE_CAPTIONING", "NEXUSRAG_ENABLE_IMAGE_CAPTIONING"))
    DUAL_ENGINE_RAG_ENABLE_TABLE_CAPTIONING: bool = Field(default=True, validation_alias=AliasChoices("DUAL_ENGINE_RAG_ENABLE_TABLE_CAPTIONING", "NEXUSRAG_ENABLE_TABLE_CAPTIONING"))
    DUAL_ENGINE_RAG_MAX_TABLE_MARKDOWN_CHARS: int = Field(default=8000, validation_alias=AliasChoices("DUAL_ENGINE_RAG_MAX_TABLE_MARKDOWN_CHARS", "NEXUSRAG_MAX_TABLE_MARKDOWN_CHARS"))
    DUAL_ENGINE_RAG_CHUNK_MAX_TOKENS: int = Field(default=512, validation_alias=AliasChoices("DUAL_ENGINE_RAG_CHUNK_MAX_TOKENS", "NEXUSRAG_CHUNK_MAX_TOKENS"))
    DUAL_ENGINE_RAG_KG_QUERY_TIMEOUT: float = Field(default=30.0, validation_alias=AliasChoices("DUAL_ENGINE_RAG_KG_QUERY_TIMEOUT", "NEXUSRAG_KG_QUERY_TIMEOUT"))
    DUAL_ENGINE_RAG_KG_CHUNK_TOKEN_SIZE: int = Field(default=1200, validation_alias=AliasChoices("DUAL_ENGINE_RAG_KG_CHUNK_TOKEN_SIZE", "NEXUSRAG_KG_CHUNK_TOKEN_SIZE"))
    DUAL_ENGINE_RAG_KG_LANGUAGE: str = Field(default="English", validation_alias=AliasChoices("DUAL_ENGINE_RAG_KG_LANGUAGE", "NEXUSRAG_KG_LANGUAGE"))
    DUAL_ENGINE_RAG_KG_ENTITY_TYPES: list[str] = Field(
        default=[
            "Organization", "Person", "Product", "Location", "Event",
            "Financial_Metric", "Technology", "Date", "Regulation",
        ],
        validation_alias=AliasChoices("DUAL_ENGINE_RAG_KG_ENTITY_TYPES", "NEXUSRAG_KG_ENTITY_TYPES")
    )
    DUAL_ENGINE_RAG_DEFAULT_QUERY_MODE: str = Field(default="hybrid", validation_alias=AliasChoices("DUAL_ENGINE_RAG_DEFAULT_QUERY_MODE", "NEXUSRAG_DEFAULT_QUERY_MODE"))
    DUAL_ENGINE_RAG_DOCLING_IMAGES_SCALE: float = Field(default=2.0, validation_alias=AliasChoices("DUAL_ENGINE_RAG_DOCLING_IMAGES_SCALE", "NEXUSRAG_DOCLING_IMAGES_SCALE"))
    DUAL_ENGINE_RAG_MAX_IMAGES_PER_DOC: int = Field(default=50, validation_alias=AliasChoices("DUAL_ENGINE_RAG_MAX_IMAGES_PER_DOC", "NEXUSRAG_MAX_IMAGES_PER_DOC"))
    DUAL_ENGINE_RAG_ENABLE_FORMULA_ENRICHMENT: bool = Field(default=True, validation_alias=AliasChoices("DUAL_ENGINE_RAG_ENABLE_FORMULA_ENRICHMENT", "NEXUSRAG_ENABLE_FORMULA_ENRICHMENT"))

    # Document Parser provider: "docling" (default) or "marker"
    DUAL_ENGINE_RAG_DOCUMENT_PARSER: str = Field(default="docling", validation_alias=AliasChoices("DUAL_ENGINE_RAG_DOCUMENT_PARSER", "NEXUSRAG_DOCUMENT_PARSER"))
    DUAL_ENGINE_RAG_MARKER_USE_LLM: bool = Field(default=False, validation_alias=AliasChoices("DUAL_ENGINE_RAG_MARKER_USE_LLM", "NEXUSRAG_MARKER_USE_LLM"))

    # Processing timeout (minutes) — stale documents auto-recover to FAILED
    DUAL_ENGINE_RAG_PROCESSING_TIMEOUT_MINUTES: int = Field(default=10, validation_alias=AliasChoices("DUAL_ENGINE_RAG_PROCESSING_TIMEOUT_MINUTES", "NEXUSRAG_PROCESSING_TIMEOUT_MINUTES"))

    # Pre-ingestion Deduplication
    DUAL_ENGINE_RAG_DEDUP_ENABLED: bool = Field(default=True, validation_alias=AliasChoices("DUAL_ENGINE_RAG_DEDUP_ENABLED", "NEXUSRAG_DEDUP_ENABLED"))
    DUAL_ENGINE_RAG_DEDUP_MIN_CHUNK_LENGTH: int = Field(default=50, validation_alias=AliasChoices("DUAL_ENGINE_RAG_DEDUP_MIN_CHUNK_LENGTH", "NEXUSRAG_DEDUP_MIN_CHUNK_LENGTH"))
    DUAL_ENGINE_RAG_DEDUP_NEAR_THRESHOLD: float = Field(default=0.85, validation_alias=AliasChoices("DUAL_ENGINE_RAG_DEDUP_NEAR_THRESHOLD", "NEXUSRAG_DEDUP_NEAR_THRESHOLD"))

    # Retrieval Quality
    DUAL_ENGINE_RAG_EMBEDDING_MODEL: str = Field(default="BAAI/bge-m3", validation_alias=AliasChoices("DUAL_ENGINE_RAG_EMBEDDING_MODEL", "NEXUSRAG_EMBEDDING_MODEL"))
    DUAL_ENGINE_RAG_RERANKER_MODEL: str = Field(default="BAAI/bge-reranker-v2-m3", validation_alias=AliasChoices("DUAL_ENGINE_RAG_RERANKER_MODEL", "NEXUSRAG_RERANKER_MODEL"))
    DUAL_ENGINE_RAG_VECTOR_PREFETCH: int = Field(default=20, validation_alias=AliasChoices("DUAL_ENGINE_RAG_VECTOR_PREFETCH", "NEXUSRAG_VECTOR_PREFETCH"))
    DUAL_ENGINE_RAG_RERANKER_TOP_K: int = Field(default=8, validation_alias=AliasChoices("DUAL_ENGINE_RAG_RERANKER_TOP_K", "NEXUSRAG_RERANKER_TOP_K"))
    DUAL_ENGINE_RAG_MIN_RELEVANCE_SCORE: float = Field(default=0.15, validation_alias=AliasChoices("DUAL_ENGINE_RAG_MIN_RELEVANCE_SCORE", "NEXUSRAG_MIN_RELEVANCE_SCORE"))

    # Backward compatibility properties
    @property
    def NEXUSRAG_ENABLED(self) -> bool:
        return self.DUAL_ENGINE_RAG_ENABLED

    @property
    def NEXUSRAG_ENABLE_KG(self) -> bool:
        return self.DUAL_ENGINE_RAG_ENABLE_KG

    @property
    def NEXUSRAG_ENABLE_IMAGE_EXTRACTION(self) -> bool:
        return self.DUAL_ENGINE_RAG_ENABLE_IMAGE_EXTRACTION

    @property
    def NEXUSRAG_ENABLE_IMAGE_CAPTIONING(self) -> bool:
        return self.DUAL_ENGINE_RAG_ENABLE_IMAGE_CAPTIONING

    @property
    def NEXUSRAG_ENABLE_TABLE_CAPTIONING(self) -> bool:
        return self.DUAL_ENGINE_RAG_ENABLE_TABLE_CAPTIONING

    @property
    def NEXUSRAG_MAX_TABLE_MARKDOWN_CHARS(self) -> int:
        return self.DUAL_ENGINE_RAG_MAX_TABLE_MARKDOWN_CHARS

    @property
    def NEXUSRAG_CHUNK_MAX_TOKENS(self) -> int:
        return self.DUAL_ENGINE_RAG_CHUNK_MAX_TOKENS

    @property
    def NEXUSRAG_KG_QUERY_TIMEOUT(self) -> float:
        return self.DUAL_ENGINE_RAG_KG_QUERY_TIMEOUT

    @property
    def NEXUSRAG_KG_CHUNK_TOKEN_SIZE(self) -> int:
        return self.DUAL_ENGINE_RAG_KG_CHUNK_TOKEN_SIZE

    @property
    def NEXUSRAG_KG_LANGUAGE(self) -> str:
        return self.DUAL_ENGINE_RAG_KG_LANGUAGE

    @property
    def NEXUSRAG_KG_ENTITY_TYPES(self) -> list[str]:
        return self.DUAL_ENGINE_RAG_KG_ENTITY_TYPES

    @property
    def NEXUSRAG_DEFAULT_QUERY_MODE(self) -> str:
        return self.DUAL_ENGINE_RAG_DEFAULT_QUERY_MODE

    @property
    def NEXUSRAG_DOCLING_IMAGES_SCALE(self) -> float:
        return self.DUAL_ENGINE_RAG_DOCLING_IMAGES_SCALE

    @property
    def NEXUSRAG_MAX_IMAGES_PER_DOC(self) -> int:
        return self.DUAL_ENGINE_RAG_MAX_IMAGES_PER_DOC

    @property
    def NEXUSRAG_ENABLE_FORMULA_ENRICHMENT(self) -> bool:
        return self.DUAL_ENGINE_RAG_ENABLE_FORMULA_ENRICHMENT

    @property
    def NEXUSRAG_DOCUMENT_PARSER(self) -> str:
        return self.DUAL_ENGINE_RAG_DOCUMENT_PARSER

    @property
    def NEXUSRAG_MARKER_USE_LLM(self) -> bool:
        return self.DUAL_ENGINE_RAG_MARKER_USE_LLM

    @property
    def NEXUSRAG_PROCESSING_TIMEOUT_MINUTES(self) -> int:
        return self.DUAL_ENGINE_RAG_PROCESSING_TIMEOUT_MINUTES

    @property
    def NEXUSRAG_DEDUP_ENABLED(self) -> bool:
        return self.DUAL_ENGINE_RAG_DEDUP_ENABLED

    @property
    def NEXUSRAG_DEDUP_MIN_CHUNK_LENGTH(self) -> int:
        return self.DUAL_ENGINE_RAG_DEDUP_MIN_CHUNK_LENGTH

    @property
    def NEXUSRAG_DEDUP_NEAR_THRESHOLD(self) -> float:
        return self.DUAL_ENGINE_RAG_DEDUP_NEAR_THRESHOLD

    @property
    def NEXUSRAG_EMBEDDING_MODEL(self) -> str:
        return self.DUAL_ENGINE_RAG_EMBEDDING_MODEL

    @property
    def NEXUSRAG_RERANKER_MODEL(self) -> str:
        return self.DUAL_ENGINE_RAG_RERANKER_MODEL

    @property
    def NEXUSRAG_VECTOR_PREFETCH(self) -> int:
        return self.DUAL_ENGINE_RAG_VECTOR_PREFETCH

    @property
    def NEXUSRAG_RERANKER_TOP_K(self) -> int:
        return self.DUAL_ENGINE_RAG_RERANKER_TOP_K

    @property
    def NEXUSRAG_MIN_RELEVANCE_SCORE(self) -> float:
        return self.DUAL_ENGINE_RAG_MIN_RELEVANCE_SCORE

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5174", "http://localhost:3000"]

    model_config = {
        "env_file": str(ENV_FILE),
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

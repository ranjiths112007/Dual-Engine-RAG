"""
Fast Document Parser
====================

Ultra-fast document parser using lightweight native text extractors (pypdf, etc.).
Parses documents in <0.5s without requiring heavy CPU neural networks.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.services.document_parser.base import BaseDocumentParser
from app.services.models.parsed_document import (
    EnrichedChunk,
    ParsedDocument,
)
from app.services.chunker import DocumentChunker
from app.services.document_loader import load_document

logger = logging.getLogger(__name__)

_SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx", ".pptx", ".ppt"}


class FastDocumentParser(BaseDocumentParser):
    """
    Ultra-fast document parser for instant indexing.
    - PDF: extracts text directly via pypdf per page (<0.2s)
    - DOCX/PPTX/TXT/MD: fast text extraction
    - Chunks with DocumentChunker
    """

    parser_name = "fast"

    @staticmethod
    def supported_extensions() -> set[str]:
        return _SUPPORTED_EXTENSIONS

    def parse(
        self,
        file_path: str | Path,
        document_id: int,
        original_filename: str,
    ) -> ParsedDocument:
        path = Path(file_path)
        suffix = path.suffix.lower()
        start_time = time.time()

        if suffix not in _SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {suffix}")

        chunks: list[EnrichedChunk] = []
        markdown_parts = []
        page_count = 1

        chunk_size = settings.DUAL_ENGINE_RAG_CHUNK_MAX_TOKENS * 4  # approx chars
        chunker = DocumentChunker(chunk_size=chunk_size, chunk_overlap=100)

        if suffix == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(str(path))
                page_count = len(reader.pages) or 1
                chunk_idx = 0
                for page_idx, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        markdown_parts.append(f"<!-- Page {page_idx + 1} -->\n" + page_text)
                        page_chunks = chunker.split_text(
                            text=page_text,
                            source=original_filename,
                            extra_metadata={"document_id": document_id, "page_no": page_idx + 1},
                        )
                        for pc in page_chunks:
                            chunks.append(
                                EnrichedChunk(
                                    content=pc.content,
                                    chunk_index=chunk_idx,
                                    source_file=original_filename,
                                    document_id=document_id,
                                    page_no=page_idx + 1,
                                )
                            )
                            chunk_idx += 1
                markdown_content = "\n\n".join(markdown_parts)
            except Exception as e:
                logger.warning(f"Fast PDF extraction failed: {e}, falling back to document_loader")
                loaded = load_document(str(path))
                page_count = loaded.page_count
                markdown_content = loaded.content
                text_chunks = chunker.split_text(
                    text=loaded.content,
                    source=original_filename,
                    extra_metadata={"document_id": document_id, "file_type": loaded.file_type},
                )
                chunks = [
                    EnrichedChunk(
                        content=tc.content,
                        chunk_index=i,
                        source_file=original_filename,
                        document_id=document_id,
                        page_no=1,
                    )
                    for i, tc in enumerate(text_chunks)
                ]
        else:
            loaded = load_document(str(path))
            page_count = loaded.page_count
            markdown_content = loaded.content
            text_chunks = chunker.split_text(
                text=loaded.content,
                source=original_filename,
                extra_metadata={"document_id": document_id, "file_type": loaded.file_type},
            )
            chunks = [
                EnrichedChunk(
                    content=tc.content,
                    chunk_index=i,
                    source_file=original_filename,
                    document_id=document_id,
                    page_no=1,
                )
                for i, tc in enumerate(text_chunks)
            ]

        elapsed_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"[fast-parser] Parsed document {document_id} ({original_filename}) in {elapsed_ms}ms: "
            f"{page_count} pages, {len(chunks)} chunks"
        )

        return ParsedDocument(
            document_id=document_id,
            original_filename=original_filename,
            markdown=markdown_content,
            page_count=page_count,
            chunks=chunks,
            images=[],
            tables=[],
            tables_count=0,
        )

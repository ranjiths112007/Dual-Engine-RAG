"""
Document Loader Service
Handles loading and extracting text from various document formats.
"""
from __future__ import annotations

from pathlib import Path
from typing import NamedTuple
import logging

logger = logging.getLogger(__name__)


class LoadedDocument(NamedTuple):
    """Represents a loaded document with its content and metadata."""
    content: str
    source: str
    file_type: str
    page_count: int = 1


def load_txt_file(file_path: Path) -> LoadedDocument:
    """Load a plain text file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        return LoadedDocument(
            content=content,
            source=str(file_path),
            file_type="txt",
            page_count=1
        )
    except UnicodeDecodeError:
        # Try with different encoding
        content = file_path.read_text(encoding="latin-1")
        return LoadedDocument(
            content=content,
            source=str(file_path),
            file_type="txt",
            page_count=1
        )


def load_pdf_file(file_path: Path) -> LoadedDocument:
    """Load a PDF file and extract text."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(file_path))
        pages_text = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)

        content = "\n\n".join(pages_text)

        return LoadedDocument(
            content=content,
            source=str(file_path),
            file_type="pdf",
            page_count=len(reader.pages)
        )
    except Exception as e:
        logger.error(f"Error loading PDF {file_path}: {e}")
        raise ValueError(f"Failed to load PDF: {e}")


def load_markdown_file(file_path: Path) -> LoadedDocument:
    """Load a markdown file."""
    content = file_path.read_text(encoding="utf-8")
    return LoadedDocument(
        content=content,
        source=str(file_path),
        file_type="md",
        page_count=1
    )


def load_pptx_file(file_path: Path) -> LoadedDocument:
    """Load a PPT/PPTX presentation using python-pptx."""
    try:
        from pptx import Presentation
        prs = Presentation(str(file_path))
        slides_text = []
        for i, slide in enumerate(prs.slides):
            slide_parts = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        text = paragraph.text.strip()
                        if text:
                            slide_parts.append(text)
            if slide_parts:
                slides_text.append(f"## Slide {i+1}\n" + "\n".join(slide_parts))
        content = "\n\n".join(slides_text)
        return LoadedDocument(
            content=content,
            source=str(file_path),
            file_type="pptx",
            page_count=len(prs.slides) or 1,
        )
    except Exception as e:
        logger.error(f"Error loading PPTX {file_path}: {e}")
        raise ValueError(f"Failed to load presentation: {e}")


def load_docx_file(file_path: Path) -> LoadedDocument:
    """Load a DOCX document using docx."""
    try:
        import docx
        doc = docx.Document(str(file_path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        content = "\n\n".join(paragraphs)
        return LoadedDocument(
            content=content,
            source=str(file_path),
            file_type="docx",
            page_count=1,
        )
    except Exception as e:
        logger.error(f"Error loading DOCX {file_path}: {e}")
        raise ValueError(f"Failed to load DOCX: {e}")


def load_document(file_path: str | Path) -> LoadedDocument:
    """
    Load a document based on its file type.

    Supported formats: .txt, .pdf, .md, .docx, .pptx, .ppt
    """
    path = Path(file_path)

    if not path.exists():
        raise ValueError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    loaders = {
        ".txt": load_txt_file,
        ".pdf": load_pdf_file,
        ".md": load_markdown_file,
        ".docx": load_docx_file,
        ".pptx": load_pptx_file,
        ".ppt": load_pptx_file,
    }

    loader = loaders.get(suffix)
    if loader is None:
        raise ValueError(f"Unsupported file type: {suffix}. Supported: {list(loaders.keys())}")

    return loader(path)


def get_supported_extensions() -> list[str]:
    """Return list of supported file extensions."""
    return [".txt", ".pdf", ".md", ".docx", ".pptx", ".ppt"]

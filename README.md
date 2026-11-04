# Dual-Engine RAG

A hybrid Retrieval-Augmented Generation (RAG) application combining semantic/vector retrieval with knowledge-graph retrieval, reranking, and grounded answer generation.

**Maintained and customized by Ranjith S**  
**Upstream project:** [NexusRAG by LaDat98](https://github.com/LeDat98/NexusRAG)

> This repository is a rebranded and customized distribution of the upstream project. The original implementation and its contributors remain credited; this is not a claim of sole original authorship.

## Included capabilities

- FastAPI backend and React + TypeScript frontend
- Vector retrieval and knowledge-graph retrieval
- Reranking for retrieval precision
- Document ingestion and parsing
- Streaming chat and source citations
- Docker-based development and deployment configuration

## Setup

Review the configuration examples and deployment files before starting:

- `.env.example`
- `frontend/.env.example`
- `docker-compose.yml`
- `docker-compose.services.yml`

Configure your own model/API credentials. Never commit secrets.

## Attribution and license

The upstream archive includes `LICENSE.md` with the **Do What The F*ck You Want To Public License (WTFPL), Version 2**, and a copyright notice for LaDat98 (2026). The upstream license is retained in this distribution. See [NOTICE.md](NOTICE.md) for provenance and customization notes.

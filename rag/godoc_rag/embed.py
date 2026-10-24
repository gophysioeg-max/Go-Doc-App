"""Embedding back ends. All return 1024-dimension, L2-normalised vectors."""

from __future__ import annotations

import hashlib
import math
import re
from typing import Protocol

DIM = 1024


class Embedder(Protocol):
    name: str

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, text: str) -> list[float]: ...


class BgeM3:
    """BAAI/bge-m3 run locally: free, offline after the first download, strong on Arabic."""

    name = "bge-m3"

    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer  # optional dependency

        self._model = SentenceTransformer("BAAI/bge-m3")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._model.encode(texts, batch_size=16, normalize_embeddings=True,
                                  show_progress_bar=len(texts) > 64).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


class Voyage:
    """Voyage AI API (needs VOYAGE_API_KEY). Use a model with 1024-dim output."""

    def __init__(self, model: str) -> None:
        import voyageai  # optional dependency

        self.name = f"voyage:{model}"
        self._model = model
        self._client = voyageai.Client()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        for i in range(0, len(texts), 64):
            res = self._client.embed(texts[i:i + 64], model=self._model,
                                     input_type="document", output_dimension=DIM)
            out.extend(res.embeddings)
        return out

    def embed_query(self, text: str) -> list[float]:
        return self._client.embed([text], model=self._model, input_type="query",
                                  output_dimension=DIM).embeddings[0]


class HashEmbedder:
    """Deterministic bag-of-words hashing. For tests and offline wiring only:
    it matches shared words, not meaning."""

    name = "hash"

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        vec = [0.0] * DIM
        for token in re.findall(r"\w+", text.lower()):
            h = int.from_bytes(hashlib.blake2b(token.encode(), digest_size=8).digest(), "big")
            vec[h % DIM] += 1.0 if (h >> 63) & 1 else -1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


def get(name: str, voyage_model: str = "voyage-3.5") -> Embedder:
    if name == "bge-m3":
        return BgeM3()
    if name == "voyage":
        return Voyage(voyage_model)
    if name == "hash":
        return HashEmbedder()
    raise ValueError(f"unknown embedder {name!r}; use bge-m3, voyage or hash")

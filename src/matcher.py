"""Semantic similarity. Uses sentence-transformers; falls back to TF-IDF if the model can't load (offline)."""
import numpy as np


class Embedder:
    def __init__(self):
        self.model = None
        self.kind = "TF-IDF (fallback)"
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.kind = "MiniLM embeddings"
        except Exception:
            pass

    def raw_similarity(self, query: str, texts: list) -> list:
        if not texts:
            return []
        if self.model is not None:
            vecs = self.model.encode([query] + texts, normalize_embeddings=True)
            return [float(v @ vecs[0]) for v in vecs[1:]]
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        m = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform([query] + texts)
        return list(cosine_similarity(m[0], m[1:])[0])

    def semantic_scores(self, jd: str, texts: list) -> list:
        """Rescaled to 0-1 so scores are intuitive for recruiters."""
        raw = self.raw_similarity(jd, texts)
        if self.model is not None:
            return [float(np.clip((s - 0.15) / 0.55, 0, 1)) for s in raw]
        return [float(min(1.0, s * 2.5)) for s in raw]

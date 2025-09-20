from sentence_transformers import SentenceTransformer
from app.config import settings
from numpy import ndarray


embed_model = SentenceTransformer(settings.embedding_model)

def embed_encode(string: str) -> ndarray:
    return embed_model.encode([string]).flatten()
"""Skill taxonomy: canonical skill -> aliases. Synonyms are what make matching 'smarter' than plain keywords."""
import re

SKILL_MAP = {
    "python": ["python"], "java": ["java"], "javascript": ["javascript", "js"],
    "typescript": ["typescript"], "c++": ["c++"], "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
    "machine learning": ["machine learning", "ml"], "deep learning": ["deep learning", "neural networks", "cnn", "lstm"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "opencv", "yolo", "image processing", "object detection"],
    "llm": ["llm", "llms", "large language model", "large language models", "generative ai", "genai"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented generation", "retrieval-augmented systems"],
    "vector database": ["faiss", "chroma", "chromadb", "pinecone", "vector database", "vector db"],
    "langchain": ["langchain", "langgraph"], "pytorch": ["pytorch"], "tensorflow": ["tensorflow", "keras"],
    "scikit-learn": ["scikit-learn", "sklearn"], "pandas": ["pandas"], "numpy": ["numpy"],
    "fastapi": ["fastapi"], "flask": ["flask"], "django": ["django"], "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "express"], "rest api": ["rest api", "rest apis", "restful"],
    "docker": ["docker"], "kubernetes": ["kubernetes", "k8s"], "aws": ["aws", "amazon web services"],
    "azure": ["azure"], "gcp": ["gcp", "google cloud"], "git": ["git", "github"], "linux": ["linux"],
    "streamlit": ["streamlit"], "mongodb": ["mongodb"], "multi-agent systems": ["multi-agent", "multi agent", "agentic"],
    "mlops": ["mlops", "model deployment"], "ci/cd": ["ci/cd", "github actions", "jenkins"],
    "data structures": ["data structures", "dsa", "algorithms"], "oop": ["oop", "oops", "object-oriented"],
    "html/css": ["html", "css", "tailwind"], "power bi": ["power bi", "tableau"],
}

_PATTERNS = {
    canon: re.compile(r"(?<![\w+#.])(?:%s)(?![\w+#])" % "|".join(re.escape(a) for a in aliases), re.I)
    for canon, aliases in SKILL_MAP.items()
}


def extract_skills(text: str) -> set:
    return {canon for canon, pat in _PATTERNS.items() if pat.search(text or "")}

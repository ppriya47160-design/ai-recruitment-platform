"""Resume Q&A. Uses Claude if ANTHROPIC_API_KEY is set, otherwise offline retrieval of the most relevant resume lines."""
import os


def retrieve_chunks(question: str, text: str, embedder, k: int = 3) -> list:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    chunks = [" ".join(lines[i:i + 3]) for i in range(0, len(lines), 3)] or [text]
    sims = embedder.raw_similarity(question, chunks)
    order = sorted(range(len(chunks)), key=lambda i: sims[i], reverse=True)[:k]
    return [chunks[i] for i in order]


def ask(question: str, resume_text: str, embedder) -> str:
    chunks = retrieve_chunks(question, resume_text, embedder)
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return "**Offline mode (no API key).** Most relevant resume parts:\n\n" + "\n\n".join(f"- {c}" for c in chunks)
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        msg = client.messages.create(
            model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"), max_tokens=500,
            system="You are a recruiting assistant. Answer ONLY from the resume excerpts. If the evidence is missing, say so.",
            messages=[{"role": "user", "content": "Resume excerpts:\n" + "\n---\n".join(chunks) + f"\n\nQuestion: {question}"}],
        )
        return msg.content[0].text
    except Exception as e:
        return f"Claude call failed ({e}). Relevant parts:\n\n" + "\n\n".join(f"- {c}" for c in chunks)

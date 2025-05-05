import json
import requests
import sys
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# ——— Config ———
CHEMIN_DB_FAISS = r"C:\Users\User\Desktop\projet_fin_d'annee\chatbot_RASA\data\DATA\data_public\db_faiss"
OLLAMA_API_URL  = "http://127.0.0.1:11435/api/generate"  # port où tourne ollama serve

# ——— Prompt template ———
MODELE_PROMPT_PERSONNALISE = """\
Utilisez les informations suivantes pour répondre à la question de l'utilisateur.
Si vous ne connaissez pas la réponse, dites que vous ne savez pas, n'inventer rien.

Contexte :
{contexte}

Question :
{question}

Réponse utile :
"""

# ——— Chargement FAISS + embeddings ———
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)
faiss_index = FAISS.load_local(CHEMIN_DB_FAISS, embeddings)

def interroger_ollama(prompt: str) -> str:
    """
    Envoie le prompt à Ollama Mistral via l’API HTTP et renvoie le texte généré.
    On désactive le streaming pour récupérer toute la réponse d’un coup.
    """
    payload = {
        "model":  "mistral",
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        choice = data.get("choices", [{}])[0]
        return choice.get("text") or choice.get("response", "")
    except requests.RequestException as e:
        print(f"[Erreur API Ollama] {e}", file=sys.stderr)
        return "Désolé, je n’ai pas pu contacter Mistral pour le moment."

def interroger_faiss_plus_ollama(question: str, k: int = 2) -> str:
    """
    1) Récupère les k docs les plus similaires via FAISS.
    2) Construit le prompt avec le contexte + la question.
    3) Interroge Mistral et renvoie la réponse.
    """
    docs = faiss_index.similarity_search(question, k=k)
    contexte = "\n\n".join(d.page_content for d in docs)
    prompt = MODELE_PROMPT_PERSONNALISE.format(contexte=contexte, question=question)
    return interroger_ollama(prompt)

if __name__ == "__main__":
    # Exemple de lancement en CLI :
    # python faiss_cpu.py "Explique-moi le fonctionnement de FAISS." 3
    import argparse
    parser = argparse.ArgumentParser(description="Pipeline FAISS + Ollama")
    parser.add_argument("question", help="Question à poser au chatbot")
    parser.add_argument("-k", "--top_k", type=int, default=2, help="Nombre de documents FAISS à récupérer")
    args = parser.parse_args()

    réponse = interroger_faiss_plus_ollama(args.question, k=args.top_k)
    print(réponse)

import json
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# 1) Charger ton JSON structuré
with open(r"C:\Users\User\Desktop\projet_fin_d'annee\chatbot_RASA\data\DATA\data_public\data_public.json", "r", encoding="utf-8") as f:
    sections = json.load(f)

# 2) Créer des Documents LangChain à partir de chaque paragraphe
documents = []
for entry in sections:
    sec = entry["section"]
    for para in entry["paragraphs"]:
        documents.append(
            Document(
                page_content=para,
                metadata={"section": sec}
            )
        )

# 3) (Optionnel) Re-chunker si tu veux des morceaux plus petits
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# documents = splitter.split_documents(documents)

# 4) Générer les embeddings
emb = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

# 5) Construire et sauvegarder l’index FAISS
db = FAISS.from_documents(documents, emb)
db.save_local(r"C:\Users\User\Desktop\projet_fin_d'annee\chatbot_RASA\data\DATA\data_public\db_faiss")

print("✅ Base FAISS créée à partir de ton JSON")


def build_index():
    if __name__ == "__main__":
        build_index()
    print("✅ Index FAISS construit.")

    
    

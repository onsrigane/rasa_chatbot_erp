import json
import re
import nltk
from nltk.tokenize import blankline_tokenize

# Si c'est la première fois, téléchargez le tokenizer NLTK :
# nltk.download('punkt')

def txt_to_paragraphs_json(input_path: str, output_path: str):
    docs = []
    current_section = None
    buffer = []

    # Lire tout le fichier brut
    with open(input_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    # 1) Insère une ligne vide avant chaque "- " et chaque "Clé:" pour marquer un nouveau paragraphe
    pre = re.sub(r'\n(- )', r'\n\n\1', raw)
    pre = re.sub(r'\n([A-Za-z][\w\s]+?:)', r'\n\n\1', pre)

    # 2) Découpage en paragraphes selon les lignes vides
    paras = blankline_tokenize(pre)

    # 3) Répartir les paragraphes par section
    for p in paras:
        p = p.strip()
        if not p:
            continue

        # Si c'est une nouvelle section
        m = re.match(r'^Section:\s*(.+)', p)
        if m:
            # Sauvegarde l’ancienne
            if current_section:
                docs.append(current_section)
            # Crée une nouvelle section
            current_section = {
                "section": m.group(1).strip(),
                "paragraphs": []
            }
        else:
            # Ajoute ce paragraphe à la section courante
            if current_section:
                current_section["paragraphs"].append(p)

    # N’oublie pas la dernière
    if current_section:
        docs.append(current_section)

    # 4) Écriture du JSON
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(docs, out, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    txt_to_paragraphs_json(
        r"C:\Users\User\...\decoupage_data.txt",
        r"C:\Users\User\...\data_public_paragraphs.json"
    )
    print("✅ JSON avec paragraphes généré")

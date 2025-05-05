import json
import re

def txt_to_json(input_path: str, output_path: str):
    docs = []
    current = None

    # Expressions régulières
    section_re = re.compile(r'^Section:\s*(.+)')
    kv_re      = re.compile(r'^([\w\s]+):\s*(.+)')

    with open(input_path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip()

            # 1) Nouvelle section ?
            m = section_re.match(line)
            if m:
                # Sauvegarde la section précédente
                if current:
                    docs.append(current)
                # Initialise la nouvelle
                current = {
                    "section": m.group(1).strip(),
                    "metadata": {},
                    "content": []
                }
                continue

            # Si on est dans une section valide
            if current is not None:
                # 2) Ligne "Clé: Valeur" ?
                m2 = kv_re.match(line)
                if m2:
                    key = m2.group(1).strip()
                    val = m2.group(2).strip()
                    # Si clé déjà présente, on fait une liste
                    current["metadata"].setdefault(key, []).append(val)
                else:
                    # 3) Liste à puce ou texte libre
                    if line.startswith('- '):
                        current["content"].append(line[2:].strip())
                    elif line:
                        current["content"].append(line)
        # N’oublie pas la dernière section
        if current:
            docs.append(current)

    # Convertir les listes de contenu en chaîne
    for d in docs:
        d["content"] = "\n".join(d["content"])

    # Écrire le JSON
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(docs, out, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    txt_to_json(
        r"C:\Users\User\Desktop\projet_fin_d'annee\chatbot_RASA\data\DATA\data_public\data_public_decoupage.txt",
        r"C:\Users\User\Desktop\projet_fin_d'annee\chatbot_RASA\data\DATA\data_public\data_public.json"
    )
    print("✅ Conversion terminée : data_public.json créé")

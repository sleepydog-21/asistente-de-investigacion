import os
import json
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

# Configuración
load_dotenv(dotenv_path="credentials/.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedding_model = "text-embedding-3-small"

input_path = "data/fragments/fragments.json"
index_path = "data/embeddings/index.faiss"
metadata_path = "data/embeddings/metadata.json"
resumen_path = "data/descarga_resumen.json"
os.makedirs("data/embeddings", exist_ok=True)

# Leer lista de títulos si existe
usar_resumen = os.path.exists(resumen_path)
titulos_validos = set()

if usar_resumen:
    with open(resumen_path, "r", encoding="utf-8") as f:
        resumen = json.load(f)
        titulos_validos = {entry["title"] for entry in resumen}

# Cargar fragmentos
with open(input_path, "r", encoding="utf-8") as f:
    fragments = json.load(f)

print(f"🧩 Fragmentos cargados: {len(fragments)}")
if usar_resumen:
    print(f"📑 Filtrando por títulos en descarga_resumen: {len(titulos_validos)}")

# Preparar FAISS con similitud de coseno
dim = 1536
index = faiss.IndexFlatIP(dim)
metadata = []

for i, frag in enumerate(fragments):
    if usar_resumen and frag["title"] not in titulos_validos:
        continue

    if not frag.get("text"):
        print(f"⚠️ Fragmento sin texto en índice {i}")
        continue

    try:
        response = client.embeddings.create(
            model=embedding_model,
            input=frag["text"]
        )
        vector = np.array(response.data[0].embedding, dtype=np.float32)
        norm = np.linalg.norm(vector)

        if norm == 0:
            print(f"⚠️ Vector nulo en fragmento {i + 1}, omitido.")
            continue

        vector /= norm
        index.add(np.array([vector]))
        metadata.append({
            "chunk_id": frag["chunk_id"],
            "title": frag["title"],
            "doi": frag["doi"],
            "year": frag["year"],
            "source": frag["source"],
            "authors": frag["authors"]
        })

    except Exception as e:
        print(f"⚠️ Error en el fragmento {i + 1}: {e}")

# Guardar índice y metadatos
faiss.write_index(index, index_path)
with open(metadata_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✅ Se generaron {len(metadata)} embeddings y se guardaron en '{index_path}'")
print(f"🧠 Total de vectores en FAISS: {index.ntotal}")
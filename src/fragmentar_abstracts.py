import os
import json
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Configuración
load_dotenv(dotenv_path="credentials/.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

fulltext_dir = "data/papers_fulltext"
abstracts_path = "data/fragments/fragments.json"
resumen_path = "data/descarga_resumen.json"
resumenes_dir = "resumenes"
os.makedirs(resumenes_dir, exist_ok=True)

# Historial
historial = []

def guardar_resumen(historial):
    resumen_texto = ""
    for paso in historial:
        resumen_texto += f"🧐 Pregunta: {paso['pregunta']}\n\n"
        resumen_texto += f"💬 Respuesta:\n{paso['respuesta']}\n\n"
        resumen_texto += "📚 Fuentes:\n"
        for cita in paso['fuentes']:
            resumen_texto += f"- {cita}\n"
        resumen_texto += "\n" + ("=" * 50) + "\n\n"

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    resumen_path_out = os.path.join(resumenes_dir, f"resumen_{timestamp}.md")
    with open(resumen_path_out, "w", encoding="utf-8") as f:
        f.write(resumen_texto)
    print(f"📝 Resumen guardado en {resumen_path_out}")

# Cargar abstracts
abstracts = []
fuentes = []
if os.path.exists(abstracts_path):
    with open(abstracts_path, encoding="utf-8") as f:
        fragments = json.load(f)
        for frag in fragments:
            abstracts.append(frag)

# Chat principal
print("\n🔍 Búsqueda semántica (modo palabras clave en abstract)")
print("Escribe tu término de búsqueda. Usa 'resumen' para guardar o 'salir' para terminar.\n")

while True:
    pregunta = input(">> Tu búsqueda: ").strip()
    if pregunta.lower() in ("salir", "exit", "quit"):
        print("👋 Sesión finalizada.")
        break

    if pregunta.lower() == "resumen":
        if historial:
            guardar_resumen(historial)
        else:
            print("⚠️ No hay historial para resumir.")
        continue

    print("\n🔎 Buscando artículos que contienen palabras clave en su abstract...\n")
    keywords = pregunta.lower().split()
    encontrados = [
        frag for frag in abstracts
        if any(kw in frag["text"].lower() for kw in keywords)
    ]

    if not encontrados:
        print("⚠️ No se encontraron coincidencias en los abstracts.")
        actualizar = input("¿Deseas actualizar la base con este tema? (S/N): ").strip().lower()
        if actualizar == "s":
            subprocess.run(["python", "src/descargar_articulos_pubmed.py", pregunta], check=True)
            subprocess.run(["python", "src/fragmentar_abstracts.py"], check=True)
            subprocess.run(["python", "src/generar_embeddings.py"], check=True)
            with open(resumen_path, "w", encoding="utf-8") as f:
                f.write("[]")
            print("✅ Base actualizada. Intenta hacer tu búsqueda nuevamente.")
        continue

    top5 = encontrados[:5]
    resumenes = "\n\n".join([frag["text"] for frag in top5])
    fuentes = [frag["title"] for frag in top5]

    print("\n🤖 Generando resumen con GPT-4-turbo...\n")
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente científico. Solo responde utilizando los abstracts proporcionados. No inventes información. Si no puedes responder con los textos dados, di que no hay suficiente información."
                },
                {
                    "role": "user",
                    "content": f"Resumen de los siguientes artículos:\n\n" + "\n\n".join([f"Título: {frag['title']}\nAbstract: {frag['text']}" for frag in top5]) + f"\n\nPregunta: {pregunta}\n\nSi alguna información no está presente en los abstracts, no la inventes."
                }
            ],
            temperature=0.3
        )
        respuesta = completion.choices[0].message.content.strip()
        print(respuesta)

        historial.append({
            "pregunta": pregunta,
            "respuesta": respuesta,
            "fuentes": fuentes
        })

    except Exception as e:
        print("❌ Error al generar respuesta:", e)


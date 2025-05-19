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
resumenes_dir = "resumenes"
os.makedirs(resumenes_dir, exist_ok=True)

# Cargar abstracts
abstracts = []
fuentes = []
if os.path.exists(abstracts_path):
    with open(abstracts_path, encoding="utf-8") as f:
        fragments = json.load(f)
        for frag in fragments:
            abstracts.append(frag["text"])
            fuentes.append(frag["title"][:80])

# Cargar textos completos
textos_completos = {}
for filename in os.listdir(fulltext_dir):
    if filename.endswith(".txt"):
        path = os.path.join(fulltext_dir, filename)
        with open(path, encoding="utf-8") as f:
            textos_completos[filename.replace(".txt", "")] = f.read()

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
    resumen_path = os.path.join(resumenes_dir, f"resumen_{timestamp}.md")
    with open(resumen_path, "w", encoding="utf-8") as f:
        f.write(resumen_texto)
    print(f"📝 Resumen guardado en {resumen_path}")

# Chat principal
print("\n💬 Asistente de investigación (modo chat directo)")
print("Puedes escribir tu pregunta sobre el tema. Escribe 'resumen' para guardar la sesión o 'salir' para terminar.\n")

while True:
    pregunta = input(">> Tu pregunta: ").strip()
    if pregunta.lower() in ("salir", "exit", "quit"):
        print("👋 Sesión finalizada.")
        break

    if pregunta.lower() == "resumen":
        if historial:
            guardar_resumen(historial)
        else:
            print("⚠️ No hay historial para resumir.")
        continue

    # Primero usar los abstracts
    contexto = "\n\n".join(abstracts)[:12000]

    print("\n🤖 Generando respuesta con GPT-4-turbo...\n")
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente científico experto en biología molecular. Usa el conocimiento de los artículos proporcionados para responder preguntas de forma precisa, clara y con referencias."},
                {"role": "user", "content": f"Pregunta: {pregunta}\n\nResumen de artículos relevantes:\n{contexto}"}
            ],
            temperature=0.3
        )
        respuesta = completion.choices[0].message.content.strip()
        print(respuesta)

        historial.append({
            "pregunta": pregunta,
            "respuesta": respuesta,
            "fuentes": fuentes[:5]
        })

    except Exception as e:
        print("❌ Error al generar respuesta:", e)

    # Preguntar si se debe consultar el texto completo
    expandir = input("¿Deseas consultar los textos completos para una mejor respuesta? (S/N): ").strip().lower()
    if expandir == "s":
        contexto_ext = "\n\n".join(textos_completos.values())[:12000]
        print("\n🔄 Generando respuesta extendida...\n")
        try:
            completion = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente científico experto en biología molecular. Usa el conocimiento de los artículos completos para responder con más profundidad."},
                    {"role": "user", "content": f"Pregunta: {pregunta}\n\nTexto completo de artículos:\n{contexto_ext}"}
                ],
                temperature=0.3
            )
            respuesta_ext = completion.choices[0].message.content.strip()
            print(respuesta_ext)

            historial[-1]["respuesta"] += "\n\n📌 Extensión basada en texto completo:\n" + respuesta_ext

        except Exception as e:
            print("❌ Error al generar respuesta extendida:", e)

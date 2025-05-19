import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Configuración
load_dotenv(dotenv_path="credentials/.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

fulltext_dir = "data/papers_fulltext"
resumenes_dir = "resumenes"
os.makedirs(resumenes_dir, exist_ok=True)

def resumen_articulo():
    print("🔎 Escribe una palabra clave para buscar un artículo:")
    keyword = input(">>> ").strip().lower()

    matches = [f for f in os.listdir(fulltext_dir) if keyword in f.lower() and f.endswith(".txt")]

    if not matches:
        print("❌ No se encontraron artículos que coincidan.")
        return

    print("\n📄 Artículos encontrados:")
    for i, name in enumerate(matches, 1):
        print(f"{i}. {name}")

    idx = input("\nSelecciona el número del artículo a resumir: ").strip()
    if not idx.isdigit() or int(idx) < 1 or int(idx) > len(matches):
        print("❌ Selección inválida.")
        return

    filename = matches[int(idx) - 1]
    filepath = os.path.join(fulltext_dir, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        contenido = f.read()

    print("\n🤖 Generando resumen con GPT-4-turbo...\n")
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente científico. Resume este artículo de forma clara, estructurada y concisa."},
                {"role": "user", "content": contenido[:12000]}
            ],
            temperature=0.3
        )
        resumen = completion.choices[0].message.content.strip()
        print(resumen)

        guardar = input("\n¿Deseas guardar este resumen en la carpeta 'resumenes'? (S/N): ").strip().lower()
        if guardar == "s":
            output_name = f"resumen_{filename.replace('.txt','')}.md"
            output_path = os.path.join(resumenes_dir, output_name)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(resumen)
            print(f"✅ Resumen guardado en '{output_path}'")

    except Exception as e:
        print("❌ Error al generar el resumen:", e)

# Bucle para múltiples resúmenes
while True:
    resumen_articulo()
    cont = input("\n¿Deseas resumir otro artículo? (S/N): ").strip().lower()
    if cont != "s":
        break
import os
from openai import OpenAI
from dotenv import load_dotenv

# Configuración
load_dotenv(dotenv_path="credentials/.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

fulltext_dir = "data/papers_fulltext"
resumenes_dir = "resumenes"
os.makedirs(resumenes_dir, exist_ok=True)

def listar_articulos():
    archivos = [f for f in os.listdir(fulltext_dir) if f.endswith(".txt")]
    for i, name in enumerate(archivos, 1):
        print(f"{i}. {name}")
    return archivos

def cargar_texto(nombre):
    path = os.path.join(fulltext_dir, nombre)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def comparar_articulos():
    print("📚 Lista de artículos disponibles:")
    archivos = listar_articulos()
    if len(archivos) < 2:
        print("❌ Se requieren al menos 2 artículos.")
        return

    try:
        i1 = int(input("\\nSelecciona el número del primer artículo: ")) - 1
        i2 = int(input("Selecciona el número del segundo artículo: ")) - 1
        if i1 == i2 or not (0 <= i1 < len(archivos)) or not (0 <= i2 < len(archivos)):
            print("❌ Selección inválida.")
            return
    except ValueError:
        print("❌ Entrada no válida.")
        return

    art1 = archivos[i1]
    art2 = archivos[i2]

    texto1 = cargar_texto(art1)[:6000]
    texto2 = cargar_texto(art2)[:6000]

    prompt = (
        "Compara críticamente los siguientes dos artículos científicos.\n\n"
        f"Artículo 1: {texto1}\n\n---\n\n"
        f"Artículo 2: {texto2}\n\n---\n\n"
        "Haz una comparación clara, concisa y estructurada, destacando similitudes, diferencias, enfoques metodológicos y hallazgos clave."
    )

    print("\\n🤖 Generando comparación con GPT-4-turbo...\\n")
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente científico que compara artículos de forma crítica y clara."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        comparacion = completion.choices[0].message.content.strip()
        print(comparacion)

        guardar = input("\\n¿Deseas guardar esta comparación? (S/N): ").strip().lower()
        if guardar == "s":
            nombre = f"comparacion_{art1[:40]}__{art2[:40]}.md".replace(' ', '_')
            ruta = os.path.join(resumenes_dir, nombre)
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(comparacion)
            print(f"✅ Comparación guardada en '{ruta}'")

    except Exception as e:
        print("❌ Error al generar la comparación:", e)

# Bucle para comparar múltiples veces
while True:
    comparar_articulos()
    cont = input("\\n¿Deseas comparar otros artículos? (S/N): ").strip().lower()
    if cont != "s":
        break
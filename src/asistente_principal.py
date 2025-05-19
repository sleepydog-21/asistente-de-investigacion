import os

def mostrar_menu():
    print("""\n🎓 Asistente de Investigación - Menú Principal
Selecciona una opción:

1. 📄 Resumen de un artículo
2. 📊 Comparación entre artículos
3. 🔍 Búsqueda semántica
4. 💬 Asistente en chat
0. 🔁 Salir
""")

while True:
    mostrar_menu()
    opcion = input("Ingresa el número de tu elección (0-4): ").strip()

    if opcion == "1":
        os.system("python src/resumen_articulo.py")
    elif opcion == "2":
        os.system("python src/comparar_articulos.py")
    elif opcion == "3":
        os.system("python src/semantica.py")
    elif opcion == "4":
        os.system("python chat_asistente2.0.py")
    elif opcion == "0":
        print("👋 Saliendo del asistente.")
        break
    else:
        print("❌ Opción no válida. Intenta nuevamente.")
import tkinter as tk
from tkinter import ttk, messagebox

# =========================
# === LÓGICA DEL ÁRBOL ====
# =========================

# Clase Nodo: representa cada categoría en el árbol
class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre           # Nombre de la categoría
        self.hijos = []                # Lista de subcategorías (hijos)
        self.padre = None              # Referencia al nodo padre

    def agregar_subcategoria(self, subcategoria):
        subcategoria.padre = self      # Establece el nodo padre
        self.hijos.append(subcategoria)  # Añade la subcategoría a la lista de hijos

# Función para buscar nodos por coincidencia parcial de nombre (no sensible a mayúsculas)
def buscar_nodos_por_nombre(nodo, texto):
    resultado = []  # Lista para almacenar los nodos encontrados
    if texto.lower() in nodo.nombre.lower():  # Comparación sin distinguir mayúsculas
        resultado.append(nodo)
    for hijo in nodo.hijos:  # Buscar recursivamente en subcategorías
        resultado.extend(buscar_nodos_por_nombre(hijo, texto))  # extend es para añadir elementos de una lista a otra
    return resultado

# Función que devuelve la ruta completa desde la raíz hasta un nodo dado
def obtener_ruta_completa(nodo):
    ruta = []
    actual = nodo
    while actual:
        ruta.insert(0, actual.nombre)  # Agrega nombres al inicio para formar la ruta
        actual = actual.padre
    return " > ".join(ruta)

# Crear árbol base (raíz)
arbol_raiz = Nodo("Productos")

# Crear subcategorías manualmente
electronicos = Nodo("Electrónicos")
computadoras = Nodo("Computadoras")
laptops = Nodo("Laptops")
gaming = Nodo("Laptops para Juegos")
laptops.agregar_subcategoria(gaming)
computadoras.agregar_subcategoria(laptops)
electronicos.agregar_subcategoria(computadoras)

ropa = Nodo("Ropa")
hombre = Nodo("Hombre")
mujer = Nodo("Mujer")
ropa.agregar_subcategoria(hombre)
ropa.agregar_subcategoria(mujer)

# Añadir ramas al árbol raíz
arbol_raiz.agregar_subcategoria(electronicos)
arbol_raiz.agregar_subcategoria(ropa)

# Diccionario para mapear nodos visuales con nodos reales
id_map = {}

# ============================
# === INTERFAZ GRÁFICA (GUI) =
# ============================

def crear_interfaz():
    def mostrar_todo_en_treeview(tree, nodo, padre_id=""):
        # Inserta el nodo en el Treeview
        nodo_id = tree.insert(padre_id, "end", text=nodo.nombre, open=True)
        id_map[nodo_id] = nodo  # Guarda referencia al nodo real
        for hijo in nodo.hijos:  # Inserta recursivamente los hijos
            mostrar_todo_en_treeview(tree, hijo, nodo_id)

    def actualizar_info(nodo):
        # Muestra ruta completa y cantidad de subcategorías
        ruta = obtener_ruta_completa(nodo)
        cantidad = len(nodo.hijos)
        resultado_texto.set(f"Ruta: {ruta}\nSubcategorías: {cantidad}")

    def al_seleccionar(event):
        # Evento al hacer clic en un ítem del árbol
        item = tree.focus()
        if item:
            nodo = id_map.get(item)
            if nodo:
                actualizar_info(nodo)

    def buscar_categoria():
        # Función de búsqueda parcial desde la entrada
        entrada = entrada_busqueda.get().strip()
        if not entrada:
            messagebox.showwarning("Entrada vacía", "Por favor escribe una categoría.")
            return
        resultados = buscar_nodos_por_nombre(arbol_raiz, entrada)
        if not resultados:
            messagebox.showinfo("No encontrado", f"No se encontraron coincidencias para '{entrada}'.")
        else:
            sugerencias = "\n".join([obtener_ruta_completa(n) for n in resultados])
            messagebox.showinfo("Resultados encontrados", f"Coincidencias:\n{sugerencias}")

    def agregar_categoria():
        # Agrega una nueva categoría bajo un nodo existente
        padre_nombre = entrada_padre.get().strip()
        nueva_nombre = entrada_nueva.get().strip()

        if not padre_nombre or not nueva_nombre:
            messagebox.showwarning("Datos incompletos", "Completa ambos campos.")
            return

        resultados = buscar_nodos_por_nombre(arbol_raiz, padre_nombre)
        if not resultados:
            messagebox.showerror("Padre no encontrado", f"No se encontró la categoría '{padre_nombre}'.")
            return

        nuevo_nodo = Nodo(nueva_nombre)
        resultados[0].agregar_subcategoria(nuevo_nodo)

        # Refresca el árbol visual
        tree.delete(*tree.get_children())
        mostrar_todo_en_treeview(tree, arbol_raiz)
        messagebox.showinfo("Éxito", f"Se agregó '{nueva_nombre}' bajo '{padre_nombre}'.")

    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Árbol de Categorías de Productos")
    ventana.geometry("700x500")

    # Encabezado bonito del sistema
    encabezado = tk.Label(
        ventana,
        text="🌟 Sistema de Categorías de Productos 🌟",
        font=("Helvetica", 18, "bold"),
        fg="#2C3E50",
        bg="#ECF0F1",
        pady=15
    )
    encabezado.pack(fill="x")

    # Estilo moderno
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure("Treeview", font=("Arial", 11), rowheight=25)

    # Sección superior: búsqueda
    frame_top = tk.Frame(ventana)
    frame_top.pack(pady=10)

    tk.Label(frame_top, text="Buscar categoría:", font=("Arial", 12)).grid(row=0, column=0)
    entrada_busqueda = tk.Entry(frame_top, font=("Arial", 12), width=30)
    entrada_busqueda.grid(row=0, column=1, padx=5)
    tk.Button(frame_top, text="Buscar", command=buscar_categoria, bg="#007ACC", fg="white").grid(row=0, column=2)

    # Sección de agregar categoría
    frame_agregar = tk.Frame(ventana)
    frame_agregar.pack(pady=10)

    tk.Label(frame_agregar, text="Pertenece a:", font=("Arial", 12)).grid(row=0, column=0)
    entrada_padre = tk.Entry(frame_agregar, font=("Arial", 12), width=20)
    entrada_padre.grid(row=0, column=1, padx=5)

    tk.Label(frame_agregar, text="Nueva categoría:", font=("Arial", 12)).grid(row=0, column=2)
    entrada_nueva = tk.Entry(frame_agregar, font=("Arial", 12), width=20)
    entrada_nueva.grid(row=0, column=3, padx=5)

    tk.Button(frame_agregar, text="Agregar", command=agregar_categoria, bg="#28A745", fg="white").grid(row=0, column=4, padx=5)

    # Árbol visual interactivo
    tree = ttk.Treeview(ventana)
    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", al_seleccionar)

    # Texto inferior para mostrar ruta y cantidad de subcategorías
    resultado_texto = tk.StringVar()
    tk.Label(ventana, textvariable=resultado_texto, font=("Arial", 12), fg="gray").pack(pady=10)

    # Mostrar la estructura inicial del árbol
    mostrar_todo_en_treeview(tree, arbol_raiz)

    ventana.mainloop()  # Ejecutar la ventana

# ============================
# === FIN DE LA INTERFAZ =====
# ============================

# Ejecutar la GUI
crear_interfaz()
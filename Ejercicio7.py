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
        nodo_id = tree.insert(padre_id, "end", text=nodo.nombre, open=True)
        id_map[nodo_id] = nodo
        for hijo in nodo.hijos:
            mostrar_todo_en_treeview(tree, hijo, nodo_id)

    def actualizar_info(nodo):
        ruta = obtener_ruta_completa(nodo)
        cantidad = len(nodo.hijos)
        resultado_texto.set(f"Ruta: {ruta}\nSubcategorías: {cantidad}")

    def al_seleccionar(event):
        item = tree.focus()
        if item:
            nodo = id_map.get(item)
            if nodo:
                actualizar_info(nodo)

    def buscar_categoria():
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
        tree.delete(*tree.get_children())
        mostrar_todo_en_treeview(tree, arbol_raiz)
        messagebox.showinfo("Éxito", f"Se agregó '{nueva_nombre}' bajo '{padre_nombre}'.")

    # Ventana principal
    ventana = tk.Tk()
    ventana.title("Árbol de Categorías de Productos")
    ventana.geometry("800x600")
    ventana.configure(bg="#F7F9FB")

    # Encabezado
    encabezado = tk.Label(
        ventana,
        text="🌟 Sistema de Categorías de Productos 🌟",
        font=("Segoe UI", 20, "bold"),
        fg="#34495E",
        bg="#D6EAF8",
        pady=18
    )
    encabezado.pack(fill="x")

    # Marco principal con borde y fondo
    marco_principal = tk.Frame(ventana, bg="#F7F9FB", bd=2, relief="groove")
    marco_principal.pack(padx=20, pady=15, fill="both", expand=True)

    # Estilo moderno
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure("Treeview", font=("Segoe UI", 12), rowheight=28, background="#FDFEFE", fieldbackground="#FDFEFE")
    estilo.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"), background="#5DADE2", foreground="white")
    estilo.map("Treeview", background=[("selected", "#AED6F1")])

    # Sección superior: búsqueda
    frame_top = tk.Frame(marco_principal, bg="#F7F9FB")
    frame_top.pack(pady=10, fill="x")
    tk.Label(frame_top, text="🔎 Buscar categoría:", font=("Segoe UI", 12), bg="#F7F9FB").grid(row=0, column=0, sticky="w")
    entrada_busqueda = tk.Entry(frame_top, font=("Segoe UI", 12), width=30, bg="#EBF5FB")
    entrada_busqueda.grid(row=0, column=1, padx=7)
    tk.Button(frame_top, text="Buscar", command=buscar_categoria, bg="#2980B9", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2").grid(row=0, column=2, padx=5)

    # Línea divisoria
    tk.Frame(marco_principal, height=2, bg="#D6DBDF").pack(fill="x", pady=8)

    # Sección de agregar categoría
    frame_agregar = tk.Frame(marco_principal, bg="#F7F9FB")
    frame_agregar.pack(pady=10, fill="x")
    tk.Label(frame_agregar, text="📂 Pertenece a:", font=("Segoe UI", 12), bg="#F7F9FB").grid(row=0, column=0, sticky="e")
    entrada_padre = tk.Entry(frame_agregar, font=("Segoe UI", 12), width=18, bg="#EBF5FB")
    entrada_padre.grid(row=0, column=1, padx=5)
    tk.Label(frame_agregar, text="➕ Nueva categoría:", font=("Segoe UI", 12), bg="#F7F9FB").grid(row=0, column=2, sticky="e")
    entrada_nueva = tk.Entry(frame_agregar, font=("Segoe UI", 12), width=18, bg="#EBF5FB")
    entrada_nueva.grid(row=0, column=3, padx=5)
    tk.Button(frame_agregar, text="Agregar", command=agregar_categoria, bg="#27AE60", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2").grid(row=0, column=4, padx=8)

    # Línea divisoria
    tk.Frame(marco_principal, height=2, bg="#D6DBDF").pack(fill="x", pady=8)

    # Árbol visual interactivo
    tree_frame = tk.Frame(marco_principal, bg="#F7F9FB")
    tree_frame.pack(fill="both", expand=True, pady=5)
    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")
    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree.pack(fill="both", expand=True)
    tree_scroll.config(command=tree.yview)
    tree.bind("<<TreeviewSelect>>", al_seleccionar)

    # Texto inferior para mostrar ruta y cantidad de subcategorías
    resultado_texto = tk.StringVar()
    info_frame = tk.Frame(marco_principal, bg="#F7F9FB")
    info_frame.pack(pady=10, fill="x")
    tk.Label(info_frame, textvariable=resultado_texto, font=("Segoe UI", 12, "italic"), fg="#616A6B", bg="#F7F9FB").pack()

    # Mostrar la estructura inicial del árbol
    mostrar_todo_en_treeview(tree, arbol_raiz)

    # Mensaje de bienvenida
    resultado_texto.set("Selecciona una categoría para ver su ruta y subcategorías.")

    ventana.mainloop()

# ============================
# === FIN DE LA INTERFAZ =====
# ============================

# Ejecutar la GUI
crear_interfaz()
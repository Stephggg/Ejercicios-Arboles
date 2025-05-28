import tkinter as tk
from tkinter import ttk, messagebox

# =========================
# LÓGICA DEL ÁRBOL DOM HTML
# =========================

# Clase para representar un nodo del árbol DOM (una etiqueta HTML)
class NodoHTML:
    def __init__(self, nombre, atributos=None, hijos=None):
        self.nombre = nombre  # Nombre de la etiqueta (ej: 'div', 'p', 'body')
        self.atributos = atributos if atributos else {}  # Diccionario de atributos
        self.hijos = hijos if hijos else []  # Lista de nodos hijos

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

# Función recursiva para buscar etiquetas y sus rutas en el árbol DOM
def buscar_etiquetas_con_ruta(raiz, nombre_busqueda, ruta_actual=None):
    if ruta_actual is None:
        ruta_actual = []
    encontrados = []
    nueva_ruta = ruta_actual + [raiz.nombre]  # Se agrega el nombre actual a la ruta
    # Si el nombre coincide, se agrega el nodo y su ruta a la lista de encontrados
    if raiz.nombre.lower() == nombre_busqueda.lower():
        encontrados.append((raiz, nueva_ruta))
    # Se busca recursivamente en los hijos
    for hijo in raiz.hijos:
        encontrados.extend(buscar_etiquetas_con_ruta(hijo, nombre_busqueda, nueva_ruta))
    return encontrados

# =========================
# LÓGICA DE CONSTRUCCIÓN DEL ÁRBOL DE EJEMPLO
# =========================

# Se crean los nodos para cada etiqueta HTML
arbol_html = NodoHTML("html")
head = NodoHTML("head")
title = NodoHTML("title")
body = NodoHTML("body")
div1 = NodoHTML("div", {"class": "container"})
p = NodoHTML("p", {"id": "parrafo1"})
div2 = NodoHTML("div", {"class": "footer"})
span = NodoHTML("span")

'''
Estructura del árbol HTML construido:
<html>
    <head>
        <title>Ejemplo de Árbol HTML</title>
    </head>
    <body>
        <div class="container">
            <p id="parrafo1">Este es un párrafo dentro de un div.</p>
        </div>
        <div class="footer">
            <span>Este es un span dentro del footer.</span>
        </div>
    </body>
'''

# Se construye la jerarquía del árbol agregando los hijos a cada nodo
arbol_html.agregar_hijo(head)
head.agregar_hijo(title)
arbol_html.agregar_hijo(body)
body.agregar_hijo(div1)
div1.agregar_hijo(p)
body.agregar_hijo(div2)
div2.agregar_hijo(span)

# =========================
# INTERFAZ GRÁFICA (Tkinter)
# =========================

# Función para mostrar los resultados en la interfaz
def mostrar_resultados():
    etiqueta = entrada_etiqueta.get().strip()
    # Validación: el campo no puede estar vacío
    if not etiqueta:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de etiqueta.")
        return
    # Validación: solo letras y números permitidos en el nombre de la etiqueta
    if not etiqueta.isalnum():
        messagebox.showerror("Error", "El nombre de la etiqueta solo puede contener letras y números.")
        return
    # Buscar etiquetas en el árbol DOM (con rutas)
    resultados = buscar_etiquetas_con_ruta(arbol_html, etiqueta)
    # Limpiar el área de resultados
    texto_resultados.config(state='normal')
    texto_resultados.delete(1.0, tk.END)
    if resultados:
        texto_resultados.insert(tk.END, f"Se encontraron {len(resultados)} etiqueta(s) <{etiqueta}>:\n\n")
        for idx, (nodo, ruta) in enumerate(resultados, 1):
            ruta_str = " / ".join(ruta)
            texto_resultados.insert(tk.END, f"{idx}. Ruta: {ruta_str}\n   <{nodo.nombre}")
            if nodo.atributos:
                attrs = " ".join(f'{k}="{v}"' for k, v in nodo.atributos.items())
                texto_resultados.insert(tk.END, f" {attrs}")
            texto_resultados.insert(tk.END, ">\n\n")
    else:
        texto_resultados.insert(tk.END, "No se encontraron etiquetas con ese nombre.")
    texto_resultados.config(state='disabled')

# --- Creación de la ventana principal ---
ventana = tk.Tk()
ventana.title("Buscador de Etiquetas HTML")
ventana.geometry("540x430")
ventana.resizable(False, False)
ventana.configure(bg="#f0f4f8")

# --- Título de la ventana ---
titulo = tk.Label(ventana, text="Buscador de Etiquetas en Árbol HTML", font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#333")
titulo.pack(pady=15)

# --- Marco para la entrada y el botón ---
frame_entrada = tk.Frame(ventana, bg="#f0f4f8")
frame_entrada.pack(pady=10)

# Etiqueta para el campo de entrada
lbl_etiqueta = tk.Label(frame_entrada, text="Nombre de la etiqueta:", font=("Arial", 12), bg="#f0f4f8")
lbl_etiqueta.grid(row=0, column=0, padx=5, pady=5)

# Campo de entrada para el nombre de la etiqueta
entrada_etiqueta = ttk.Entry(frame_entrada, font=("Arial", 12), width=20)
entrada_etiqueta.grid(row=0, column=1, padx=5, pady=5)

# Botón para buscar la etiqueta
btn_buscar = ttk.Button(frame_entrada, text="Buscar", command=mostrar_resultados)
btn_buscar.grid(row=0, column=2, padx=5, pady=5)

# --- Área de resultados ---
lbl_resultados = tk.Label(ventana, text="Resultados:", font=("Arial", 12, "bold"), bg="#f0f4f8")
lbl_resultados.pack(pady=(20, 5))

# Caja de texto para mostrar los resultados de la búsqueda
texto_resultados = tk.Text(ventana, height=13, width=65, font=("Consolas", 11), state='disabled', bg="#e9ecef")
texto_resultados.pack(pady=5)

# --- Pie de página ---
footer = tk.Label(ventana, text="Ejercicio 8 - Estructura de Documento HTML/XML", font=("Arial", 9), bg="#f0f4f8", fg="#888")
footer.pack(side="bottom", pady=10)

# --- Iniciar el bucle principal de la interfaz ---
ventana.mainloop()
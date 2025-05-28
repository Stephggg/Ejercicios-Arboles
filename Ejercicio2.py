import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Clase base para elementos del sistema de archivos (directorio o archivo)
class ElementoFS:
    def __init__(self, nombre):
        self.nombre = nombre  # Nombre del elemento

# Clase para archivos, hereda de ElementoFS
class Archivo(ElementoFS):
    def __init__(self, nombre):
        super().__init__(nombre)  # Inicializa con el nombre

# Clase para directorios, hereda de ElementoFS
class Directorio(ElementoFS):
    def __init__(self, nombre):
        super().__init__(nombre)  # Inicializa con el nombre
        self.hijos = []           # Lista de hijos (archivos o directorios)

    def agregar(self, elemento):
        self.hijos.append(elemento)  # Agrega un hijo al directorio

# Busca la ruta completa de un elemento (archivo o directorio) dado su nombre, recorriendo el árbol desde la raíz
def buscar_ruta_elemento(raiz, nombre_elemento, ruta_actual=""):
    # Si el nodo actual coincide con el nombre buscado (ya sea archivo o directorio)
    if raiz.nombre == nombre_elemento:
        return ruta_actual + "/" + raiz.nombre if raiz.nombre else "/"
    # Si es un directorio, buscar recursivamente en sus hijos
    if isinstance(raiz, Directorio):
        for hijo in raiz.hijos:
            resultado = buscar_ruta_elemento(hijo, nombre_elemento, ruta_actual + "/" + raiz.nombre)
            if resultado:
                return resultado
    return None

# Llena el widget Treeview con la estructura del árbol de directorios y archivos
def llenar_treeview(tree, nodo, padre=""):
    """Llena el Treeview con la estructura del árbol."""
    if isinstance(nodo, Directorio):
        # Inserta el directorio en el Treeview (si el nombre es vacío, muestra 'raiz')
        item_id = tree.insert(padre, "end", text=nodo.nombre if nodo.nombre else "raiz", open=True)
        for hijo in nodo.hijos:
            llenar_treeview(tree, hijo, item_id)  # Llama recursivamente para los hijos
    elif isinstance(nodo, Archivo):
        # Inserta el archivo en el Treeview
        tree.insert(padre, "end", text=nodo.nombre, open=True)

# Función que se ejecuta al presionar el botón "Buscar"
def buscar_archivo_gui():
    nombre = entry_nombre.get()  # Obtiene el nombre del archivo ingresado por el usuario
    ruta = buscar_ruta_elemento(raiz, nombre)  # Busca la ruta del archivo
    if ruta:
        messagebox.showinfo("Resultado", f"Ruta encontrada:\n{ruta}")  # Muestra la ruta encontrada
    else:
        messagebox.showwarning("Resultado", "Elemento no encontrado.")  # Muestra advertencia si no se encuentra

# Ejemplo de uso:
if __name__ == "__main__":
    # Crear estructura de directorios y archivos (árbol)
    raiz = Directorio("")  # Directorio raíz

    home = Directorio("home")  # /home
    usuario = Directorio("usuario")  # /home/usuario
    documentos = Directorio("documentos")  # /home/usuario/documentos
    informe = Archivo("informe.txt")  # /home/usuario/documentos/informe.txt
    imagen = Archivo("foto.jpg")  # /home/usuario/foto.jpg

    documentos.agregar(informe)  # Agrega informe.txt a documentos
    usuario.agregar(documentos)  # Agrega documentos a usuario
    usuario.agregar(imagen)      # Agrega foto.jpg a usuario
    home.agregar(usuario)        # Agrega usuario a home
    raiz.agregar(home)           # Agrega home a la raíz



     # ------------------------Interfaz gráfica mejorada con Treeview--------------------------------------
    
    ventana = tk.Tk()  # Crea la ventana principal
    ventana.title("Buscador de Archivos")  # Título de la ventana
    ventana.geometry("600x300")  # Tamaño de la ventana
    ventana.configure(bg="#f0f4f7")  # Color de fondo

    # Frame principal con borde y color de fondo
    frame = tk.Frame(ventana, bg="#e3eaf2", bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=570, height=260)

    # Título en la parte superior del frame
    titulo = tk.Label(frame, text="Buscar archivo en sistema de archivos", font=("Arial", 14, "bold"), bg="#e3eaf2")
    titulo.pack(pady=(10, 5))

    # Subframe para contener el árbol y el panel de búsqueda
    subframe = tk.Frame(frame, bg="#e3eaf2")
    subframe.pack(fill="both", expand=True, padx=10, pady=5)

    # Treeview para mostrar el árbol de directorios y archivos
    tree = ttk.Treeview(subframe)
    tree.pack(side="left", fill="y", padx=(0, 10), pady=5)
    llenar_treeview(tree, raiz)  # Llena el Treeview con la estructura del árbol

    # Panel de búsqueda a la derecha del árbol
    panel_busqueda = tk.Frame(subframe, bg="#e3eaf2")
    panel_busqueda.pack(side="left", fill="both", expand=True)

    # Etiqueta y campo de entrada para el nombre del archivo
    tk.Label(panel_busqueda, text="Nombre del archivo:", font=("Arial", 11), bg="#e3eaf2").pack(pady=5)
    entry_nombre = tk.Entry(panel_busqueda, font=("Arial", 11), width=30)
    entry_nombre.pack(pady=5)

    # Botón para buscar el archivo
    btn_buscar = tk.Button(panel_busqueda, text="Buscar", font=("Arial", 11, "bold"), bg="#4a90e2", fg="white", command=buscar_archivo_gui)
    btn_buscar.pack(pady=15)

    ventana.mainloop()  # Inicia el bucle principal de la interfaz gráfica
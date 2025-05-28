import tkinter as tk
from tkinter import ttk, messagebox
import math

# ==========================
# BLOQUE DE LÓGICA DEL CDN
# ==========================

# ----- Clase que representa un servidor en el árbol -----
class Servidor:
    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre              # Nombre del servidor
        self.latitud = latitud            # Latitud geográfica
        self.longitud = longitud          # Longitud geográfica
        self.hijos = []                   # Lista de servidores hijos (subservidores)
        self.padre = None                 # Referencia al servidor padre (para trazar rutas)

    def agregar_hijo(self, servidor):
        servidor.padre = self             # Asigna este servidor como padre del hijo
        self.hijos.append(servidor)       # Agrega el hijo a la lista

# ----- Calcula la distancia euclidiana entre dos ubicaciones -----
def distancia(lat1, lon1, lat2, lon2):
    # Fórmula simple para distancia en un plano (no es la distancia real sobre la Tierra)
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# ----- Busca los k servidores más cercanos a una ubicación dada -----
def servidores_mas_cercanos(raiz, lat_user, lon_user, k=3):
    servidores_distancias = []
    # Función interna recursiva para recorrer todo el árbol
    def buscar(nodo):
        d = distancia(lat_user, lon_user, nodo.latitud, nodo.longitud)
        servidores_distancias.append((d, nodo))
        for hijo in nodo.hijos:
            buscar(hijo)
    buscar(raiz)
    servidores_distancias.sort(key=lambda x: x[0])  # Ordena por distancia
    return [s[1] for s in servidores_distancias[:k]] # Devuelve los k más cercanos

# ----- Busca servidores por nombre (puede haber varios con el mismo nombre) -----
def buscar_por_nombre(raiz, nombre):
    resultado = []
    def buscar(nodo):
        if nodo.nombre.lower() == nombre.lower():
            resultado.append(nodo)
        for hijo in nodo.hijos:
            buscar(hijo)
    buscar(raiz)
    return resultado

# ----- Obtiene la ruta desde la raíz hasta un servidor -----
def obtener_ruta(servidor):
    ruta = []
    actual = servidor
    while actual:
        ruta.insert(0, actual.nombre)  # Inserta al inicio para que quede de raíz a hoja
        actual = actual.padre
    return " → ".join(ruta)

# ----- Muestra el árbol de servidores en un Treeview de Tkinter -----
def mostrar_arbol(tree, nodo, parent=""):
    # Inserta el nodo actual en el Treeview
    item_id = tree.insert(parent, "end", text=nodo.nombre,
                          values=(nodo.latitud, nodo.longitud))
    # Llama recursivamente para cada hijo
    for hijo in nodo.hijos:
        mostrar_arbol(tree, hijo, item_id)

# ==========================
# BLOQUE DE INTERFAZ GRÁFICA
# ==========================
def crear_interfaz():
    historial = []  # Guarda el historial de búsquedas (solo para mostrar en consola)

    # ---- Menú principal con botones para cada función ----
    def mostrar_menu_principal():
        for widget in ventana.winfo_children():
            widget.destroy()
        tk.Label(
            ventana, text="🌐 Bienvenido al Sistema CDN 🌐",
            font=("Segoe UI", 18, "bold"), bg="#e3f0fa", fg="#1976d2"
        ).pack(pady=20)
        tk.Button(
            ventana, text="🔍 Buscar Servidores más Cercanos", font=("Segoe UI", 13, "bold"), width=40,
            bg="#42a5f5", fg="white", activebackground="#1976d2", activeforeground="white",
            relief="raised", bd=3, cursor="hand2", command=mostrar_busqueda_cercanos
        ).pack(pady=12)
        tk.Button(
            ventana, text="📌 Buscar Servidor por Nombre", font=("Segoe UI", 13, "bold"), width=40,
            bg="#66bb6a", fg="white", activebackground="#388e3c", activeforeground="white",
            relief="raised", bd=3, cursor="hand2", command=mostrar_busqueda_nombre
        ).pack(pady=12)
        tk.Button(
            ventana, text="🗂️ Ver Árbol de Servidores", font=("Segoe UI", 13, "bold"), width=40,
            bg="#ffa726", fg="white", activebackground="#f57c00", activeforeground="white",
            relief="raised", bd=3, cursor="hand2", command=mostrar_arbol_servidores
        ).pack(pady=12)

    # ---- Pantalla para buscar los 3 servidores más cercanos a una ubicación ----
    def mostrar_busqueda_cercanos():
        for widget in ventana.winfo_children():
            widget.destroy()
        encabezado = tk.Label(
            ventana,
            text="Buscar los 3 servidores más cercanos según tu ubicación",
            font=("Segoe UI", 15, "bold"), bg="#e3f0fa", fg="#1976d2"
        )
        encabezado.pack(pady=10)
        frame_inputs = tk.Frame(ventana, bg="#e3f0fa")
        frame_inputs.pack(pady=10)
        ttk.Label(frame_inputs, text="Latitud:", font=("Segoe UI", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_lat = ttk.Entry(frame_inputs, font=("Segoe UI", 11))
        entry_lat.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_inputs, text="Longitud:", font=("Segoe UI", 11)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_lon = ttk.Entry(frame_inputs, font=("Segoe UI", 11))
        entry_lon.grid(row=1, column=1, padx=5, pady=5)
        resultado_var = tk.StringVar()
        resultado_label = tk.Label(
            ventana, textvariable=resultado_var, font=("Segoe UI", 12), bg="#e3f0fa", fg="#222"
        )
        resultado_label.pack(pady=15)
        # Función que se ejecuta al presionar "Buscar"
        def buscar():
            try:
                lat = float(entry_lat.get())
                lon = float(entry_lon.get())
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores válidos para latitud y longitud.")
                return
            servidores = servidores_mas_cercanos(servidor_central, lat, lon)
            resultado = "\n".join([
                f"🌍 {i+1}. {s.nombre} (Lat: {s.latitud}, Lon: {s.longitud})"
                for i, s in enumerate(servidores)
            ])
            resultado_var.set(f"Servidores más cercanos:\n{resultado}")
            historial.append(f"Usuario en ({lat}, {lon}) → {[s.nombre for s in servidores]}")
            actualizar_historial()
        tk.Button(
            ventana, text="Buscar", command=buscar, font=("Segoe UI", 11, "bold"),
            bg="#1976d2", fg="white", activebackground="#1565c0", activeforeground="white",
            relief="raised", bd=2, cursor="hand2", width=15
        ).pack(pady=5)
        tk.Button(
            ventana, text="Volver al Menú", command=mostrar_menu_principal, font=("Segoe UI", 11),
            bg="#bdbdbd", fg="#222", activebackground="#757575", activeforeground="white",
            relief="raised", bd=2, cursor="hand2", width=15
        ).pack(pady=5)

    # ---- Pantalla para buscar un servidor por su nombre ----
    def mostrar_busqueda_nombre():
        for widget in ventana.winfo_children():
            widget.destroy()
        encabezado = tk.Label(
            ventana,
            text="Buscar Servidor por Nombre",
            font=("Segoe UI", 15, "bold"), bg="#e3f0fa", fg="#388e3c"
        )
        encabezado.pack(pady=10)
        frame_inputs = tk.Frame(ventana, bg="#e3f0fa")
        frame_inputs.pack(pady=10)
        ttk.Label(frame_inputs, text="Nombre del servidor:", font=("Segoe UI", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_nombre = ttk.Entry(frame_inputs, font=("Segoe UI", 11))
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        resultado_var = tk.StringVar()
        resultado_label = tk.Label(
            ventana, textvariable=resultado_var, font=("Segoe UI", 12), bg="#e3f0fa", fg="#222"
        )
        resultado_label.pack(pady=15)
        # Función que se ejecuta al presionar "Buscar"
        def buscar():
            nombre = entry_nombre.get()
            encontrados = buscar_por_nombre(servidor_central, nombre)
            if not encontrados:
                resultado_var.set("❌ Servidor no encontrado.")
            else:
                servidor = encontrados[0]
                ruta = obtener_ruta(servidor)
                resultado_var.set(
                    f"✅ Nombre: {servidor.nombre}\n"
                    f"📍 Latitud: {servidor.latitud}\n"
                    f"📍 Longitud: {servidor.longitud}\n"
                    f"🛣️ Ruta: {ruta}"
                )
        tk.Button(
            ventana, text="Buscar", command=buscar, font=("Segoe UI", 11, "bold"),
            bg="#388e3c", fg="white", activebackground="#1b5e20", activeforeground="white",
            relief="raised", bd=2, cursor="hand2", width=15
        ).pack(pady=5)
        tk.Button(
            ventana, text="Volver al Menú", command=mostrar_menu_principal, font=("Segoe UI", 11),
            bg="#bdbdbd", fg="#222", activebackground="#757575", activeforeground="white",
            relief="raised", bd=2, cursor="hand2", width=15
        ).pack(pady=5)

    # ---- Pantalla para mostrar el árbol de servidores en forma jerárquica ----
    def mostrar_arbol_servidores():
        for widget in ventana.winfo_children():
            widget.destroy()
        tk.Label(
            ventana, text="Árbol de Servidores", font=("Segoe UI", 15, "bold"),
            bg="#e3f0fa", fg="#ffa726"
        ).pack(pady=10)
        tree_frame = tk.Frame(ventana, bg="#e3f0fa")
        tree_frame.pack(pady=10, fill="both", expand=True)
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        tree = ttk.Treeview(tree_frame, columns=("Latitud", "Longitud"), selectmode="browse")
        tree.heading("#0", text="Servidor")
        tree.heading("Latitud", text="Latitud")
        tree.heading("Longitud", text="Longitud")
        tree.column("#0", width=180)
        tree.column("Latitud", width=100, anchor="center")
        tree.column("Longitud", width=100, anchor="center")
        tree.pack(fill="both", expand=True)
        mostrar_arbol(tree, servidor_central)
        tk.Button(
            ventana, text="Volver al Menú", command=mostrar_menu_principal, font=("Segoe UI", 11),
            bg="#bdbdbd", fg="#222", activebackground="#757575", activeforeground="white",
            relief="raised", bd=2, cursor="hand2", width=15
        ).pack(pady=10)

    # ---- Muestra el historial de búsquedas en la consola ----
    def actualizar_historial():
        print("Historial de Búsquedas:")
        for h in historial[-10:]:
            print(h)

    # ---- Configuración de la ventana principal ----
    ventana = tk.Tk()
    ventana.title("Sistema de CDN")
    ventana.geometry("750x540")
    ventana.configure(bg="#e3f0fa")
    ventana.resizable(False, False)
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("TFrame", background="#e3f0fa")
    estilo.configure("TButton", font=("Segoe UI", 11), padding=6)
    estilo.configure("TLabel", font=("Segoe UI", 11), background="#e3f0fa")
    mostrar_menu_principal()
    ventana.mainloop()

# ==========================
# BLOQUE DE CREACIÓN DEL ÁRBOL
# ==========================
# Crea la estructura jerárquica de servidores (central, regionales y locales)
servidor_central = Servidor("Central", 0, 0)
usa = Servidor("USA", 10, -100)
europa = Servidor("Europa", 50, 10)
asia = Servidor("Asia", 30, 120)
servidor_central.agregar_hijo(usa)
servidor_central.agregar_hijo(europa)
servidor_central.agregar_hijo(asia)
ny = Servidor("Nueva York", 12, -90)
la = Servidor("Los Ángeles", 9, -120)
paris = Servidor("París", 48, 2)
madrid = Servidor("Madrid", 40, -4)
beijing = Servidor("Beijing", 39, 116)
tokyo = Servidor("Tokio", 35, 139)
usa.agregar_hijo(ny)
usa.agregar_hijo(la)
europa.agregar_hijo(paris)
europa.agregar_hijo(madrid)
asia.agregar_hijo(beijing)
asia.agregar_hijo(tokyo)

# ==========================
# EJECUCIÓN DE LA INTERFAZ
# ==========================
crear_interfaz()
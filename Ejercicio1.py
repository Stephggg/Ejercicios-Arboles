import tkinter as tk
from tkinter import messagebox

# Clase que representa a un empleado
class Empleado:
    def __init__(self, nombre, puesto):
        # Valida que el nombre y el puesto sean cadenas no vacías
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del empleado debe ser una cadena no vacía.")
        if not isinstance(puesto, str) or not puesto.strip():
            raise ValueError("El puesto del empleado debe ser una cadena no vacía.")   # raise sirve para lanzar excepciones
        self.nombre = nombre.strip()   # Guarda el nombre del empleado
        self.puesto = puesto.strip()   # Guarda el puesto del empleado

# Nodo del árbol jerárquico, cada nodo es un empleado y sus subordinados
class NodoEmpleado:
    def __init__(self, empleado):
        # Valida que el argumento sea un objeto Empleado
        if not isinstance(empleado, Empleado):   #insistance verifica el tipo de un objeto
            raise TypeError("Debe recibir un objeto Empleado.")
        self.empleado = empleado           # Objeto Empleado asociado al nodo
        self.subordinados = []             # Lista de nodos subordinados

    # Agrega un subordinado a este nodo
    def agregar_subordinado(self, nodo_subordinado):
        if not isinstance(nodo_subordinado, NodoEmpleado):
            raise TypeError("Solo se pueden agregar nodos de tipo NodoEmpleado.")
        self.subordinados.append(nodo_subordinado)  # Añade el subordinado a la lista

    # Busca un empleado por nombre en el subárbol de este nodo
    def buscar(self, nombre):
        if self.empleado.nombre == nombre:
            return self  # Si el nombre coincide, retorna el nodo actual
        for sub in self.subordinados:
            encontrado = sub.buscar(nombre)  # Busca recursivamente en los subordinados
            if encontrado:
                return encontrado
        return None  # Si no se encuentra, retorna None

# Función para calcular cuántos niveles hay entre el CEO y un empleado dado
def niveles_bajo_ceo(raiz, nombre_empleado):
    if not isinstance(raiz, NodoEmpleado):
        raise TypeError("La raíz debe ser un NodoEmpleado.")
    if not isinstance(nombre_empleado, str) or not nombre_empleado.strip():
        raise ValueError("El nombre del empleado debe ser una cadena no vacía.")

    # Función recursiva para buscar el nivel del empleado
    def buscar_niveles(nodo, nombre, nivel):
        if nodo.empleado.nombre == nombre:
            return nivel  # Si encuentra el empleado, retorna el nivel actual
        for sub in nodo.subordinados:
            resultado = buscar_niveles(sub, nombre, nivel + 1)  # Busca en los subordinados aumentando el nivel
            if resultado is not None:
                return resultado
        return None  # Si no se encuentra, retorna None

    niveles = buscar_niveles(raiz, nombre_empleado.strip(), 0)  # Inicia la búsqueda desde el nivel 0 (CEO)
    if niveles is None:
        raise ValueError(f"Empleado '{nombre_empleado}' no encontrado en la jerarquía.")
    return niveles  # Retorna el número de niveles bajo el CEO

# Clase principal de la aplicación con interfaz gráfica
class JerarquiaApp:
    def __init__(self):
        self.raiz_jerarquia = None  # Nodo raíz del árbol (CEO)
        self.window = tk.Tk()  # Ventana principal de la aplicación
        self.window.title("Jerarquía Organizacional")
        self.window.configure(bg="#f0f4f8")  # Color de fondo

        # Encabezado de la ventana
        header = tk.Label(self.window, text="Jerarquía Organizacional", font=("Arial Rounded MT Bold", 20, "bold"), bg="#4f8cff", fg="white", pady=10)
        header.pack(fill=tk.X)

        # Área de texto con scroll para mostrar la jerarquía
        text_frame = tk.Frame(self.window, bg="#f0f4f8")
        text_frame.pack(pady=10)
        self.tree = tk.Text(text_frame, width=55, height=16, font=("Consolas", 12), bg="#eaf1fb", fg="#222", bd=2, relief="groove")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = tk.Scrollbar(text_frame, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scroll.set)

        # Formulario para agregar empleados
        frame = tk.LabelFrame(self.window, text="Agregar Empleado", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#4f8cff", bd=2, relief="ridge", padx=10, pady=10)
        frame.pack(pady=5)

        tk.Label(frame, text="Nombre Empleado:", font=("Arial", 11), bg="#f0f4f8").grid(row=0, column=0, sticky="e", pady=2)
        self.entry_nombre = tk.Entry(frame, font=("Arial", 12), bg="#fff")
        self.entry_nombre.grid(row=0, column=1, pady=2)

        tk.Label(frame, text="Puesto:", font=("Arial", 11), bg="#f0f4f8").grid(row=1, column=0, sticky="e", pady=2)
        self.entry_puesto = tk.Entry(frame, font=("Arial", 12), bg="#fff")
        self.entry_puesto.grid(row=1, column=1, pady=2)

        tk.Label(frame, text="Jefe Directo (vacío si es CEO):", font=("Arial", 11), bg="#f0f4f8").grid(row=2, column=0, sticky="e", pady=2)
        self.entry_jefe = tk.Entry(frame, font=("Arial", 12), bg="#fff")
        self.entry_jefe.grid(row=2, column=1, pady=2)

        self.btn_agregar = tk.Button(frame, text="Agregar Empleado", command=self.agregar_empleado, bg="#4f8cff", fg="white", font=("Arial", 11, "bold"), relief="raised", bd=2, cursor="hand2", activebackground="#356ac3")
        self.btn_agregar.grid(row=3, column=0, columnspan=2, pady=8)

        # Área para consultar niveles bajo el CEO
        consulta_frame = tk.Frame(self.window, bg="#f0f4f8")
        consulta_frame.pack(pady=10)

        self.entry_consulta = tk.Entry(consulta_frame, font=("Arial", 12), width=30, bg="#fff")
        self.entry_consulta.pack(side=tk.LEFT, padx=5)
        self.entry_consulta.insert(0, "Nombre del empleado a consultar")

        self.button = tk.Button(consulta_frame, text="Consultar niveles bajo CEO", command=self.consultar_niveles, bg="#4f8cff", fg="white", font=("Arial", 11, "bold"), relief="raised", bd=2, cursor="hand2", activebackground="#356ac3")
        self.button.pack(side=tk.LEFT, padx=5)

    # Muestra la jerarquía en el área de texto, incluyendo el nivel
    def mostrar_jerarquia(self):
        self.tree.delete(1.0, tk.END)  # Limpia el área de texto
        def recorrer(nodo, nivel):
            # Inserta el nombre, puesto y nivel del empleado con indentación según el nivel
            color = "#4f8cff" if nivel == 0 else "#222"
            self.tree.insert(
                tk.END,
                f"{'  '*nivel}● {nodo.empleado.nombre} ({nodo.empleado.puesto}) [Nivel: {nivel}]\n"
            )
            for sub in nodo.subordinados:
                recorrer(sub, nivel + 1)  # Llama recursivamente para los subordinados
        if self.raiz_jerarquia:
            recorrer(self.raiz_jerarquia, 0)

    # Lógica para agregar un empleado a la jerarquía
    def agregar_empleado(self):
        nombre = self.entry_nombre.get().strip()  # Obtiene el nombre ingresado
        puesto = self.entry_puesto.get().strip()  # Obtiene el puesto ingresado
        jefe = self.entry_jefe.get().strip()      # Obtiene el jefe directo ingresado
        if not nombre or not puesto:
            messagebox.showerror("Error", "Por favor, ingresa el nombre y el puesto del empleado.")
            return
        # Verifica si ya existe alguien con ese nombre
        if self.raiz_jerarquia and self.raiz_jerarquia.buscar(nombre):
            messagebox.showerror("Error", f"Ya existe un empleado con el nombre '{nombre}'.")
            return
        try:
            nuevo = NodoEmpleado(Empleado(nombre, puesto))  # Crea el nuevo nodo empleado
            if not jefe:
                # Si no hay jefe, este empleado será el CEO (raíz)
                if self.raiz_jerarquia is not None:
                    messagebox.showerror("Error", "Ya existe un CEO.")
                    return
                self.raiz_jerarquia = nuevo
            else:
                # Si hay jefe, lo buscamos y lo agregamos como subordinado
                if self.raiz_jerarquia is None:
                    messagebox.showerror("Error", "Primero debes agregar al CEO.")
                    return
                jefe_nodo = self.raiz_jerarquia.buscar(jefe)
                if jefe_nodo is None:
                    messagebox.showerror("Error", f"No se encontró al jefe '{jefe}'.")
                    return
                jefe_nodo.agregar_subordinado(nuevo)
            self.mostrar_jerarquia()  # Actualiza la visualización de la jerarquía
            self.entry_nombre.delete(0, tk.END)  # Limpia los campos del formulario
            self.entry_puesto.delete(0, tk.END)
            self.entry_jefe.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Lógica para consultar cuántos niveles hay entre el CEO y un empleado
    def consultar_niveles(self):
        nombre = self.entry_consulta.get().strip()  # Obtiene el nombre a consultar
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre.")
            return
        if not self.raiz_jerarquia:
            messagebox.showerror("Error", "No hay empleados en la jerarquía.")
            return
        try:
            niveles = niveles_bajo_ceo(self.raiz_jerarquia, nombre)  # Calcula los niveles bajo el CEO
            nodo = self.raiz_jerarquia.buscar(nombre)  # Busca el nodo del empleado
            if nodo:
                puesto = nodo.empleado.puesto
                messagebox.showinfo(
                    "Resultado",
                    f"{nombre} ({puesto}) está en el nivel {niveles} debajo del CEO."
                )
            else:
                messagebox.showerror("Error", f"No se encontró al empleado '{nombre}'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Inicia la aplicación gráfica
    def run(self):
        self.window.mainloop()

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = JerarquiaApp()
    app.run()
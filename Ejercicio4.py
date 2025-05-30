import tkinter as tk
from tkinter import messagebox, ttk

# Clase Persona representa un nodo en el árbol genealógico
class Persona:
    def __init__(self, nombre, padre=None, madre=None):
        # Nombre de la persona (string)
        self.nombre = nombre
        # Padre y madre son objetos Persona o None
        self.padre = padre
        self.madre = madre

    def __str__(self):
        return self.nombre

# Función para encontrar ancestros en una generación específica
def encontrar_ancestros(persona, generacion):
    """
    Retorna una lista de nombres de ancestros en la generación indicada.
    generacion=1: padres, generacion=2: abuelos, generacion=3: bisabuelos, etc.
    """
    if persona is None or generacion < 1:
        return []
    if generacion == 1:
        # Retorna los padres si existen
        return [p.nombre for p in [persona.padre, persona.madre] if p]
    # Recursivamente busca en la generación anterior
    ancestros = []
    for p in [persona.padre, persona.madre]:
        if p:
            ancestros.extend(encontrar_ancestros(p, generacion - 1))  #-1 es # para ir hacia arriba en el árbol
    return ancestros # extend sirve para añadir los elementos de una lista a otra

# Clase principal para la interfaz gráfica
class ArbolGenealogicoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Árbol Genealógico - Presentación Final")
        self.geometry("600x650")  # Antes: 600x500
        self.configure(bg="#f0f4f8")
        self.resizable(False, False)

        # Diccionario para almacenar personas por nombre
        self.personas = {}

        # Llama a la función para construir la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(self, text="Árbol Genealógico", font=("Arial Rounded MT Bold", 24), bg="#f0f4f8", fg="#2d415a")
        titulo.pack(pady=20)

        # Marco para agregar personas
        marco_agregar = tk.LabelFrame(self, text="Agregar Persona", bg="#e3eaf2", font=("Arial", 12, "bold"))
        marco_agregar.pack(padx=20, pady=10, fill="x")

        # Entrada para nombre
        tk.Label(marco_agregar, text="Nombre:", bg="#e3eaf2").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entrada_nombre = tk.Entry(marco_agregar, width=20)
        self.entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Combobox para seleccionar padre
        tk.Label(marco_agregar, text="Padre:", bg="#e3eaf2").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_padre = ttk.Combobox(marco_agregar, values=[], state="readonly", width=18)
        self.combo_padre.grid(row=1, column=1, padx=5, pady=5)

        # Combobox para seleccionar madre
        tk.Label(marco_agregar, text="Madre:", bg="#e3eaf2").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combo_madre = ttk.Combobox(marco_agregar, values=[], state="readonly", width=18)
        self.combo_madre.grid(row=2, column=1, padx=5, pady=5)

        # Botón para agregar persona
        btn_agregar = tk.Button(marco_agregar, text="Agregar", command=self.agregar_persona, bg="#4a90e2", fg="white", font=("Arial", 10, "bold"))
        btn_agregar.grid(row=3, column=0, columnspan=2, pady=10)

        # Marco para buscar ancestros
        marco_buscar = tk.LabelFrame(self, text="Buscar Ancestros", bg="#e3eaf2", font=("Arial", 12, "bold"))
        marco_buscar.pack(padx=20, pady=10, fill="x")

        # Combobox para seleccionar persona
        tk.Label(marco_buscar, text="Persona:", bg="#e3eaf2").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_persona = ttk.Combobox(marco_buscar, values=[], state="readonly", width=18)
        self.combo_persona.grid(row=0, column=1, padx=5, pady=5)

        # Entrada para generación
        tk.Label(marco_buscar, text="Generación:", bg="#e3eaf2").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entrada_generacion = tk.Entry(marco_buscar, width=20)
        self.entrada_generacion.grid(row=1, column=1, padx=5, pady=5)

        # Botón para buscar ancestros
        btn_buscar = tk.Button(marco_buscar, text="Buscar", command=self.buscar_ancestros, bg="#4a90e2", fg="white", font=("Arial", 10, "bold"))
        btn_buscar.grid(row=2, column=0, columnspan=2, pady=10)

        # Marco para mostrar resultados
        self.marco_resultados = tk.LabelFrame(self, text="Resultados", bg="#e3eaf2", font=("Arial", 12, "bold"))
        self.marco_resultados.pack(padx=20, pady=10, fill="both", expand=True)

        # Lista para mostrar resultados (aumenta height para más líneas visibles)
        self.lista_resultados = tk.Listbox(self.marco_resultados, font=("Arial", 12), bg="#f7fafc", height=15)
        self.lista_resultados.pack(fill="both", expand=True, padx=10, pady=10)

        # Inicializa el árbol con algunos datos de ejemplo
        self.inicializar_arbol_ejemplo()

    def inicializar_arbol_ejemplo(self):
        # No agregues personas de ejemplo, solo actualiza los combobox vacíos
        self.actualizar_comboboxes()

    def actualizar_comboboxes(self):
        # Actualiza las opciones de los combobox con los nombres actuales
        nombres = list(self.personas.keys())
        self.combo_padre['values'] = [""] + nombres
        self.combo_madre['values'] = [""] + nombres
        self.combo_persona['values'] = nombres

    def agregar_persona(self):
        # Obtiene los datos ingresados
        nombre = self.entrada_nombre.get().strip()
        padre_nombre = self.combo_padre.get()
        madre_nombre = self.combo_madre.get()

        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        if padre_nombre == madre_nombre and padre_nombre != "":
            messagebox.showerror("Error", "Padre y madre no pueden ser la misma persona.")
            return

        # Obtiene los objetos Persona de padre y madre si existen
        padre = self.personas.get(padre_nombre) if padre_nombre else None
        madre = self.personas.get(madre_nombre) if madre_nombre else None

        if nombre in self.personas:
            # Si la persona ya existe, actualiza sus padres
            persona = self.personas[nombre]
            persona.padre = padre
            persona.madre = madre
            messagebox.showinfo("Actualizado", f"Padres de '{nombre}' actualizados correctamente.")
        else:
            # Crea la nueva persona y la agrega al diccionario
            nueva_persona = Persona(nombre, padre, madre)
            self.personas[nombre] = nueva_persona
            messagebox.showinfo("Éxito", f"Persona '{nombre}' agregada correctamente.")

        # Limpia los campos y actualiza los combobox
        self.entrada_nombre.delete(0, tk.END)
        self.combo_padre.set("")
        self.combo_madre.set("")
        self.actualizar_comboboxes()

    def buscar_hermanos(self, persona):
        # Devuelve una lista de hermanos (excluyendo a la persona misma)
        hermanos = []
        for p in self.personas.values():
            if p is not persona and p.padre == persona.padre and p.madre == persona.madre and (p.padre or p.madre):
                hermanos.append(p.nombre)
        return hermanos

    def mostrar_arbol(self, persona):
        # Construye el árbol desde la persona seleccionada hacia los ancestros,
        # de modo que la persona seleccionada tenga la mayor indentación.
        def construir_cadena(persona, nivel=0, visitados=None):
            if not persona or (visitados and persona.nombre in visitados):
                return []
            if visitados is None:
                visitados = set()
            visitados.add(persona.nombre)
            ramas = []
            # Primero sube a los ancestros
            if persona.padre:
                ramas += construir_cadena(persona.padre, nivel + 1, visitados)
            if persona.madre:
                ramas += construir_cadena(persona.madre, nivel + 1, visitados)
            # Luego agrega la persona actual
            linea = f"{'    ' * nivel}- {persona.nombre}"
            # Agrega hermanos si existen
            hermanos = self.buscar_hermanos(persona)
            if hermanos:
                linea += " (Hermanos: " + ", ".join(hermanos) + ")"
            ramas.append(linea)
            return ramas

        # Invierte el resultado para mostrar de ancestro antiguo a reciente
        resultado = construir_cadena(persona, nivel=0)
        return resultado

    def buscar_ancestros(self):
        # Obtiene la persona y la generación seleccionada
        nombre = self.combo_persona.get()
        generacion_str = self.entrada_generacion.get().strip()

        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "Seleccione una persona.")
            return

        persona = self.personas.get(nombre)

        # Muestra el árbol completo a partir de la persona seleccionada
        self.lista_resultados.delete(0, tk.END)
        if persona:
            arbol = self.mostrar_arbol(persona)
            for linea in arbol:
                self.lista_resultados.insert(tk.END, linea)
        else:
            self.lista_resultados.insert(tk.END, "No se encontró la persona.")

# Punto de entrada principal
if __name__ == "__main__":
    # Crea y ejecuta la aplicación
    app = ArbolGenealogicoApp()
    app.mainloop()
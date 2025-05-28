import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# Clase Empleado con atributos adicionales
class Empleado:
    def __init__(self, nombre, cargo, departamento, fecha_ingreso):
        self.nombre = nombre
        self.cargo = cargo
        self.departamento = departamento
        self.fecha_ingreso = fecha_ingreso


    def __str__(self):
        return f"{self.nombre} ({self.cargo})"


# Nodo del árbol jerárquico de empleados
class NodoEmpleado:
    def __init__(self, empleado):
        self.empleado = empleado
        self.subordinados = []


    def agregar_subordinado(self, nodo_subordinado):
        self.subordinados.append(nodo_subordinado)


# Función para buscar empleados por nombre o cargo (retorna lista de nodos y niveles)
def buscar_empleados(nodo, texto_busqueda, nivel=0, resultados=None):
    if resultados is None:
        resultados = []
    texto_busqueda = texto_busqueda.lower()
    empleado = nodo.empleado
    # Buscar coincidencia en nombre o cargo
    if texto_busqueda in empleado.nombre.lower() or texto_busqueda in empleado.cargo.lower():
        resultados.append((nodo, nivel))
    for sub in nodo.subordinados:
        buscar_empleados(sub, texto_busqueda, nivel + 1, resultados)
    return resultados


# Función para obtener todos los empleados para autocompletar (solo nombres)
def obtener_todos_empleados(nodo, lista=None):
    if lista is None:
        lista = []
    lista.append(nodo.empleado.nombre)
    for sub in nodo.subordinados:
        obtener_todos_empleados(sub, lista)
    return lista


# Función para agregar nodos al Treeview de forma recursiva
def agregar_nodos_treeview(tree, nodo, padre=""):
    texto = f"{nodo.empleado.nombre} - {nodo.empleado.cargo}"
    id_nodo = tree.insert(padre, "end", text=texto, values=(
        nodo.empleado.departamento,
        nodo.empleado.fecha_ingreso.strftime("%Y-%m-%d")
    ))
    for sub in nodo.subordinados:
        agregar_nodos_treeview(tree, sub, id_nodo)


# Clase para la interfaz gráfica
class InterfazJerarquia:
    def __init__(self, raiz_arbol):
        self.raiz_arbol = raiz_arbol


        self.ventana = tk.Tk()
        self.ventana.title("Gestor de Jerarquía de Empleados")
        self.ventana.geometry("700x500")
        self.ventana.config(bg="#E8F0F2")


        self.style = ttk.Style(self.ventana)
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Segoe UI", 11), background="#E8F0F2")
        self.style.configure("TButton", font=("Segoe UI", 11), padding=6)
        self.style.configure("TEntry", font=("Segoe UI", 11))
        self.style.configure("Treeview", font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))


        # Título
        ttk.Label(self.ventana, text="Buscar empleado por nombre o cargo", font=("Segoe UI", 16, "bold"), background="#E8F0F2").pack(pady=10)


        # Frame búsqueda
        frame_busqueda = ttk.Frame(self.ventana)
        frame_busqueda.pack(pady=5, padx=10, fill="x")


        # Combobox con autocompletado
        self.nombres_empleados = obtener_todos_empleados(self.raiz_arbol)
        self.combo_buscar = ttk.Combobox(frame_busqueda, values=self.nombres_empleados)
        self.combo_buscar.set("Escribe nombre o cargo...")
        self.combo_buscar.pack(side="left", fill="x", expand=True, padx=5)
        self.combo_buscar.bind("<FocusIn>", self.limpiar_placeholder)
        self.combo_buscar.bind("<FocusOut>", self.restaurar_placeholder)


        # Botón buscar
        self.btn_buscar = ttk.Button(frame_busqueda, text="Buscar", command=self.buscar)
        self.btn_buscar.pack(side="left", padx=5)


        # Resultado de la búsqueda
        self.resultado = ttk.Label(self.ventana, text="", font=("Segoe UI", 11, "italic"), background="#E8F0F2")
        self.resultado.pack(pady=5)


        # Treeview para mostrar jerarquía
        self.tree = ttk.Treeview(self.ventana, columns=("departamento", "fecha_ingreso"), show="tree headings")
        self.tree.heading("#0", text="Empleado - Cargo")
        self.tree.heading("departamento", text="Departamento")
        self.tree.heading("fecha_ingreso", text="Fecha Ingreso")
        self.tree.column("#0", width=250)
        self.tree.column("departamento", width=150)
        self.tree.column("fecha_ingreso", width=120)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)


        # Cargar el árbol completo al iniciar
        agregar_nodos_treeview(self.tree, self.raiz_arbol)


        self.ventana.mainloop()


    # Limpia el texto placeholder cuando entra al combobox
    def limpiar_placeholder(self, event):
        if self.combo_buscar.get() == "Escribe nombre o cargo...":
            self.combo_buscar.set("")


    # Restaura el placeholder si el campo queda vacío
    def restaurar_placeholder(self, event):
        if not self.combo_buscar.get():
            self.combo_buscar.set("Escribe nombre o cargo...")


    # Acción al presionar buscar
    def buscar(self):
        texto = self.combo_buscar.get().strip()
        if not texto or texto == "Escribe nombre o cargo...":
            messagebox.showwarning("Entrada inválida", "Por favor, ingresa un nombre o cargo para buscar.")
            return


        resultados = buscar_empleados(self.raiz_arbol, texto)
        if not resultados:
            self.resultado.config(text=f"No se encontró ningún empleado o cargo que coincida con '{texto}'.", foreground="red")
            return


        # Mostrar todos los resultados encontrados con nivel jerárquico y detalles
        texto_resultado = f"Resultados para '{texto}':\n"
        for nodo, nivel in resultados:
            emp = nodo.empleado
            texto_resultado += (f"- {emp.nombre} (Cargo: {emp.cargo}, Departamento: {emp.departamento}, "
                               f"Ingreso: {emp.fecha_ingreso.strftime('%Y-%m-%d')}) - Nivel: {nivel}\n")
        self.resultado.config(text=texto_resultado, foreground="green")


# Construir ejemplo de árbol con atributos extendidos
def construir_arbol_ejemplo():
    ceo = NodoEmpleado(Empleado("Priscila", "CEO", "Dirección", datetime(2023, 1, 10)))
    jefe_finanzas = NodoEmpleado(Empleado("Emma", "Jefe de Finanzas", "Finanzas", datetime(2023, 5, 22)))
    jefe_tecnologia = NodoEmpleado(Empleado("Steph", "Jefe de Tecnología", "Tecnología", datetime(2023, 8, 13)))
    analista = NodoEmpleado(Empleado("Jeyni", "Analista", "Finanzas", datetime(2024, 3, 15)))
    desarrollador = NodoEmpleado(Empleado("Alejandro", "Desarrollador", "Tecnología", datetime(2024, 7, 19)))
    tester = NodoEmpleado(Empleado("Eduardo", "Tester", "Tecnología", datetime(2025, 2, 11)))
    practicante = NodoEmpleado(Empleado("Carlos", "Practicante", "Tecnología", datetime(2025, 1, 5)))


    ceo.agregar_subordinado(jefe_finanzas)
    ceo.agregar_subordinado(jefe_tecnologia)


    jefe_finanzas.agregar_subordinado(analista)
    jefe_tecnologia.agregar_subordinado(desarrollador)
    jefe_tecnologia.agregar_subordinado(tester)


    desarrollador.agregar_subordinado(practicante)


    return ceo


# Ejecutar programa
if __name__ == "__main__":
    raiz = construir_arbol_ejemplo()
    InterfazJerarquia(raiz)

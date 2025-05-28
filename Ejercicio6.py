import tkinter as tk
from tkinter import messagebox

# Explicación conceptual de cómo un árbol AST representa la expresión (3 + 4) * 2
EXPLICACION = (
   "Un Árbol de Sintaxis Abstracta (AST) para la expresión (3 + 4) * 2 se construye así:\n\n"
   "1. El nodo raíz es el operador principal: '*'.\n"
   "2. El hijo izquierdo de '*' es el subárbol que representa '(3 + 4)':\n"
   "   - Nodo '+', con hijos '3' y '4'.\n"
   "3. El hijo derecho de '*' es el número '2'.\n\n"
   "Visualmente:\n"
   "      *\n"
   "     / \\\n"
   "    +   2\n"
   "   / \\\n"
   "  3   4\n"
   "\n"
   "Cada nodo interno representa un operador y cada hoja un operando."
)

class ASTVisualizer(tk.Tk):
   def __init__(self):
       super().__init__()
       self.title("Árbol de Sintaxis Abstracta: (3 + 4) * 2")
       self.geometry("600x500")
       self.configure(bg="#f0f4f8")
       self.resizable(False, False)
       self.create_widgets()

   def create_widgets(self):
       # Título
       title = tk.Label(self, text="Visualización de AST para (3 + 4) * 2",
                        font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#2d415a")
       title.pack(pady=10)

       # Botón para mostrar explicación
       explain_btn = tk.Button(self, text="Mostrar Explicación",
                               command=self.show_explanation, bg="#4f8cff", fg="white",
                               font=("Arial", 12, "bold"), relief="raised")
       explain_btn.pack(pady=5)

       # Canvas para dibujar el árbol
       self.canvas = tk.Canvas(self, width=550, height=300, bg="white", highlightthickness=1, highlightbackground="#b0b0b0")
       self.canvas.pack(pady=20)
       self.draw_ast()

   def show_explanation(self):
       # Muestra la explicación conceptual en una ventana emergente
       messagebox.showinfo("Explicación Conceptual", EXPLICACION)

   def draw_ast(self):
       # Dibuja el árbol AST en el canvas
       c = self.canvas
       c.delete("all")  # Limpia el canvas

       # Coordenadas de los nodos
       root_x, root_y = 275, 60
       left_x, left_y = 150, 150
       right_x, right_y = 400, 150
       left_left_x, left_left_y = 100, 240
       left_right_x, left_right_y = 200, 240

       # Dibuja líneas (ramas)
       c.create_line(root_x, root_y+20, left_x, left_y-20, width=2)
       c.create_line(root_x, root_y+20, right_x, right_y-20, width=2)
       c.create_line(left_x, left_y+20, left_left_x, left_left_y-20, width=2)
       c.create_line(left_x, left_y+20, left_right_x, left_right_y-20, width=2)

       # Dibuja nodos (óvalos) y etiquetas
       self.draw_node(c, root_x, root_y, "*")
       self.draw_node(c, left_x, left_y, "+")
       self.draw_node(c, right_x, right_y, "2")
       self.draw_node(c, left_left_x, left_left_y, "3")
       self.draw_node(c, left_right_x, left_right_y, "4")

   def draw_node(self, canvas, x, y, text):
       # Dibuja un nodo ovalado con texto centrado
       r = 25  # radio
       canvas.create_oval(x-r, y-r, x+r, y+r, fill="#e3eaff", outline="#4f8cff", width=2)
       canvas.create_text(x, y, text=text, font=("Arial", 14, "bold"), fill="#2d415a")

if __name__ == "__main__":
   # Inicia la aplicación gráfica
   app = ASTVisualizer()
   app.mainloop()
import tkinter as tk
from tkinter import messagebox

# -------------------- BLOQUE DE LÓGICA --------------------
# Árbol de decisiones representado como diccionario anidado
decision_tree = {
    "¿El dispositivo enciende?": {
        "Sí": {
            "¿La pantalla muestra imagen?": {
                "Sí": {
                    "¿El sonido funciona?": {
                        "Sí": {
                            "¿El dispositivo se conecta a internet?": {
                                "Sí": "El dispositivo funciona correctamente.",
                                "No": {
                                    "¿El WiFi está activado?": {
                                        "Sí": {
                                            "¿Otras redes están disponibles?": {
                                                "Sí": "Revisar configuración de red o contactar al proveedor de internet.",
                                                "No": "Revisar el router o la señal WiFi."
                                            }
                                        },
                                        "No": "Activar el WiFi desde la configuración del dispositivo."
                                    }
                                }
                            }
                        },
                        "No": {
                            "¿El volumen está subido y no está en silencio?": {
                                "Sí": "Revisar altavoces o configuración de sonido.",
                                "No": "Subir el volumen y quitar el silencio."
                            }
                        }
                    }
                },
                "No": {
                    "¿La pantalla está iluminada?": {
                        "Sí": {
                            "¿Se ve alguna imagen tenue o parpadeante?": {
                                "Sí": "Revisar la conexión de video o la tarjeta gráfica.",
                                "No": "Revisar el brillo de la pantalla o intentar con un monitor externo."
                            }
                        },
                        "No": {
                            "¿El indicador de encendido está prendido?": {
                                "Sí": "Revisar retroiluminación o fuente de alimentación de la pantalla.",
                                "No": "Posible problema de hardware en la pantalla o la placa base."
                            }
                        }
                    }
                }
            }
        },
        "No": {
            "¿Está conectado a la corriente?": {
                "Sí": {
                    "¿El cargador muestra luz o indicador?": {
                        "Sí": "Revisar batería o fuente de alimentación interna.",
                        "No": {
                            "¿El enchufe funciona con otros dispositivos?": {
                                "Sí": "Reemplazar el cargador.",
                                "No": "Revisar la toma de corriente o usar otra."
                            }
                        }
                    }
                },
                "No": "Conectar el dispositivo a la corriente."
            }
        }
    }
}

# -------------------- BLOQUE DE INTERFAZ --------------------
class DecisionTreeGUI:
    def __init__(self, root, tree):
        self.root = root  # Ventana principal
        self.tree = tree  # Árbol de decisiones
        self.current_node = tree  # Nodo actual

        # Colores y estilos
        self.bg_color = "#e3f0fa"
        self.header_color = "#1976d2"
        self.button_color = "#42a5f5"
        self.button_fg = "#fff"
        self.diagnosis_color = "#388e3c"
        self.font = ("Segoe UI", 13)
        self.header_font = ("Segoe UI", 18, "bold")

        self.root.configure(bg=self.bg_color)

        # Encabezado
        self.header = tk.Label(
            root, text="Árbol de Decisiones\nDiagnóstico de Dispositivo",
            font=self.header_font, bg=self.header_color, fg="white", pady=10
        )
        self.header.pack(fill=tk.X, pady=(0, 10))

        # Marco para la pregunta/diagnóstico
        self.question_frame = tk.Frame(root, bg=self.bg_color, bd=2, relief="groove")
        self.question_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.question_label = tk.Label(
            self.question_frame, text="", font=self.font, wraplength=420,
            bg=self.bg_color, fg="#222", justify="center"
        )
        self.question_label.pack(pady=18, padx=10)

        # Frame para los botones de respuesta
        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.pack(pady=10)

        # Botón de reinicio (aparece solo en diagnóstico)
        self.restart_btn = tk.Button(
            root, text="Reiniciar", command=self.restart,
            bg="#f44336", fg="white", font=("Segoe UI", 11, "bold"),
            relief="raised", bd=2, cursor="hand2", activebackground="#b71c1c"
        )

        # Muestra la primera pregunta
        self.show_question(self.current_node)

    def show_question(self, node):
        # Elimina los botones anteriores
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.restart_btn.pack_forget()

        # Si el nodo es un string, es un diagnóstico final
        if isinstance(node, str):
            self.question_label.config(
                text="Diagnóstico:\n" + node,
                fg=self.diagnosis_color, font=("Segoe UI", 14, "bold")
            )
            self.restart_btn.pack(pady=10)
            return

        # Si el nodo es un diccionario, muestra la pregunta y los botones
        question = list(node.keys())[0]
        self.question_label.config(
            text=question, fg="#222", font=self.font
        )
        for answer in node[question]:
            btn = tk.Button(
                self.button_frame, text=answer, width=15,
                command=lambda ans=answer: self.next_node(node[question][ans]),
                bg=self.button_color, fg=self.button_fg, font=("Segoe UI", 11, "bold"),
                relief="raised", bd=2, cursor="hand2", activebackground="#1565c0"
            )
            btn.pack(side=tk.LEFT, padx=15, pady=5)

    def next_node(self, next_node):
        # Cambia al siguiente nodo según la respuesta
        if next_node is None:
            messagebox.showerror("Error", "Respuesta no válida.")
            return
        self.current_node = next_node
        self.show_question(self.current_node)

    def restart(self):
        # Reinicia el árbol de decisiones
        self.current_node = self.tree
        self.show_question(self.current_node)

# -------------------- EJECUCIÓN PRINCIPAL --------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Árbol de Decisiones - Diagnóstico de Dispositivo")
    root.geometry("520x340")
    root.resizable(False, False)
    app = DecisionTreeGUI(root, decision_tree)
    root.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CircuitSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Circuitos Eléctricos")

        # Lista para almacenar resistencias y su tipo de conexión
        self.resistencias = []
        self.conexion_tipo = tk.StringVar(value="serie")

        # Crear y colocar widgets
        self.create_widgets()

    def create_widgets(self):
        # Entrada de voltaje
        tk.Label(self.root, text="Voltaje (V):").grid(row=0, column=0, padx=10, pady=5)
        self.entry_voltaje = tk.Entry(self.root)
        self.entry_voltaje.grid(row=0, column=1, padx=10, pady=5)

        # Entrada de resistencia
        tk.Label(self.root, text="Resistencia (Ω):").grid(row=1, column=0, padx=10, pady=5)
        self.entry_resistencia = tk.Entry(self.root)
        self.entry_resistencia.grid(row=1, column=1, padx=10, pady=5)

        # Tipo de conexión
        tk.Label(self.root, text="Tipo de Conexión:").grid(row=2, column=0, padx=10, pady=5)
        ttk.Radiobutton(self.root, text="Serie", variable=self.conexion_tipo, value="serie").grid(row=2, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.root, text="Paralelo", variable=self.conexion_tipo, value="paralelo").grid(row=2, column=2, padx=5, pady=5)

        # Botón para agregar resistencia
        self.button_agregar = tk.Button(self.root, text="Agregar Resistencia", command=self.agregar_resistencia)
        self.button_agregar.grid(row=3, column=0, columnspan=3, pady=10)

        # Lista para mostrar resistencias
        self.lista_resistencias = tk.Listbox(self.root, width=50)
        self.lista_resistencias.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        # Botón para calcular
        self.button_calcular = tk.Button(self.root, text="Calcular", command=self.calcular)
        self.button_calcular.grid(row=5, column=0, columnspan=3, pady=10)

        # Etiqueta para mostrar resultados
        self.label_resultado = tk.Label(self.root, text="")
        self.label_resultado.grid(row=6, column=0, columnspan=3, pady=10)

    def agregar_resistencia(self):
        try:
            valor = float(self.entry_resistencia.get())
            if valor <= 0:
                raise ValueError
            tipo_conexion = self.conexion_tipo.get()
            self.resistencias.append((valor, tipo_conexion))
            self.lista_resistencias.insert(tk.END, f"Resistencia: {valor} Ω ({tipo_conexion})")
            self.entry_resistencia.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor de resistencia válido.")

    def calcular(self):
        try:
            voltaje = float(self.entry_voltaje.get())
            if not self.resistencias:
                raise ValueError("No hay resistencias para calcular.")
            
            # Calcular la resistencia total considerando serie y paralelo
            resistencia_total = 0
            paralelo = []

            for valor, tipo in self.resistencias:
                if tipo == "serie":
                    if paralelo:
                        # Calcular paralelo pendiente y agregarlo a la serie
                        resistencia_total += 1 / sum(1 / r for r in paralelo)
                        paralelo = []
                    resistencia_total += valor
                elif tipo == "paralelo":
                    paralelo.append(valor)

            # Agregar el último paralelo si existe
            if paralelo:
                resistencia_total += 1 / sum(1 / r for r in paralelo)
            
            corriente = voltaje / resistencia_total
            self.label_resultado.config(text=f"Resistencia Total: {resistencia_total:.2f} Ω\nCorriente: {corriente:.2f} A")
        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")

# Crear la ventana principal y la aplicación
root = tk.Tk()
app = CircuitSimulator(root)
root.mainloop()

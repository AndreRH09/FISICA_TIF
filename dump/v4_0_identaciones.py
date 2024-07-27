import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class SubCircuit:
    def __init__(self, tipo_conexion):
        self.resistencias = []
        self.tipo_conexion = tipo_conexion
        self.subcircuitos = []

    def agregar_resistencia(self, resistencia):
        self.resistencias.append(resistencia)

    def agregar_subcircuito(self, subcircuito):
        self.subcircuitos.append(subcircuito)

    def calcular_resistencia_total(self):
        if not self.resistencias and not self.subcircuitos:
            return 0
        if self.tipo_conexion == "serie":
            resistencia_total = sum(self.resistencias)
            for subcircuito in self.subcircuitos:
                resistencia_total += subcircuito.calcular_resistencia_total()
            return resistencia_total
        elif self.tipo_conexion == "paralelo":
            inversa_resistencia_total = sum(1 / (r if r != 0 else 1) for r in self.resistencias)
            for subcircuito in self.subcircuitos:
                inversa_resistencia_total += 1 / subcircuito.calcular_resistencia_total()
            if inversa_resistencia_total == 0:
                raise ZeroDivisionError
            return 1 / inversa_resistencia_total
        else:
            raise ValueError("Tipo de conexión no válido.")

class CircuitSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Circuitos Eléctricos")

        self.subcircuitos = []
        self.conexion_tipo = tk.StringVar(value="serie")
        self.current_subcircuit = SubCircuit(self.conexion_tipo.get())
        self.parent_subcircuit = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Voltaje (V):").grid(row=0, column=0, padx=10, pady=5)
        self.entry_voltaje = tk.Entry(self.root)
        self.entry_voltaje.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Resistencia (Ω):").grid(row=1, column=0, padx=10, pady=5)
        self.entry_resistencia = tk.Entry(self.root)
        self.entry_resistencia.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Tipo de Conexión:").grid(row=2, column=0, padx=10, pady=5)
        ttk.Radiobutton(self.root, text="Serie", variable=self.conexion_tipo, value="serie").grid(row=2, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.root, text="Paralelo", variable=self.conexion_tipo, value="paralelo").grid(row=2, column=2, padx=5, pady=5)

        self.button_agregar = tk.Button(self.root, text="Agregar Resistencia", command=self.agregar_resistencia)
        self.button_agregar.grid(row=3, column=0, columnspan=3, pady=10)

        self.button_nuevo_subcircuito = tk.Button(self.root, text="Nuevo Subcircuito", command=self.nuevo_subcircuito)
        self.button_nuevo_subcircuito.grid(row=4, column=0, columnspan=3, pady=10)

        self.lista_resistencias = tk.Listbox(self.root, width=50)
        self.lista_resistencias.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        self.button_calcular = tk.Button(self.root, text="Calcular", command=self.calcular)
        self.button_calcular.grid(row=6, column=0, columnspan=3, pady=10)

        self.button_reiniciar = tk.Button(self.root, text="Reiniciar", command=self.reiniciar)
        self.button_reiniciar.grid(row=7, column=0, columnspan=3, pady=10)

        self.label_resultado = tk.Label(self.root, text="")
        self.label_resultado.grid(row=8, column=0, columnspan=3, pady=10)

    def agregar_resistencia(self):
        try:
            valor = float(self.entry_resistencia.get())
            if valor <= 0:
                raise ValueError
            self.current_subcircuit.agregar_resistencia(valor)
            self.lista_resistencias.insert(tk.END, f"Resistencia: {valor} Ω ({self.conexion_tipo.get()})")
            self.entry_resistencia.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor de resistencia válido.")

    def nuevo_subcircuito(self):
        if self.current_subcircuit.resistencias or self.current_subcircuit.subcircuitos:
            if self.parent_subcircuit:
                self.parent_subcircuit.agregar_subcircuito(self.current_subcircuit)
                self.lista_resistencias.insert(tk.END, f"Subcircuito ({self.current_subcircuit.tipo_conexion}): {self.current_subcircuit.calcular_resistencia_total():.2f} Ω")
            else:
                self.subcircuitos.append(self.current_subcircuit)
                self.lista_resistencias.insert(tk.END, f"Subcircuito ({self.current_subcircuit.tipo_conexion}): {self.current_subcircuit.calcular_resistencia_total():.2f} Ω")
            self.current_subcircuit = SubCircuit(self.conexion_tipo.get())
            self.parent_subcircuit = None
            self.lista_resistencias.insert(tk.END, "---- Nuevo Subcircuito ----")
        else:
            self.lista_resistencias.insert(tk.END, "El subcircuito actual está vacío, no se puede añadir.")

    def calcular(self):
        try:
            voltaje = float(self.entry_voltaje.get())
            if not self.subcircuitos and not self.current_subcircuit.resistencias and not self.current_subcircuit.subcircuitos:
                raise ValueError("No hay resistencias para calcular.")

            if self.current_subcircuit.resistencias or self.current_subcircuit.subcircuitos:
                self.subcircuitos.append(self.current_subcircuit)

            resistencia_total = 0
            detalles_subcircuitos = []
            for subcircuito in self.subcircuitos:
                resistencia_subcircuito = subcircuito.calcular_resistencia_total()
                resistencia_total += resistencia_subcircuito
                detalles_subcircuitos.append(f"Subcircuito ({subcircuito.tipo_conexion}): {resistencia_subcircuito:.2f} Ω")

            corriente = voltaje / resistencia_total
            detalles = "\n".join(detalles_subcircuitos)
            self.label_resultado.config(text=f"{detalles}\n\nResistencia Total del Circuito: {resistencia_total:.2f} Ω\nCorriente: {corriente:.2f} A")
        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Una de las resistencias es cero. No se puede calcular la resistencia total en paralelo con una resistencia de valor cero.")

    def reiniciar(self):
        self.subcircuitos = []
        self.current_subcircuit = SubCircuit(self.conexion_tipo.get())
        self.parent_subcircuit = None
        self.lista_resistencias.delete(0, tk.END)
        self.label_resultado.config(text="")
        self.entry_voltaje.delete(0, tk.END)
        self.entry_resistencia.delete(0, tk.END)

# Crear la ventana principal y la aplicación
root = tk.Tk()
app = CircuitSimulator(root)
root.mainloop()

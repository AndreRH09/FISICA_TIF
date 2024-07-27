import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import schemdraw
import schemdraw.elements as elm

# Crear figura y ejes para el diagrama del circuito
fig, ax_circuit = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(left=0.1, bottom=0.35)  # Ajustar espacio para los sliders

# Parámetros iniciales
V_init = 10  # Voltaje inicial
R_init = 2   # Resistencia inicial

# Configurar sliders
axcolor = 'lightgoldenrodyellow'
ax_volt = plt.axes([0.15, 0.25, 0.30, 0.02], facecolor=axcolor)  # Slider para voltaje
ax_res = plt.axes([0.15, 0.20, 0.30, 0.02], facecolor=axcolor)   # Slider para resistencia

s_volt = Slider(ax_volt, 'Voltaje (V)', 0, 20, valinit=V_init, valstep=0.1)
s_res = Slider(ax_res, 'Resistencia (Ω)', 0.1, 10, valinit=R_init, valstep=0.1)

# Función para dibujar el circuito
def draw_circuit(voltage, resistance):
    ax_circuit.clear()
    with schemdraw.Drawing(ax=ax_circuit, fontsize=10) as d:
        d.add(elm.SourceV().up().label(f'{voltage} V'))
        d.add(elm.Resistor().right().label(f'{resistance} Ω'))
        d.add(elm.Line().down())
        d.add(elm.Line().left())
    ax_circuit.axis('off')

# Dibujar el circuito inicial
draw_circuit(V_init, R_init)

# Función para actualizar el circuito basado en los sliders
def update(val):
    voltage = s_volt.val
    resistance = s_res.val
    draw_circuit(voltage, resistance)
    plt.draw()

# Conectar los sliders a la función de actualización
s_volt.on_changed(update)
s_res.on_changed(update)

# Mostrar el gráfico
plt.show()

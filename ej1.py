import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import numpy as np
from PIL import Image
import matplotlib.image as mpimg

# Crear figura y ejes para el gráfico de corriente y el diagrama del circuito
fig, (ax_circuit, ax_current) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(left=0.1, bottom=0.35)  # Ajustar espacio para los sliders y botones

# Parámetros iniciales
V_init = 10  # Voltaje inicial
R_init = 2   # Resistencia inicial
time_max = 30  # Tiempo máximo en segundos
fps = 10
frames = time_max * fps  # Número de frames

# Almacenar datos
x_data = []
y_data = []

# Variables de corriente
current = V_init / R_init
last_time = 0
paused = False

# Configurar sliders
axcolor = 'lightgoldenrodyellow'
ax_volt = plt.axes([0.15, 0.25, 0.30, 0.02], facecolor=axcolor)  # Slider para voltaje
ax_res = plt.axes([0.15, 0.20, 0.30, 0.02], facecolor=axcolor)   # Slider para resistencia

s_volt = Slider(ax_volt, 'Voltaje (V)', 0, 20, valinit=V_init, valstep=0.1)
s_res = Slider(ax_res, 'Resistencia (Ω)', 0.1, 10, valinit=R_init, valstep=0.1)

# Crear ejes para mostrar la resistencia, intensidad y voltaje
ax_resistance = plt.axes([0.15, 0.05, 0.75, 0.03], frameon=False)  # Posición de subtítulos
ax_resistance.xaxis.set_visible(False)
ax_resistance.yaxis.set_visible(False)

a = ax_resistance.text(0, 0.01, f'Resistencia Total: {R_init} Ω', fontsize=10, va='center')
b = ax_resistance.text(0.62, 0.01, f'Intensidad Total: {current:.2f} A', fontsize=10, va='center', ha='center')
c = ax_resistance.text(1.15, 0.01, f'Voltaje Total: {V_init} V', fontsize=10, va='center', ha='right')

# Función para actualizar la corriente basada en los valores de los sliders
def update_current(val):
    global current
    voltage = s_volt.val
    resistance = s_res.val
    current = voltage / resistance
    ax_current.set_title(f"Intensidad: {current:.2f} A")
    a.set_text(f"Resistencia Total: {resistance:.2f} Ω")
    b.set_text(f"Intensidad Total: {current:.2f} A")
    c.set_text(f"Voltaje Total: {voltage:.2f} V")

# Función para reiniciar la animación
def reset(event):
    global x_data, y_data, last_time, paused
    x_data = []
    y_data = []
    last_time = 0
    s_volt.set_val(V_init)
    s_res.set_val(R_init)
    ax_current.clear()
    update_current(None)
    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq() 
    ani.event_source.start()
    paused = False  # Asegurarse de que la animación se reanude

# Función para alternar pausa y reanudar
def toggle_pause(event):
    global paused
    if paused:
        ani.event_source.start()
        paused = False
        pause_button.label.set_text('Pausar')
    else:
        ani.event_source.stop()
        paused = True
        pause_button.label.set_text('Reanudar')

# Configurar botones
ax_button_reset = plt.axes([0.55, 0.1, 0.1, 0.05])
button_reset = Button(ax_button_reset, 'Reiniciar', color='lightblue', hovercolor='lightgreen')
button_reset.on_clicked(reset)

ax_button_pause = plt.axes([0.65, 0.1, 0.1, 0.05])
pause_button = Button(ax_button_pause, 'Pausar', color='lightblue', hovercolor='lightgreen')
pause_button.on_clicked(toggle_pause)

# Función para animar el gráfico de corriente
def animate(i):
    global last_time
    
    if not paused:
        # Tiempo en segundos
        t = i / fps
        
        if t > last_time:
            last_time = t
            
            # Añadir nuevos datos
            x_data.append(t)
            y_data.append(current)
            
            # Limpiar gráfico anterior
            ax_current.clear()
            
            # Graficar datos actualizados
            ax_current.plot(x_data, y_data, color='red')
            ax_current.set_xlim(0, time_max)
            ax_current.set_ylim(0, max(y_data) + 10 if y_data else 10)
            ax_current.grid(True)
        
        update_current(None)  # Actualizar el gráfico con los valores de los sliders

# Cargar y mostrar la imagen del circuito en el eje correspondiente
circuit_img = mpimg.imread('img/circuit1.png')
ax_circuit.imshow(circuit_img)
ax_circuit.axis('off')  # Ocultar los ejes del circuito

# Configurar la animación
ani = FuncAnimation(fig, animate, frames=frames, interval=1000//fps, repeat=False)

# Mostrar el gráfico
plt.show()
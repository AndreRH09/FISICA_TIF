import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 5))
plt.subplots_adjust(left=0.1, bottom=0.25, top=0.85)  # Adjust space for sliders and buttons

# Initial parameters
V_init = 10  # Initial voltage
R_init = 2   # Initial resistance
time_max = 15  # Maximum time in seconds
fps = 10
frames = time_max * fps  # Number of frames

# Data storage
x_data = []
y_data = []

# Current variables
current = V_init / R_init
last_time = 0
paused = False

# Setup sliders (positioned at the top)
axcolor = 'lightgoldenrodyellow'
ax_volt = plt.axes([0.5, 0.0001, 1, 0.02], facecolor=axcolor)  # Slider for voltage
ax_res = plt.axes([0.5, 0.02, 1, 0.02], facecolor=axcolor)   # Slider for resistance

s_volt = Slider(ax_volt, 'Voltage (V)', 0, 20, valinit=V_init, valstep=0.1)
s_res = Slider(ax_res, 'Resistance (Ω)', 0.1, 10, valinit=R_init, valstep=0.1)

def update_current(val):
    """Update the current based on slider values"""
    global current
    voltage = s_volt.val
    resistance = s_res.val
    if resistance != 0:
        current = voltage / resistance
    else:
        current = 0
    ax.set_title(f"Current: {current:.2f} A")

# Reset button callback
def reset(event):
    global x_data, y_data, last_time, paused, ani
    x_data = []
    y_data = []
    last_time = 0
    s_volt.set_val(V_init)
    s_res.set_val(R_init)
    ax.clear()
    update_current(None)
    ani.event_source.stop()
    ani.event_source.start()  # Restart animation
    paused = False  # Ensure animation resumes

# Pause button callback
def toggle_pause(event):
    global paused
    if paused:
        ani.event_source.start()
        paused = False
        pause_button.label.set_text('Pause')
    else:
        ani.event_source.stop()
        paused = True
        pause_button.label.set_text('Resume')

# Setup buttons (positioned below the sliders)
ax_button_reset = plt.axes([0.1, 0.1, 0.15, 0.05])
button_reset = Button(ax_button_reset, 'Reset', color='lightblue', hovercolor='lightgreen')
button_reset.on_clicked(reset)

ax_button_pause = plt.axes([0.3, 0.1, 0.15, 0.05])
pause_button = Button(ax_button_pause, 'Pause', color='lightblue', hovercolor='lightgreen')
pause_button.on_clicked(toggle_pause)

def animate(i):
    global last_time
    
    if not paused:
        # Time in seconds
        t = i / fps
        
        if t > last_time:
            last_time = t
            
            # Append the new data
            x_data.append(t)
            y_data.append(current)
            
            # Clear previous plot
            ax.clear()
            
            # Plot updated data
            ax.plot(x_data, y_data, color='red')
            ax.set_xlim(0, time_max)
            ax.set_ylim(-20, 20)  # Set static y limits
            ax.grid(True)
        
        update_current(None)  # Update the plot with current slider values

# Create animation
ani = FuncAnimation(fig, animate, frames=frames, interval=1000/fps, repeat=False)

plt.show()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 4))
plt.subplots_adjust(left=0.1, bottom=0.25, top=0.75)  # Adjust space for sliders and buttons

# Initial parameters
time_max = 15  # Maximum time in seconds
fps = 10
frames = time_max * fps  # Number of frames

# Data storage
x_data = []
y_data = []

# Current variables
paused = False

# Setup slider (positioned at the bottom)
axcolor = 'lightgoldenrodyellow'
ax_slider = plt.axes([0.1, 0.1, 0.65, 0.02], facecolor=axcolor)  # Slider position at the bottom
slider = Slider(ax_slider, 'Value', 0, 100, valinit=50, valstep=1)

def update_value(val):
    """Update the plot based on the slider value."""
    pass  # No need to do anything here since we will handle it in the animate function

# Reset button callback
def reset(event):
    global x_data, y_data, ani
    x_data = []
    y_data = []
    i = 0
    slider.set_val(50)  # Reset slider to default value
    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq() 
    ani.event_source.start()

# Setup buttons (positioned above the slider)
ax_button_reset = plt.axes([0.1, 0.15, 0.15, 0.05])
button_reset = Button(ax_button_reset, 'Reset', color='lightblue', hovercolor='lightgreen')
button_reset.on_clicked(reset)

def animate(i):
    global paused
    
    if not paused:
        # Time in seconds
        t = i / fps
        
        # Append the new data
        x_data.append(t)
        y_data.append(slider.val)
        
        # Clear previous plot
        ax.clear()
        
        # Plot updated data
        ax.plot(x_data, y_data, color='red')
        ax.set_xlim(0, time_max)
        ax.set_ylim(0, 100)  # Set static y limits for the slider values
        ax.grid(True)

# Create animation
ani = FuncAnimation(fig, animate, frames=frames, interval=1000/fps, repeat=False)

plt.show()

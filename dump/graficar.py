import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

fig = plt.figure(figsize=(6,4)) 
ax = fig.add_subplot(1,1,1) 

plt.title("Ejes Dinámicos")
y1 = [(np.sin(i*np. pi)*i) for i in np.arange(0,105,0.01)]
t = range(len(y1))
x,y=[], []


def animate(i): 
    x.append(t[i])
    y.append((y1[i]))
    # plt.xlim(i-20,i+20)
    plt.plot(x, y, scaley=True, scalex=True, color="red")

anim = FuncAnimation(fig, animate, interval=50, frames=1000,repeat= False)
plt.show()
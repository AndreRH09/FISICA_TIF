import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import schemdraw
import schemdraw.elements as elm

# Crear figura y ejes para el diagrama del circuito


with schemdraw.Drawing() as d:
    d += (V := elm.SourceV().up().label(f'V1 (V)'))
    d += elm.Resistor().right().label(f'R1 (Ω)')
    d += elm.Line().down()
    d += elm.Line().left()
# Mostrar el gráfico
plt.show()

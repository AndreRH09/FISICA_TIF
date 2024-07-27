import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import schemdraw
import schemdraw.elements as elm

# Crear figura y ejes para el diagrama del circuito

with schemdraw.Drawing() as d:
    d += (V := elm.SourceV().up().label(f'V1 (V)'))
    d += elm.Resistor().right().label(f'R1 (Ω)')
    
    # Primer quiebre (R1)
    d.push()
    d += elm.Resistor().right().label(f'R3 (Ω)').down()
    d += elm.Resistor().left().label(f'R2 (Ω)')
    d.pop()
    # Fin quiebre

    d += elm.Line().right()

    # Segundo quiebre (R2)
    d.push()
    d += elm.Resistor().right().label(f'R4 (Ω)').down()
    d += elm.Line().left()
    d.pop()
    # Fin quiebre

    d += elm.Line().down()
    d += elm.Line().left()
    d.save('img/circuitMixto.png')

# Mostrar el gráfico
plt.show()
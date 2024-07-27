import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import schemdraw
import schemdraw.elements as elm

# Crear figura y ejes para el diagrama del circuito


with schemdraw.Drawing() as d:
    d += (V := elm.SourceV().up().label(f'V1 (V)'))
    d += elm.Line().right()
    #primer quiebre
    d.push()
    d += elm.Resistor().right().label(f'R1 (Ω)').down()
    d += elm.Line().left()
    d.pop()
    #fin quiebre

    d += elm.Line().right()
    
    #seg  quiebre
    d.push()
    d += elm.Resistor().right().label(f'R2 (Ω)').down()
    d += elm.Line().left()
    d.pop()
    #fin quiebre

    
    d += elm.Line().right()
    #tercer  quiebre
    d.push()
    d += elm.Resistor().right().label(f'R3 (Ω)').down()
    d += elm.Line().left()
    d.pop()
    #fin quiebre

    d += elm.Line().right()
    #cuarto  quiebre
    d.push()
    d += elm.Resistor().right().label(f'R4 (Ω)').down()
    d += elm.Line().left()
    d.pop()
    #fin quiebre


    d.save('img/circuit2.png')
# Mostrar el gráfico
plt.show()

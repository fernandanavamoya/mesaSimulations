#servidor que tya tiene mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter 
from mesa.visualization.modules import CanvasGrid
# hacer import a nuestra clase
from model import ForestFire

colors = {"Fine" : "#00FF00", "On fire" : "#AA0000", "Burned out" : "#000000"}

# portrayal es una forma que tiene el visualizador para entender como se van a ver los agentes
def forest_fire_portrayal(tree):
    # si el agente no existe se regresa
    if tree is None:
        return
    portrayal = {"Shape" : "rect", "w" : 0.7, "h" : 0.7, "Filled" : "true", "Layer" : 0}
    # la posición es la posición del árbol
    (x,y) = tree.pos 
    # asignar x,y y color de acuerdo a su condición
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = colors[tree.condition]
    # se regresa el portrayal
    return portrayal

canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)

model_params = {
    "height" : 100,
    "width" : 100,
    "density" : UserSettableParameter("slider", "Tree density", 0.6, 0.01, 1.0, 0.1)
}

server = ModularServer(
    ForestFire, 
    [canvas_element], 
    "Forest Fire", 
    model_params
)

server.launch()

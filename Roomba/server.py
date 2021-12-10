# ChartModule nos va a permitir crear graficas
from mesa import datacollection
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
#servidor que ya tiene mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter 
# hacer import a nuestra clase
from model import RoombaStart, ObstacleAgent, Roomba

# colores que se verán de acuerda al estado de objeto Cell
colors = {"Dirty" : "black", "Clean" : "white"}
# portrayal de la celda
def cell_portrayal(cell):
    # si el agente no existe se regresa
    if cell is None:
        return
    # portrayal base 
    portrayal = {
        "Shape" : "rect", 
        "w" : 0.8, 
        "h" : 0.8, 
        "Filled" : "true", 
        "Layer" : 0,
    }
    # si es un objeto tipo ObstacleAgent entonces su portrayal cambia
    if (isinstance(cell, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
        portrayal["Shape"] = "circle"
     # si es un objeto tipo Roomba entonces su portrayal cambia
    elif (isinstance(cell, Roomba)):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.5
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
     # si es un objeto tipo Cell entonces su portrayal cambia
    else:
        # la posición es la posición del árbol
        (x,y) = cell.pos
        # asignar x,y y color de acuerdo a su condición
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[cell.condition]

    # se regresa el portrayal
    return portrayal

# parametros iniciales del grid
model_params = {
    "N": UserSettableParameter("slider", "Número de Roombas", 5, 1, 10, 1), 
    "width": 15, 
    "height": 10,
    "density" : UserSettableParameter("slider", "Cantidad de celdas sucias", 0.2, 0.01, 1, 0.05),
    "maxIterations" : UserSettableParameter("slider", "Maximas iteraciones", 100, 10, 1000, 10)
}

# se crean las condiones del grid
canvas_grid = CanvasGrid(cell_portrayal, 10, 10, 500, 500)
# se crean las condiciones de la gráfica
canvas_graph = ChartModule(
    [{"Label" : "Celdas Sucias", "Color" : "red"}],
    data_collector_name = 'datacollector'
)
# se crean las condiciones de la gráfica de Pie
# canvas_pie = PieChartModule(
#     [{"Label" : "Celdas limpias", "Color" : "green"}],
#     data_collector_name = 'datacollector'
# )

# se crea un ModularServer con los parametros y datos
server = ModularServer(
    RoombaStart, 
    [canvas_grid, canvas_graph], 
    "Roomba", 
    model_params
)
# hace launch al servidor
server.port = 8521 # The default
server.launch()

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import RandomModel, ObstacleAgent

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

model_params = {"N":5, "width":10, "height":10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(RandomModel, [grid], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()
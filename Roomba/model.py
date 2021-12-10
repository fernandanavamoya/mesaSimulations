from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from agent import Cell, Roomba, ObstacleAgent
# importar datacollector de mesa
from mesa.datacollection import DataCollector

# función que obtiene las celdas sucias que qeudan en famenera de porcentage
def getDirty(model):
    result = round(((model.counter_dirty / model.startDirty) * 100), 2)
    return result
# función que obtiene la cantidad de iteraciones
def getIterations(agent):
    if isinstance(agent, Roomba):
        return agent.move
    else:
        return

# clase que diseña el grid 
class RoombaStart(Model):
    # constructor de la clase
    def __init__(self, N, width, height, density, maxIterations):
        self.num_agents = N  # numero de Roombas
        # la altura y ancho del grid
        self.grid = Grid(width,height, torus=False) 
        # crea y asigna valor la variable de maximas Iteraciones
        self.maxIterations = maxIterations
        self.schedule = RandomActivation(self)
        self.running = True 
        self.iterations = 0 # inicializar iteraciones en 0
        self.counter_dirty = 0 # counter de celdas sucias
        self.startDirty = 0 # inicializar la variable en 0

        # crea el borde del grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]
        # por cada posición en borde crea un objecto 
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.schedule.add(obs)
            # object, pos
            self.grid.place_agent(obs, pos)

        # iterador que regresa el contenido y coordenadas de la celda
        for(contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density and self.grid.is_cell_empty((x,y)):
                new_cell = Cell(self.random.randint(1,100000), self) 

                # recibe la variable del agente y después la posición
                self.grid.place_agent(new_cell, (x,y))
                self.schedule.add(new_cell)
            elif x == 1 and y == 1:
                for i in range(self.num_agents):
                    new_Roomba = Roomba(self.random.randint(1,100000), self)
                    self.grid.place_agent(new_Roomba, (x,y))
                    self.schedule.add(new_Roomba)
        # actualizar variable de startDirty
        self.startDirty = self.counter_dirty

        self.datacollector = DataCollector(
            model_reporters = {"Celdas Sucias" : getDirty},
            agent_reporters = {"Iteraciones" : getIterations}
        )
                    
        # continua la simulación
        self.running = True

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.iterations += 1 # añade uno a la variable de iteraciones
        # si las iteraciones son mayores iguales a la iteraciones maximas permitidas
        # o si ya no hay celdas sucias entonce la simulación para
        if self.iterations >= self.maxIterations or self.counter_dirty <= 0:
            self.running = False
    
from mesa import Model
from mesa.space import Grid
from mesa.time import RandomActivation
#Hacer import a nuestra clase
from agent import Tree

class ForestFire(Model):
    def __init__(self, height=100, width=100, density=0.6):
        super().__init__()
        self.schedule = RandomActivation(self)
        # torus es para que el agente pueda empezar desde el inicio otra vez cuando termine (puede darle vuelta al escenario)
        self.grid = Grid(height, width, torus=False)

        # iterador que regresa el contenido y coordenadas de la celda
        for(contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                new_tree = Tree((x,y), self) 

                if x == 0:
                    new_tree.condition = "On fire"

                self.grid._place_agent((x,y), new_tree)
                self.schedule.add(new_tree)

        # continua la simulación
        self.running = True
    
    def step(self):
        self.schedule.step()

        count = 0
        for tree in self.schedule.agents:
            if tree.condition == "On fire":
                count += 1
        # Si ya no hay árboles quemandose entonce la simulación para
        if count == 0:
            self.running = False

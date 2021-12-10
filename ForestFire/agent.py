#Primero seabre una terminal donde se instalo mesa y se activa el proyecto
#conda activate base
#conda activate test
#y el environment se pone en python ('test': conda)
from mesa import Agent

class Tree(Agent):
    #Constructor de clase
    def __init__(self, pos, model):
        #Llama el contructor de clase padre para inicializar todos sus atributos
        super().__init__(pos, model) #agrega posición al agente
        self.pos = pos
        #Estado del árbol: Fine, On fire, Burned out
        self.condition = "Fine"

    #Es un update que se va a estar llamando cada vuleta de la simulación
    def step(self):
        if self.condition == "On fire":
            #Buscar los vecinos del agente
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine":
                    neighbor.condition = "On fire"
            # Una vez que se termine de quemar a los vecinos 
            self.condition = "Burned out"
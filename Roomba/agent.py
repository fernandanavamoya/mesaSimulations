#Primero seabre una terminal donde se instalo mesa y se activa el proyecto
#conda activate base
#conda activate test
#y el environment se pone en python ('test': conda)
from mesa import Agent

# clase del agente tipo celda
class Cell(Agent):
    # constructor de clase
    def __init__(self, unique_id, model):
        #Llama el contructor de clase padre para inicializar todos sus atributos
        super().__init__(unique_id, model) #agrega posición al agente
        self.direccion = 0 #Frente 0, Derecha 1, Izquierda 2, Atras 3
        self.sentido = 3 #Derecha 0, Izquierda 1, Arriba 2, Abajo 3
        #Estado de la celda: Clean, Dirty
        self.condition = "Dirty"    
        # Contador de celdas sucias que existen
        self.model.counter_dirty += 1

    #Es un update que se va a estar llamando cada vuelta de la simulación
    def step(self):
        pass

# clase de obstaculos para que los agentes no se salgan del grid
class ObstacleAgent(Agent):
    # constructor de clase
    def __init__(self, pos, model):
        super().__init__(pos, model)
    #Es un update que se va a estar llamando cada vuelta de la simulación
    def step(self):
        pass  

# clase de Roomba las cuales van a estar limpiando el grid
class Roomba(Agent):
    # constructor de clase 
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = 4

    # función que toma coordenadas y verifica si es un ojeto tipo Roomba o no
    def notRoomba(self, coordenadas):
        # obtiene valores de la celda y los objetos en ella
        cell_content = self.model.grid.get_cell_list_contents(coordenadas)
        # itera por la lista de objetos
        for cell in cell_content:
            # en caso de ser roomba regresa False
            if isinstance(cell,Roomba):
                return False
            # o en caso de ser roomba regresa False
            elif isinstance(cell,ObstacleAgent):
                return False
        # si es una celda o esta vacía entonces regresa True
        return True

    # función que permite que el Roomba se mueva a otra celda
    def move(self):
        # possible_steps va a ser una lista de coordenadas de sus vecinos y de ella misma
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) 
                        # or Von Neumann (only up/down/left/right).
            include_center=True
        ) 
        
        # lista con las coordenas posibles en las que se puede mover
        # llama a la funcion notRoomba para saber si es una celda o esta vacía
        freeSpaces = list(map(self.notRoomba, possible_steps)) 

        # si se puede mover en esa celda entonces se mueve, si no se queda donde esta
        if freeSpaces[self.direction]:
            # obtiene los objetos que estan en esa celda, a la que se quiere mover
            cell_content = self.model.grid.get_cell_list_contents(possible_steps[self.direction])
            # itera por esa lista de objetos
            for cell in cell_content:
                # el objeto es de tipo Cell entonces 
                if isinstance(cell, Cell):
                    # le resta uno a counter_dirty ya que la Roomba se va a mover ahí y se va a limpiar
                    self.model.counter_dirty -= 1
            # se mueve a esa dirección y borra el Cell
            self.model.grid.move_agent(self, possible_steps[self.direction])

    #Es un update que se va a estar llamando cada vuelta de la simulación
    def step(self):
        # obtiene una direction random entre 0,8: posibles direcciones           
        self.direction = self.random.randint(0,8)
        # se mueve la Roomba
        self.move()


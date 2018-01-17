import sys, pygame

width = 1000
height = 800

class Graph:
    startY = int(height/2)      # starting point on Y axis
    startX = int(width/2)
    originX = 0                 # oringin of graph, moves with framelength

    scale_y = float(1)          # graph scale (the whole graph)
    
    graphs = {}             # holds graph metadata like color, units...
    values = []             # holds x and y values of graphs

    scr = None              # holds pygame surface object

    def __init__(self, x, y):

        # init pygame
        pygame.init()
        self.scr = pygame.display.set_mode((width, height))
        self.originX = self.startX 

    def render(self, frameLength=0):
        ''' Draw graphs and do other drawing stuff '''

        # fill screen black at start
        self.scr.fill((0,0,0))

        # draw dots
        for key, graph in enumerate(self.values):
            prev = [0,0]                        # start from origin
            color = self.graphs[key]['color']   # graph specific color

            # draw the graph
            for val in graph:
                x = int(val[0] + int(self.originX))
                y = int(val[1] * self.graphs[key]['scale_y'] * self.scale_y)    # scale factors

                # if there is a gap between this and previous point
                if abs(y - prev[1]) > 1 or abs(x - prev[0]) > 1:
                    pygame.draw.line(self.scr, color,
                        (prev[0], self.startY - prev[1]),
                        (x, self.startY - y))
                else:
                    self.scr.set_at((int(self.originX) + x, self.startY - y), color)

                prev = [x,y]

        self.__drawDimensions()

        self.originX -= frameLength

    def insert(self, x, y, graph):
        ''' Add new point to the graph '''

        self.values[graph].append([x,y])

    def createGraph(self, color, scale_y=1):
        ''' Create new graph with specific color, units etc.
            return: key of the new graph
        '''

        self.values.append([])
        key = len(self.values)-1
        self.graphs[key] = {
            'color': color,
            'scale_y': scale_y
        }

        return key

    def __drawDimensions(self):
        ''' Draw all the decoraton stuff of the graph like x and y axis... '''
        white = (255,255,255)

        # x axis
        pygame.draw.line(self.scr, white, (0, self.startY),(width*0.7, self.startY))

        # y axis
        pygame.draw.line(self.scr, white, (self.startX, 0),(self.startX, height))

    def adjustScale(self, change):
        self.scale_y += change

    def simu(self, vars):
        print("Simu")
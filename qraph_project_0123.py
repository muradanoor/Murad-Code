import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import itertools
class coordinate: #class for coordinate
    def __init__(self,x,y):
        self.coordinate = [x,y]
    
    def Random_Process(self,SD): 
        self.coordinate[0] = self.coordinate[0]+np.random.normal(0,SD)
        self.coordinate[1] = self.coordinate[1]+np.random.normal(0,SD)

    def x(self):
        return self.coordinate[0]
    
    def y(self):
        return self.coordinate[1]

    def xto(self,x):
        self.coordinate[0] = x
    
    def yto(self,y):
        self.coordinate[1] = y

def Distance(node1 , node2 , R , length): #calculate distance between 2 nodes in torus , if distance is greater than R ,return -1
    if node1.x() + R > length  and  node2.x() - R < 0 or node2.x() + R > length  and  node1.x() - R < 0: 
        #check whether both circle centered at node1,2 passed the vertical border
        #we want to fixed the point at right
        if node1.x() + R > length:
            LeftNode = node2
            RightNode = node1
        else:
            LeftNode = node1
            RightNode = node2 
        #check whether both circle centered at node1,2 passed the horizontal border
        if node1.y() + R > length  and  node2.y() - R < 0 or node2.y() + R > length  and  node1.y() - R < 0:
            #move both x and y
            if LeftNode.y() + R > length: #it's on the upper left ,we add length to x and minus length to y
                res =  np.sqrt((LeftNode.x()+length - RightNode.x())**2 +  (LeftNode.y() - length - RightNode.y())**2)
            else:#it's on the lower left we add length to both x and y
                res  = np.sqrt((LeftNode.x()+length - RightNode.x())**2 +  (LeftNode.y() + length - RightNode.y())**2)
        else: # it's just on left we move add length to x
            res =  np.sqrt((LeftNode.x()+length - RightNode.x())**2 +  (LeftNode.y() - RightNode.y())**2)
    elif  node1.y() + R > length  and  node2.y() - R < 0 or node2.y() + R > length  and  node1.y() - R < 0: #check y conditions
        #we want upper node be fixed
        if node1.y() + R > length:
            UpperNode = node1
            LowerNode = node2
        else:
            UpperNode = node2
            LowerNode = node1 
        res =  np.sqrt((UpperNode.x() - LowerNode.x())**2 +  (LowerNode.y()+length - UpperNode.y())**2)
    else:
        res = np.sqrt((node1.x() - node2.x())**2 +  (node1.y() - node2.y())**2)
    #check if distance is less than R
    if res > R:
        res = -1 # -1 repersents they are not connected
    return res 

class Graph: # class for graph where R is radius, SD is standard deviation
    def __init__(self , shape , R , SD , length):
        self.graph = []
        self.shape = shape
        self.R = R
        self.SD = SD
        self.length = length

        if self.shape == "square" :
            for i in range(length):
                for j in range(length):
                    self.graph.append(coordinate(i+1/2,j+1/2))
        elif self.shape == "triangle":
            for i in range (length):
                for j in range(length):
                    if i%2 == 0:
                        self.graph.append(coordinate(j+1/2,i+1/2))
                    else:
                        self.graph.append(coordinate(j+1,i+1/2))
                                
    def Print_Graph(self): #method for checking
        res = ""
        for i in range((self.length)**2):
            res = res + str(self.graph[i].coordinate)
            print(res)
    
    def Get_XY_List(self): #get a list contains 2 lists, 1st list stores x values 2nd list stores y values, used for plotting
        X = []
        Y = []
        for i in range((self.length)**2):
            X.append(self.graph[i].x())
            Y.append(self.graph[i].y())
        return [X,Y]

    def Plot_Graph(self): # plot the graph
        plt.plot(self.Get_XY_List()[0],self.Get_XY_List()[1],".")
        plt.show()

    def Random_Movement(self):
        for i in range((self.length)**2):

            self.graph[i].Random_Process(self.SD) # take random movement for each node

            if self.graph[i].x() > self.length : # make sure we are working in a torus
                self.graph[i].xto(self.graph[i].x() - self.length) # checking conditions for x
            elif self.graph[i].x() < 0 :
                self.graph[i].xto(self.length - self.graph[i].x())
            
            if self.graph[i].y() > self.length : # checking conditions for y
                self.graph[i].yto(self.graph[i].y() - self.length) 
            elif self.graph[i].y() < 0 :
                self.graph[i].yto(self.length - self.graph[i].y())

    def Find_Components(self):
        #not complete yet
        #loop until there is no more element in original list
        Avaliable_Nodes = self.graph
        current_Node = Avaliable_Nodes.pop(0)
        current_queue = []
        To_Sub = []
        res = []
        current_component = []

        #loop for first time to enter while
        for i in range(len(Avaliable_Nodes)):
            if Distance(current_Node,Avaliable_Nodes[i] , self.R ,self.length) != -1:
                current_queue.append(Avaliable_Nodes[i])
            else :
                To_Sub.append(Avaliable_Nodes[i])
        current_component.append(current_Node)
        Avaliable_Nodes =  To_Sub
        if len(current_queue) == 0 :
            current_Node = Avaliable_Nodes.pop(0) 
            res.append(current_component)   
            current_component = []
        else :
            current_Node = current_queue.pop(0)
        To_Sub = []


        while len(Avaliable_Nodes) != 0 :
            while True:
                for i in range(len(Avaliable_Nodes)):#loop through the current node, find nodes within R
                    if Distance(current_Node,Avaliable_Nodes[i], self.R ,self.length) != -1:
                        current_queue.append(Avaliable_Nodes[i])
                    else :
                        To_Sub.append(Avaliable_Nodes[i])
                current_component.append(current_Node)
                if len(current_queue) != 0 :
                    current_Node = current_queue.pop(0) 
                Avaliable_Nodes =  To_Sub
                To_Sub = []
                if len(current_queue) == 0:
                    break
            if len(Avaliable_Nodes) != 0:
                current_Node = Avaliable_Nodes.pop(0)
            res.append(current_component)
            current_component = []
        return res
    
    def largest_component(self):
        components = self.Find_Components()
        res = 0
        for i in range(len(components)):
            if len(components[i]) > res:
                res = len(components[i])
        return res
    def mean_degree(self):
        pointers = self.Get_XY_List()
        components = []
        i = 0
        degree = 0
        while i != len(pointers[0]) - 1:
            component = [pointers[0][i], pointers[1][i]]
            components.append(component)
            i = i + 1
        for j in range(len(components)):
            coordinate1 = coordinate(components[j][0],components[j][1])
            for k in range(len(components)):
                coordinate2 = coordinate(components[k][0],components[k][1])
            if Distance(coordinate1, coordinate2, self.R, self.length) != -1:
                degree = degree + 1
            else:
                degree = degree
        return (2*degree)/len(components)
def largest_component_heatmap():
    data = []
    current_D = []
    average = 0
    for i in range(10):        
        for j in range(10):
            for k in range(100):
                foo = Graph("square",1+0.1*i,0.1*j,10)
                foo.Random_Movement()
                average += foo.largest_component()
            current_D.append(average/100)
            average = 0
        data.append(current_D)
        current_D = []
    label1 = [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9]
    label2 = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    df_cm = pd.DataFrame(data, index = label1,
                  columns = label2)
    sns.set()
    ax = sns.heatmap(df_cm)
    ax.set_ylabel('R')
    ax.set_xlabel('SD')
    ax.set_title('larget_component_heatmap')
    print(str(data))
    plt.show()
def mean_degree_heatmap():
    data = []
    average = 0
    r = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    sd = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    rdsq = list(itertools.product(r, sd))
    rd = 0
    sq = 0
    while rd != 10:
        current_D = []
        for sq in range(10):
            foo = Graph("square",r[rd],sd[sq],10)
            foo.Random_Movement()
            average = foo.mean_degree()
            current_D.append(average)
        rd = rd + 1
        data.append(current_D)
    label1 = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    label2 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    df_cm = pd.DataFrame(data, index =  label1, columns = label2)
    sns.set()
    ax = sns.heatmap(df_cm)
    ax.set_ylabel('R')
    ax.set_xlabel('SD')
    ax.set_title('mean_degree_heatmap')
    plt.show()
myGraph = Graph("square",1,0,10)
print(myGraph.mean_degree())
#myGraph.Random_Movement()
#myGraph.Plot_Graph()
#print(myGraph.largest_component())
mean_degree_heatmap()

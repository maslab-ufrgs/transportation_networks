'''
Created on 22/08/2016

@author: Gabriel de O. Ramos
'''

from py_expression_eval import Parser

# represents a node in the network
class Node:
    def __init__(self, name):
        self.name = name    # name of the node

# represents an edge in the network
class Edge:
    def __init__(self, name, start, end, cost_function, param_name):
        self.name = name
        self.start = start
        self.end = end
        self.__cost_function = cost_function # cost function
        self.__param_name = param_name # name of the function's parameter (required during evaluation)
        
        self.__current_flow = 0.0
    
    # calculate the edge's cost based on its current flow
    # (if param_value is used, then the cost is calculated
    # based on it)
    def evaluate(self, param_value=None):
        if param_value == None:
            param_value = self.get_flow()
        
        return self.__cost_function.evaluate({self.__param_name: param_value})
        
    def set_flow(self, flow):
        self.__current_flow = flow
    
    def get_flow(self):
        return self.__current_flow

# generate a network from file
def generateNetwork(network_file_name):
    
    V = [] # vertices
    E = [] # edges
    F = {} # cost functions
    OD = [] # OD pairs
    
    lineid = 0
    for line in open(network_file_name, 'r'):
        
        lineid += 1
        
        # ignore \n
        line = line.rstrip()
        
        # ignore comments
        hash_pos = line.find('#')
        if hash_pos > -1:
            line = line[:hash_pos]
        
        # split the line
        taglist = line.split()
        if len(taglist) == 0:
            continue
        
        if taglist[0] == 'function':
            
            # process the params
            params = taglist[2][1:-1].split(',')
            if len(params) > 1:
                raise Exception('Cost functions with more than one parameter are not yet acceptable! (parameters defined: %s)' % str(params)[1:-1])
            
            # process the function
            expr = taglist[3]
            function = Parser().parse(expr)
            
            # handle the case where the parameter is not in the formula
            # (this needs to be handled because py-expression-eval does
            # not allows simplifying all variables of an expression) 
            if taglist[1] not in function.variables():
                expr = '%s+%s-%s' % (taglist[3], params[0], params[0])
                function = Parser().parse(expr)
            
            # process the constants
            constants = function.variables()
            if params[0] in constants: # the parameter must be ignored
                constants.remove(params[0]) 
            
            # store the function
            F[taglist[1]] = [params[0], constants, expr]
            
        elif taglist[0] == 'node':
            V.append(Node(taglist[1]))
            
        elif taglist[0] == 'dedge' or taglist[0] == 'edge': # dedge is a directed edge
            
            # process the function
            func_tuple = F[taglist[4]] # get the corresponding function
            param_values = dict(zip(func_tuple[1], map(float, taglist[5:]))) # associate constants and values specified in the line (in order of occurrence)
            function = Parser().parse(func_tuple[2]) # create the function
            function = function.simplify(param_values) # replace constants
            
            # create the edge(s)
            E.append(Edge(taglist[1], taglist[2], taglist[3], function, func_tuple[0]))
            if taglist[0] == 'edge':
                E.append(Edge('%s-%s'%(taglist[3], taglist[2]), taglist[3], taglist[2], function, func_tuple[0]))
            
        elif taglist[0] == 'od':
            OD.append(taglist[1])
        
        else:
            raise Exception('Network file does not comply with the specification! (line %d: "%s")' % (lineid, line))
    
    
    return V, E, OD

# print vertices and edges
def printGraph(N, E):
    print('nodes:')
    for node in N:
        print(node.name)
    print('edges (and free flow travel time):')
    for edge in E:
        print(edge.name, edge.evaluate(0))

# initializing procedure
if __name__ == '__main__':
    
    network_file_name = 'OW.net'
    
    # create a network from file
    Nodes, Edges, ODpairs = generateNetwork(network_file_name)
    
    printGraph(Nodes, Edges)
    
    # select an edge, set its flow, and print its cost
    anEdge = Edges[0]
    anEdge.set_flow(1000)
    print '%s has a flow of %f and costs %f' % (anEdge.name, anEdge.get_flow(), anEdge.evaluate())
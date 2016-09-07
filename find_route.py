#!/usr/bin/python

import pprint               # for development
from sys import argv,exit   # for handling system arguments
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
import heapq            # handwritten queue

### Classes ###

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
    
    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index,item) )
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


### FUNCTIONS ###

def Pprint( datatoprint ) :
    #  Input: list or dictionary
    # Return: Nothing
    #Purpose: quick code for development (debug) using pPrint
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(datatoprint)
    
def readfile(filename) :
	#   Input: "filename"
	#  Output: lines of file
	# Purpose: Try to open, read & close file < argv[1] >
    
    try:
        fp = open(filename,"r")
        data = fp.readlines()
        fp.close()
    
        return data
    
    except:
        print("Error Opening %s" % filename)
        exit(1)

def usage():   
    #   Input: nothing
    #  Output: usage for using program
    # Purpose: print usage and exit
    if len(argv) < 4 :
        print "Usage: %s  input_filename origin_city destination_city" % argv[0]
        print "example: %s input1.txt Bremen Frankfurt" % argv[0]
        exit(0)

def process_input():
    #   Input: nothing
    #  Output: Origin_city & Destination_city
    # Purpose: Check that the cities entered exist in <input_file>
    
    # process correct input
    if argv[2] not in find_dict.keys():
        print("%s <Origin_city> not found in %s" % (argv[2],argv[1]) )
        exit(1)
    
    if argv[3] not in find_dict.keys():
        print("%s <Destination_city> not found in %s" % (argv[3],argv[1]) )
        exit(1)
    
    return argv[2], argv[3]

def parse(data):
    #   Input: raw file data
    #  Output: a nested dictionary holding all the nodes
    # Purpose: parse data from file and put into nested dictionary, each key is a node

    dictionary = { }

    for line in data :
        token = line.strip()
        token = token.split(' ')
        
        if( token[0] ) :
            # token[0] = origination, token[1] = destination, token[2] = cost
            if 'END' not in token[0]  :
                
                # for each first destination read into dictionary w/ cost
                if token[0] not in dictionary.keys() :
                    dictionary[ token[0] ] = { token[1]: int(token[2]) }
                else :
                    dictionary[ token[0] ].update( {token[1]: int(token[2]) })
                
                # for each second destination reverse into dictionary w/ cost
                if token[1] not in dictionary.keys() :
                    dictionary[ token[1] ] = { token[0]: int(token[2]) }
                else :
                    dictionary[ token[1] ].update({ token[0] : int(token[2])} )
                
    return dictionary

def call_city( start, destination,cost ):
    #   Input: start location, destination, cost
    #  Output: recursively calling itself
    # Purpose: UCS algorithm on dictionary; keys are vertices
    
    # https://en.wikipedia.org/wiki/Priority_queue
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # https://docs.python.org/3/library/queue.html#Queue.PriorityQueue
    # https://www.google.com/#q=priority+queue+python

    visited = set()
    q = Q.PriorityQueue()
    q.put( (start, 0) )
    
    tmp_array = find_dict[ start ]
    # loop through each node city and create a path
    
    c = 1   # cost
    i = 0   # name
    while i < len( tmp_array ):
        
        path_array = find_dict[ tmp_array[i] ]
        
        # RECURSION CALL
        if tmp_array[i] != destination :
            if(DEBUG):
                print "Vertex: %s city: %s cost: %i " % (start, tmp_array[i], cost + tmp_array[c])
            
            # CATCH A PROBLEM
            if ( (cost + tmp_array[c]) >= 1000):
                exit(0)
            
            i+=2
            # put in array to save all other calls and iterations
            call_city( tmp_array[i],destination, cost + tmp_array[c] )
        
        # if index is at size length and not found escape node
        if ( i >= len(tmp_array) ) & ( tmp_array[i] != destination ):
            # break out of the loop
            i = len(tmp_array) * 2
        
        i += 2
        c += 2

def findavalue(dictionary):
    #   Input: a dictionary
    #  Output: nothing 
    # Purpose: debug code to find exact way to iterate vertices in nested dictionary
    for key in dictionary.keys():
        for secondkey in dictionary[key].keys():
            print("COST FROM %s TO %s is: %s" % (key,secondkey,dictionary[key][secondkey] ) )

def put(priority,item):
    #   Input: city-name (item) cost (priority)
    #
    # Purpose: update global dictionary
    pq.update( { priority:item } )

def pop():
    #   Input: nothing
    #  Output: pop'd values
    # Pupose: Remove Greatest number item from global Dictionary(pq)   
    tmp_cost = 0
    tmp_city = ''
    min = 0
    for i in pq.keys():
        if min == 0:
            min = int(i)

        elif int(i) <= min:
            min = int(i)
    
    tmp_cost = min
    tmp_city = pq[min]
    del pq[min]

    return tmp_cost, tmp_city

def ucs_old(q, graph, start, goal):
    #   Input: queue, dictionary, origination, destination
    #  Output: return exits loop
    # Purpose: Uniform Count Search
    visited = set()
    q.put( (0,start) ) 
    # for everything in the queue through into a 'queue' dict to iterate through and see what's
    # in there at any given point. Python Queue is for Threads and not iteritable.
    queue_check = { start:0 }     # only need to check for vertices
    

    # SUCCESSOR FUNCTION


    # count is for #DEBUG
    count = 0
    
    # loop do
    while q:
        # Empty frontier/priority queue
        if q.empty():
            print(" FAILED ")
            return

        # DEBUG
        if (DEBUG):
            print("Queue:")
            Pprint(queue_check)

        # POP FROM THE QUEUE       
        cost, city = q.get()
        # remove also from iterable queue
        del queue_check[city]
        
        # add node.STATE to explored
        #if city not in visited:
        visited.add(city)  

            # RETURN SOLUTION
        if city == goal:
            return

        # for each action in problem.ACTIONS(node.STATE) do
        for vertex in graph.keys():
            for nodeVertex in graph[vertex].keys():
                # nodeVertex FROM vertex is the ACTION

                # child <- CHILD-NODE(problem, node, action)
                # CHILD-NODE = graph[vertex][nodeVertex]; problem = goal; action = nodeVertex
                # NEED TO BE ABLE TO ITERATE THROUGH THE QUEUE
                #if (city not in visited) | ( city not in queue_check.keys() ) :  # | (city not in q):
                #    count += 1
                #    print("VISITED[%s]: %s" %  ( count,nodeVertex ) )
                #    q.put( (cost, nodeVertex ) )
                #    queue_check.update( {nodeVertex:count} )

                #    if(DEBUG):
                #        if count >= BREAK:
                #            return

                if nodeVertex not in visited:
                    total_cost = cost + graph[vertex][nodeVertex]  
                    print("%s : %s : %s" % (vertex, nodeVertex, total_cost) )
                    q.put( (total_cost,nodeVertex) )
                    queue_check.update( {nodeVertex:total_cost} )

def ucs(graph, start, goal):
    #   Input: dictionary, origin, destination
    #  Output: nothing
    # Purpose: GLOBAL PRIORITY QUEUE = pq = dictionary
    # uses hand coded priority queue

    explored = set()
    put( 0,start  ) 
    count = 0
    
    # loop do
    while 1:
        # Empty frontier/priority queue
        if not(bool(pq)):
            print(" FAILED ")
            return
        
        # POP FROM THE QUEUE
        cost, city = pop()
        if (DEBUG):
            print("COST: %s CITY: %s " % (cost, city) )
 
        # RETURN SOLUTION
        if city == goal:
            return
        
        # add node.STATE to explored
        explored.add(city)  

        # for each action in problem.ACTIONS(node.STATE) do
        for child in graph[city].keys():
            # child <- CHILD-NODE(problem, node, action)
            # CHILD-NODE = graph[city]; problem = goal; action = vertex
            
            # NEED TO BE ABLE TO ITERATE THROUGH THE QUEUE
            if (city not in explored ) | (city not in pq.items() ) :

                # frontier <- INSERT(child,frontier)
                put( graph[city][child], child )
                
                if(DEBUG):
                    count += 1
                    print("VISITED[%s]: %s" % ( count,city ) )
                    Pprint(pq)
                    if count >= BREAK:
                        exit()
                
                
                # if child.STATE is in frontier with higher PATH-COST then
                #   replace that frontier node with child
                #if nodeVertex in pq.items():
                for cost in pq.keys():
                    if pq[cost] == child:           # we want this specific child
                        #if (DEBUG):
                        #    print(" FOUND CHILD ")
                        # compare cost from queue to child
                        if cost >= graph[city][child]:
                            # replace one on priority queue with node
                            # delete/pop current pq[cost]
                            del pq[cost]
                            put( graph[city][child], child )
        
        if (DEBUG):
            print("<EXPLORED>")
            Pprint( explored)
            print("</EXPLORED>")
    
    

### MAIN ###

#GLOBALS#
DEBUG=True
BREAK=21
pq = {}

# check input
usage()

# grab data from file and parse it into dictionary
find_dict = parse( readfile( argv[1] ) )
# process input for desitination and origin cities
origin_city, destination_city = process_input()

if(DEBUG):
    Pprint(find_dict)

#findavalue(find_dict)
#print "all vertexes = %s " % find_dict.keys()

# Uniform Cost Selection Algorithm
# for vertex in find_dict.keys(): 
#call_city( origin_city, destination_city , 0 )
        

# TRYING TO DO HAND MADE QUEUE
q = {}
ucs(find_dict, origin_city, destination_city )

Pprint(pq)


# USING PYTHON PRIORITY QUEUE
#q = Q.PriorityQueue()
#ucs_old( q, find_dict, origin_city, destination_city )

#if(DEBUG):
#    while not q.empty():
#        print q.get()
           


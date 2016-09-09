#!/usr/bin/python

import pprint               # for development
from sys import argv,exit   # for handling system arguments
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
    
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

def search(graph, start, end):
    #   Input: Dictionary
    #  Output: nothing
    # Purpose: Uniform Cost Search, implemented using python's priority queue

    queue = Q.PriorityQueue()
    queue.put( (0, [start]) )
    
    loop = 0
    while not queue.empty():
        node = queue.get()

        current = node[1][len(node[1]) - 1]
        
        # found solution
        if end in node[1]:

            if(DEBUG):
                print("Path found: " + str(node[1]) + ", Cost = " + str(node[0]))

            print("distance: %s km" %  str(node[0]) )
            print("route:") 
            

            for _start in range( 0 , len( node[1]) - 1 ):
                # print the results from the node[1] array
                if _start == 0:
                    _cost = graph[ node[1][0] ][ node[1][ _start + 1 ]   ]
                    print("%s to %s, %s km " % ( node[1][0], node[1][ _start + 1 ], _cost ) )
                else:
                    _cost = graph[ node[1][_start] ][ node[1][ _start + 1 ] ]
                    print("%s to %s, %s km " % ( node[1][_start], node[1][ _start + 1 ], _cost ) )                    
            break

        cost = node[0]
        for neighbor in graph[current]:
            temp = node[1][:]
            temp.append(neighbor)
            total = cost + graph[current][neighbor] 
            queue.put( (total, temp) )
            
            loop += 1
            if loop >= Infinity:
                # this loop has iterated to a path size of well over one million
                print("distance: infinity")
                print("route:" )
                print("none")

                return
    

### MAIN ###

#GLOBALS#
DEBUG=False
BREAK=True
Infinity = 1000000

# check input
usage()

# grab data from file and parse it into dictionary
find_dict = parse( readfile( argv[1] ) )
# process input for desitination and origin cities
origin_city, destination_city = process_input()

if(DEBUG):
    Pprint(find_dict)

search (find_dict, origin_city, destination_city )

if(BREAK):
    # loop lots of options
    Pprint(find_dict)
    #keys = sorted(find_dict, key=lambda key: find_dict[key])
    keys = sorted( find_dict.iterkeys() )
    for i in keys:
        for j in keys:   
            if( i != j ):
                print("-----")
                print(" FROM %s TO %s " % (i, j) )
                search( find_dict, i, j )
                print("-----")


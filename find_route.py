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

def findavalue(dictionary):
    #   Input: a dictionary
    #  Output: nothing 
    # Purpose: debug code to find exact way to iterate vertices in nested dictionary
    for key in dictionary.keys():
        for secondkey in dictionary[key].keys():
            print("COST FROM %s TO %s is: %s" % (key,secondkey,dictionary[key][secondkey] ) )

def search(graph, start, end):
    #
    #
    #

    queue = Q.PriorityQueue()
    # _queue_check = {}
    queue.put( (0, [start]) )
    # _queue_check.update( { start : 0 } )
    
    loop = 0
    while not queue.empty():
        node = queue.get()
        #del _queue_check[start]

        current = node[1][len(node[1]) - 1]
        

        # found solution
        if end in node[1]:
            if(DEBUG):
                print("Path found: " + str(node[1]) + ", Cost = " + str(node[0]))
            
            print("distance: %s km" %  str(node[0]) )
            print("route:") 
            

            for _start in range( 0 , len( node[1]) - 1 ):
                '''
                Bremen to Dortmund, 234 km 
                Dortmund to Frankfurt, 221 km 
                '''
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
                print("distance: infinity")
                print("route:" )
                print("none")

                return
            
            #for _city in temp:
            #    _queue_check.update( { _city : total } )
            
            #Pprint([temp,total])
            #if( total >= BREAK):
            #    return
            # count = 0
            #for _check in temp:
            #    if _check == temp[0]:
            #        count += 1

            #if count >= Infinity:
            #    print("distance: infinity")
            #    print("route:" )
            #    print("none")
            #    return
            #    while not queue.empty():
            #        queue.get()


       


    

### MAIN ###

#GLOBALS#
DEBUG=False
BREAK=False
Infinity = 1000000
pq = {}

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
    Pprint(find_dict)
    for i in find_dict.keys():
        for j in find_dict[i].keys():
            print("-----")
            for k in find_dict.keys():
                for n in find_dict[k].keys():
                    if( (j != n) | (k != i) ):
                        print(" FROM %s TO %s " % (j, n) )
                        search( find_dict, j, n )
                        print("-----")


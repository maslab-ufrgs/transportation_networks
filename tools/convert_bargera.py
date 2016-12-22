#!/usr/bin/python
'''
Created on 22-Dec-2016

@author: Gabriel de O. Ramos <goramos@inf.ufrgs.br>
'''

import argparse
import datetime

def print_header(new_net, net_file_name, trips_file_name):
    new_net.write('########################################################################\n')
    new_net.write('#                                                                      #\n')
    new_net.write('# Network automatically generated using the convert_bargera.py script  #\n')
    new_net.write('#                                                                      #\n')
    new_net.write('# Input files:                                                         #\n')
    new_net.write('# - {:<66} #\n'.format(net_file_name))
    new_net.write('# - {:<66} #\n'.format(trips_file_name))
    new_net.write('#                                                                      #\n')
    new_net.write('# Generated on: %s                                   #\n' % datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
    new_net.write('#                                                                      #\n')
    new_net.write('########################################################################\n')

def write_new_net_file(new_net_file_name, N, L, OD):
    
    new_net = open(new_net_file_name, 'w')
    
    # the header
    print_header(new_net, net_file_name, trips_file_name)
    
    # the BPR function (all Bar-Gera's networks use this cost function) 
    new_net.write('#function name (args) formula\n')
    new_net.write('function BPR (f) t*(1+a*(f/c)^b)\n')
    
    # write the nodes
    new_net.write('#node name\n')
    for n in N:
        new_net.write('%s\n' % n)
    
    # write the links
    new_net.write('#edge name origin destination function constants\n')
    for l in L:
        new_net.write('%s\n' % l)
    
    # write the ODs
    new_net.write('#od name origin destination flow\n')
    for od in OD:
        new_net.write('%s\n' % od)
    
    new_net.close()
    

def convert_from_bargera(net_file_name, trips_file_name, new_net_file_name):
    
    # dicts of nodes, links and ODs
    nodes_names = []
    N = []
    L = []
    OD = []
    
    net = open(net_file_name, 'r')
    trips = open(trips_file_name, 'r')
    
    #process the net file
    reading_links = False
    lineid = 0
    for line in net:
        
        lineid += 1
        
        # ignore default whitespace chars
        line = line.strip() 
        
        if not line:
            continue
        
        elif line.startswith('<NUMBER OF NODES>'):
            
            # create the nodes (they are in the interval [1, <NUMBER OF NODES>] )
            for i in xrange(1, int(line.split()[3]) + 1):
                N.append('node %d' % i)
                nodes_names.append(str(i))
            
        elif reading_links:
            
            # split the line
            taglist = line.split()
            if len(taglist) == 0:
                continue
            
            if taglist[0] not in nodes_names or taglist[1] not in nodes_names:
                show_warning('Origin and/or destination node do/does not exist/s! (line %d)'%lineid)
                 
            # store the link definition
            L.append('dedge %s %s %s BPR %s %s %s %s' % ('%s-%s' % (taglist[0], taglist[1]), taglist[0], taglist[1], taglist[4], taglist[5], taglist[2], taglist[6]))
            
        # flag sinalising the begining of the edges' definitions
        elif line[0] == '~':
            reading_links = True
    
    #process the trips file
    current_origin = None
    lineid = 0
    for line in trips:
        
        lineid += 1
        
        # ignore default whitespace chars
        line = line.strip() 
        
        if not line:
            continue
        
        elif line.startswith('Origin'):
            
            current_origin = line.split()[1]
            
            if current_origin not in nodes_names:
                show_warning('Origin %s does not exists! (line %d)'%(current_origin, lineid))
            
        elif current_origin != None:
            
            # split the line
            taglist = line.replace(' ', '').replace('\t','').split(';')
            if len(taglist) == 0:
                continue
            
            for e in taglist[:-1]:
                d, flow = e.split(':')
                
                # store the OD definition
                OD.append('od %s %s %s %s' % (('%s|%s'%(current_origin, d)), current_origin, d, flow))
    
    net.close()
    trips.close()
    
    write_new_net_file(new_net_file_name, N, L, OD)

def show_warning(msg):
    print '[WARNING] %s' % msg

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='convert_bargera.py\nGenerates a network file (following Maslab\'s network files specification [1]) from a Bar-Gera\'s TNTP network file [2].',
        epilog = '\n\nREFERENCES' +
        '\n[1] http://wiki.inf.ufrgs.br/network_files_specification.' +
        '\n[2] https://github.com/bstabler/TransportationNetworks.' +
        '\n\nAUTHOR' +
        '\nCreated on December 22, 2016, by Gabriel de Oliveira Ramos <goramos@inf.ufrgs.br>.',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-n', dest='net_file', required=True,
                        help='the TNTP network file')
    parser.add_argument('-t', dest='trips_file', required=True,
                        help='the TNTP trips file')
    parser.add_argument('-o', dest='out_net_file', required=True,
                        help='the output network file (following Maslab\'s network files specification)')
    args = parser.parse_args()
    
    net_file_name = args.net_file
    trips_file_name = args.trips_file
    new_net_file_name = args.out_net_file
    
    convert_from_bargera(net_file_name, trips_file_name, new_net_file_name)
    
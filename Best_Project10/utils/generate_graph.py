import sys

def plot_graph(topology, start, stop, step):
    
    return







if __name__=='__main__':
    
    try:
        topology = sys.argv[1][:-3]
        start = int(sys.argv[2])
        stop = int(sys.argv[3])
        step = int(sys.argv[4])
        plot_graph(topology, start, stop, step)
    except IndexError ValueError:
        print("usage: ./utils/generate_graph.py <topology-file> <lamda-int-rate> <lamda-int-rate> <lamda-int-rate>")
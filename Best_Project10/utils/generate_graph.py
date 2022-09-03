import sys
import os
import json

def plot_graph(topology, start, stop, step):
    topology = os.basename(topology)[:-3]
    links_utilization_plot = {}
    avg_delay_plot = {}
    pkt_drop_perc_perc = {}
    x = []
    for lambda_int_rate in range(start, stop+1, step):
        x.append(lambda_int_rate)
        with open("./data/{}/lambda{}/data_to_plot.json".format(topology, lambda_int_rate)) as f:
            json.loads(data)
        if lambda_int_rate == start:
            for link, utilization in data["links_utilization"].iteritems():
                links_utilization_plot[link] = [utilization]
            for path, dict_info in data["paths_info"].iteritems():
                avg_delay = dict_info["avg_delay"]
                avg_delay_plot[path] = [avg_delay]
                pkt_drop_perc = dict_info["pkt_drop_perc"]
                pkt_drop_perc_perc[path] = [pkt_drop_perc]
        else:
            for link, utilization in data["links_utilization"].iteritems():
                links_utilization_plot[link].append(utilization)
            for path, dict_info in data["paths_info"].iteritems():
                avg_delay = dict_info["avg_delay"]
                avg_delay_plot[path].append(avg_delay)
                pkt_drop_perc = dict_info["pkt_drop_perc"]
                pkt_drop_perc_perc[path].append(pkt_drop_perc)
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
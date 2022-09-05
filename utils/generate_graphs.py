import sys
import os
import json
import matplotlib.pyplot as plt

def plot_graph(topology, start, stop, step):
    
    topology = os.path.basename(topology)
    y_lu = {}
    y_ad = {}
    y_pd = {}
    x = []
    for lambda_int_rate in range(start, stop+1, step):
        x.append(lambda_int_rate)
        with open("./data/{}/lambda{}/data_to_plot.json".format(topology, lambda_int_rate)) as f:
            data = json.load(f)
        if lambda_int_rate == start:
            for link, utilization in data["links_utilization"].items():
                y_lu[link] = [utilization]
            for path, dict_info in data["paths_info"].items():
                avg_delay = dict_info["avg_delay"]
                y_ad[path] = [avg_delay]
                pkt_drop_perc = dict_info["pkt_drop_perc"]
                y_pd[path] = [pkt_drop_perc]
        else:
            for link, utilization in data["links_utilization"].items():
                y_lu[link].append(utilization)
            for path, dict_info in data["paths_info"].items():
                avg_delay = dict_info["avg_delay"]
                y_ad[path].append(avg_delay)
                pkt_drop_perc = dict_info["pkt_drop_perc"]
                y_pd[path].append(pkt_drop_perc)

    folder = "./data/{}/plots_{}_{}_{}".format(topology, start, stop, step)
    if not os.path.exists(folder):
        os.mkdir(folder)

    for k, v in y_lu.items():
        plt.plot(x, v, label = k)
    plt.legend()
    plt.xlabel("lambda rate (pkt/s)")
    plt.ylabel("link utilization (%)")
    plt.savefig("{}/links_utilization.svg".format(folder), format='svg')
    plt.close()

    for k, v in y_ad.items():
        plt.plot(x, v, label = k)
    plt.legend()
    plt.xlabel("Lambda Rate (pkt/s)")
    plt.ylabel("end-to-end delay (s)")
    plt.savefig("{}/avg_delay.svg".format(folder), format='svg')
    plt.close()

    for k, v in y_pd.items():
        plt.plot(x, v, label = k)
    plt.legend()
    plt.xlabel("lambda rate (pkt/s)")
    plt.ylabel("packet drop (%)")
    plt.savefig("{}/pkt_drop.svg".format(folder), format='svg')
    plt.close()

    return



if __name__=='__main__':

    try:
        topology = sys.argv[1][:-3]
        start = int(sys.argv[2])
        stop = int(sys.argv[3])
        step = int(sys.argv[4])
        plot_graph(topology, start, stop, step)
    except ValueError:
        print("usage: ./utils/generate_graphs.py <topology-file> <lamda-int-rate> <lamda-int-rate> <lamda-int-rate>")
    except IndexError:
        print("usage: ./utils/generate_graphs.py <topology-file> <lamda-int-rate> <lamda-int-rate> <lamda-int-rate>")
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import random
from pyvis.network import Network
import networkx as nx
from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
damp = 0.85

def main_demo(num_pages, connections, num_iterations):
    i = 0
    pages = np.zeros((num_pages,num_iterations))
    while (i < num_iterations):
        for j in range(num_pages):
            soma = 0
            for node in connections:
                if j+1 in node.connections:
                    soma += pages[node.value-1][i-1]/len(node.connections)
                else:
                    soma += 0
            pages[j][i] = (1-damp) + damp * soma
        i += 1
    return pages


class Node:
    def __init__(self, value):
        self.value = value
        self.connections = []

    def __str__(self):
        return f"Node: {self.value}\n\tConnections: {self.connections}"


@app.route("/")
def index():
    num_pages = random.randint(1,10)
    num_iterations = 100

    net = Network('100%', '100%', notebook=True, directed =True)
    net.toggle_hide_edges_on_drag(True)
    net.barnes_hut()

    connections = []
    for i in range(num_pages):
        e1 = Node(i+1)
        lentgh = random.randint(1,num_pages)
        for j in range(lentgh):
            num = random.randint(1,num_pages)
            while num == i+1:
                num = random.randint(1,num_pages)
            e1.connections.append(num)

        e1.connections = list(set(e1.connections))
        print(e1)
        connections.append(e1)
    
    pages = main_demo(num_pages, connections, num_iterations)

    for node in connections:
        net.add_node(node.value, label=f"Node {node.value}", size=50, 
                title=f"Page Rank: {pages[node.value-1][-1]}\nConnected to: {node.connections}", physics=True)

    for node in connections:
        for con in node.connections:
            net.add_edge(node.value, con)

    net.toggle_physics(True)
    net.show("templates/basic.html")
    return render_template("basic.html")

if __name__ == "__main__":

    app.run(debug=True,host="0.0.0.0", port=8393, ssl_context='adhoc')
    app.logger.info( flask.request.remote_addr)
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import random

damp = 0.85

def guesses(A, B):
    i = 0
    mean = 0
    a = []
    b = []
    while (i < 40 and mean != 1):
        i += 1
        print(F"{i} -> a: {A} b: {B}")
        A = (1-damp) + damp * B
        B = (1-damp) + damp * A
        a.append(A)
        b.append(B)
        mean = (A + B) / 2
    print(F"Average pagerank: {mean}")
    ypoints = np.array(range(1,41))
    plt.plot(ypoints, a)
    plt.plot(ypoints, b)
    plt.xlabel("Number of calculations")
    plt.ylabel("Calculated PageRank")
    plt.legend(["A", "B"])
    plt.show()


def big_networks(A, B, C, D):
    i = 0
    mean = 0
    a = []
    b = []
    c = []
    d = []
    while (i < 40 and mean != 1):
        i += 1
        print(F"{i} -> a: {A}, b: {B}, c: {C} d: {D}")
        A = (1-damp) + damp * C
        B = (1-damp) + damp * (A/2)
        C = (1-damp) + damp * (A/2 + B + D)
        D = (1-damp)
        a.append(A)
        b.append(B)
        c.append(C)
        d.append(D)
        mean = (A + B) / 2
    print(F"Average pagerank: {mean}")
    ypoints = np.array(range(1,41))
    plt.plot(ypoints, a)
    plt.plot(ypoints, b)
    plt.plot(ypoints, c)
    plt.plot(ypoints, d)
    plt.xlabel("Number of calculations")
    plt.ylabel("Calculated PageRank")
    plt.legend(["A", "B", "C", "D"])
    plt.show()


def main_demo(num_pages, connections, num_iterations):
    i = 0
    pages = np.zeros((num_pages,num_iterations))
    while (i < num_iterations):
        for j in range(num_pages):
            soma = 0
            for k,v in connections.items():
                if j+1 in v:
                    soma += pages[k-1][i-1]/len(v)
                else:
                    soma += 0
            pages[j][i] = (1-damp) + damp * soma
        i += 1
    return pages



if __name__ == "__main__":
    if (sys.argv[1] == "-g"):
        guesses(float(sys.argv[2]), float(sys.argv[3]))
    elif (sys.argv[1] == "-bn"):
        big_networks(0,0,0,0)
    elif (sys.argv[1] == "-m"):
        num_pages = int(sys.argv[2])
        num_iterations = int(sys.argv[3])
        connections = {}

        for i in range(num_pages):
            connections[i+1] = []
            lentgh = random.randint(1,num_pages)
            for j in range(lentgh):
                num = random.randint(1,num_pages)
                while num == i+1:
                    num = random.randint(1,num_pages)
                connections[i+1].append(num)

            connections[i+1] = list(set(connections[i+1]))

        print(connections)
        pages = main_demo(num_pages, connections, num_iterations)
        ypoints = np.array(range(1,num_iterations+1))

        label = []
        for i in range(num_pages):
            plt.plot(ypoints, pages[i,:])
            label.append(i+1)

        plt.xlabel("Number of calculations")
        plt.ylabel("Calculated PageRank")
        plt.legend(label)
        plt.show()
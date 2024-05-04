import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os
import ast

# change this parameter from 10 to 20
moves = 10

it_deep_filename = [filename for filename in os.listdir('metrics/') if filename.startswith(f'ITDEEP_{moves}')]
minimax_filename = [filename for filename in os.listdir('metrics/') if filename.startswith(f'MINMAX_{moves}')]
mcts_filename = [filename for filename in os.listdir('metrics/') if filename.startswith(f'MCTS_{moves}')]
print(it_deep_filename)
def calculate_avg_time(file_list):
    for file in file_list:
        with open(f'metrics/{file}', 'r') as file_obj:
            t = file_obj.read()
            t = ast.literal_eval(t)
            return sum(t)/len(t)
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i-0.1, y[i], y[i])
def plot_bar(x,y):
    plt.bar( x, y)
    plt.title(f'AVG MOVE TIME FOR FIRST {moves} MOVES')
    plt.xlabel('ALGORITHM')
    plt.ylabel('AVERGAE MOVE TIME IN SECONDS')
    addlabels(x,y)    
    plt.savefig(f'figures/bar_plot_avg_{moves}.png')
    plt.show()

x=['Iterative Deepening', 'Minimax', 'Monte Carlo TS']
y=[]
y.append(calculate_avg_time(it_deep_filename)/1000)
y.append(calculate_avg_time(minimax_filename)/1000)
y.append(calculate_avg_time(mcts_filename)/1000)
print(x,y)
y = [round(elem, 3) for elem in y]
plot_bar(x,y)


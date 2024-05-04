import matplotlib.pyplot as plt
import os
import ast

# change this parameter from 1 to 2
game = 1
it_deep_filename = [filename for filename in os.listdir('metrics/') if filename.startswith(f'ITDEEP_game')]
minimax_filename = [filename for filename in os.listdir('metrics/') if filename.startswith(f'MINMAX_game')]
#mcts_filename = [filename for filename in os.listdir('metrics/') if filename.startswith(f'MCTS_game{game}')]
print(it_deep_filename)
def calculate_avg_time(file_list):
    time1 = []
    for file in file_list:
        with open(f'metrics/{file}', 'r') as file_obj:
            t = file_obj.read()
            t = ast.literal_eval(t)
            time1.append(sum(t)/len(t))
            print(sum(t)/len(t))
            print(file)
    print("dgggrgr",time1)
    return sum(time1)/len(time1)

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i-0.1, y[i], y[i])

def plot_bar(x,y):
    plt.bar( x, y)
    plt.title(f'AVG MOVE TIME FOR 5 MOVES IN A PREDEFINED STARTEGY')
    plt.xlabel('ALGORITHM')
    plt.ylabel('AVERGAE MOVE TIME IN SECONDS')
    addlabels(x,y)    
    plt.savefig(f'figures/bar_plot_avg_game.png')
    plt.show()

x=['Iterative Deepening', 'Minimax']
y=[]
y.append(calculate_avg_time(it_deep_filename)/1000)
y.append(calculate_avg_time(minimax_filename)/1000)
#y.append(calculate_avg_time(mcts_filename)/1000)
print(x,y)
y = [round(elem, 3) for elem in y]
plot_bar(x,y)


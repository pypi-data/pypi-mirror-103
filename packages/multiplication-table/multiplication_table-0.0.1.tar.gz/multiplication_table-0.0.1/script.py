import multiplication_table as mt
import time
from tkinter import Tk, Canvas


# Enter number of table (can be an integer or a float)
#  and modulo number (must be an integer)
table_number = 2
modulo_number = 10


# Représentation console
graph_object = mt.Graph(table_number, modulo_number)
graph_object.sparse_matrix()
graph_object.print_graph()


# Représentation fixe
start = time.time()
root = Tk()
canvas = Canvas(root, width=750, height=750, bg='white')
canvas.pack(side="left", fill="both", expand=True)
mt.circle(canvas=canvas, center=(360, 360), radius=300,
          state_circle=True, background_circle="", outline_circle="black")
mt.dot(canvas=canvas, graph=graph_object, radius=300, center=360,
       color_graph=['black', 'purple', "blue", "red", "cyan"],
       color_name="red")
mt.all_edges(canvas=canvas, graph=graph_object, radius=300, center=360,
             color_graph=['black', 'purple', "blue", "red", "cyan"],
             edges_width=2)
root.mainloop()
end = time.time()
print("Fixe representation 'time : " + str(end-start))


# Representation interface
mt.Interface_gestion(speed=10, state_button=True, background='white',
                     state_circle=True,
                     color_graph=['black', 'purple', "blue", "red", "cyan"],
                     background_circle="", outline_circle='black',
                     color_name="red", edges_width=1)
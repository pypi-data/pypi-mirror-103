from multiplication_table.process_vis.base_vis import coord, angle_tab, circle, dot, name_vertices
from multiplication_table.process_math.Graph import Graph
#from tkinter import Tk, Canvas


def test_coord1():
    assert coord(200, 200, 40, 60) == (260, 160)


def test_coord2():
    assert type(coord(200, 200, 40, 60)) == tuple


def test_angle_tab1():
    assert type(angle_tab(3, Graph(2, 10))) == list


def test_angle_tab2():
    angle = angle_tab(3, Graph(2, 10))
    for i in range(len(angle)):
        assert type(angle[i]) == tuple


# The following tests are usually working but we had some issues with the 
# continuous integration on github.
# When the workflow is running, it would seem it can't find the tkinter 
# package.
# This is why we put these functions in comments
        
# def test_circle():
#     cnv = Canvas(Tk(), width=600, height=600)
#     center = (300, 300)
#     radius = 50
#     state = True
#     background = "white"
#     outline = "black"
#     assert type(circle(cnv, center, radius, state, background, outline)) == Canvas


# def test_dot():
#     cnv = Canvas(Tk(), width=600, height=600)
#     graphe = Graph(2, 10)
#     center = 300
#     radius = 50
#     color_graphe = ['black', 'purple', "blue", "red", "cyan"]
#     color_name = "red"
#     assert type(dot(cnv, graphe, radius, center, color_graphe, color_name)) == Canvas


# def test_name_vertices():
#     cnv = Canvas(Tk(), width=600, height=600)
#     graphe = Graph(2, 10)
#     center = 300
#     radius = 50
#     color = "red"
#     assert type(name_vertices(cnv, radius, graphe, center, color)) == Canvas

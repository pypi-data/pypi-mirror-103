import numpy as np


def circle(canvas, center, radius, state_circle, background_circle, outline_circle):
    """
    This function creates a circle item in the canvas.

    :param canvas: Canvas where the circle will be created
    :type canvas: tkinter.Canvas
    :param center: Coordinates of the circle's center in the Canvas
    :type center: tuple
    :param radius: Corresponds to the radius of the circle
    :type radius: int
    :param state_circle: Displays the circle's item if it takes True
    :type state_circle: boolean
    :param background_circle: Color of the circle's background
    :type background_circle: str
    :param outline_circle: Color of the circle's line
    :type outline_circle: str
    :return: Returns the Canvas widget
    :rtype: tkinter.Canvas
    """
    if (state_circle):
        xC, yC = center
        A = (xC-radius, yC-radius)
        B = (xC+radius, yC+radius)
        canvas.create_oval(A, B, width=1, fill=background_circle,
                           outline=outline_circle)
    return canvas


def coord(x, y, a, b):
    """
    Gives the coordinates to change the landmark for one point (integer
    numbers).

    :return: Returns coordinates of one point in the Canvas landmark
    :rtype: tuple
    :Example:
    \n
    >>> coord(200,200,40,60)
    (260,160)
    """
    return(x+b, y-a)


def angle_tab(radius, graph):
    """
    Returns a list of coordinates in the basic landmark which gives the
    coordinates of each vertex. Vertices are proportionally spaced
    (t = 2*pi/modulo number).

    :param radius: Radius of the circle
    :type radius: int
    :param graph: Graph object which gives the modulo number
    :type graph: multiplication_table.process_math.Graph.Graph
    :return: Returns a list of coordinates of all vertices
    :rtype: list
    """
    t = (2*np.pi)/(graph.mod)
    angle = [None] * graph.mod*100
    for k in range(graph.mod*100):
        angle[k] = (radius*np.cos(k*t/100), radius*np.sin(k*t/100))
    return angle


def dot(canvas, graph, radius, center, color_graph, color_name):
    """
    Adds the number of dots needed on the circle thanks to the
    :py:meth:`angle_tab` function. These points are proportionally spaced.
    Also, it calls :py:meth:`name_vertices` function which associates,
    for each dot, a number.

    :param canvas: Canvas where the dots items will be created
    :type canvas: tkinter.Canvas
    :param graph: Graph object which gives the modulo number 
    :type graph: multiplication_table.process_math.Graph.Graph 
    :param radius: Corresponds to the circle's radius
    :type radius: int
    :param center: Center of the circle in the Canvas
    :type center: int
    :param color_graph: List of colors to change the dots color
    :type color_graph: list
    :param color_name: Color of text items which represent the name of dots
    :type color_name: str
    :return: Returns the Canvas widget
    :rtype: tkinter.Canvas
    """
    col = 0
    if (graph.mod <= 150):
        angle = angle_tab(radius, graph)
        for j in np.arange(0, len(angle), 100):
            a, b = angle[j]
            A = coord(center-3, center-3, a, b)
            B = coord(center+3, center+3, a, b)
            # create modulo_number circles (R=3)
            canvas.create_oval(A, B, fill=color_graph[col])
            col = (col + 1) % len(color_graph)
        name_vertices(canvas, radius, graph, center, color_name)
    return canvas


def name_vertices(cnv, radius, graph, center, color_name):
    """
    Adds a name, for each vertex, around the circle.

    :param cnv: Canvas where the name will be added
    :type cnv: tkinter.Canvas
    :param radius: Corresponds to the circle's radius
    :type radius: int
    :param center: Center of the circle in the canvas
    :type center: int
    :param color_name: Color of text items
    :type color_name: str
    :return: Returns the Canvas widget
    :rtype: tkinter.Canvas
    """
    angle = angle_tab(radius+17, graph)
    for j in np.arange(0, len(angle), 100):
        a, b = angle[j]
        Dots_C = (center+b, center-a)
        if (graph.mod <= 150):
            size = str(int(min(18, 16*62/graph.mod)))
            cnv.create_text(Dots_C, text=str(int(j/100)),
                            font="Arial " + size + " bold", fill=color_name)
    return cnv

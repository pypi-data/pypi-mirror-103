import multiplication_table.process_vis.base_vis as bv


def all_edges(canvas, graph, radius, center, color_graph, edges_width):
    """
    This function reiterates the :py:meth:`one_edge` function for each vertex 
    i between 0 and the modulo number minus one.

    :param canvas: Canvas where edges will be created
    :type canvas: tkinter.Canvas
    :param graph: Graph object which gives the modulo number 
    :type graph: multiplication_table.process_math.Graph.Graph 
    :param radius: Corresponds to the circle's radius
    :type radius: int
    :param center: Center of the circle in the canvas
    :type center: int
    :param color_graph: List of colors to change the edges color
    :type color_graph: list
    :param edges_width: The width of edges in pixels
    :type edges_width: int
    :return: Returns the Canvas widget
    :rtype: tkinter.Canvas
    """
    angle = bv.angle_tab(radius, graph)
    col = 0
    for i in range(0, graph.mod):
        one_edge(graph, canvas, i, angle, center,
                 color_graph[col], edges_width)
        col = (col + 1) % len(color_graph)
    return canvas


def one_edge(graph, canvas, i, angle, center, color_graph, edges_width):
    """
    This function draws for any i fixed the edge between the vertex i and
    the vertex j. j is given by the result of the modular multiplication for i.

    :param graph: Graph object which gives the modulo number 
    :type graph: multiplication_table.process_math.Graph.Graph    
    :param canvas: Canvas where the edge will be created
    :type canvas: tkinter.Canvas
    :param i: Vertex i
    :type i: int
    :param angle:  List of coordinates of all vertices
    :type angle: list
    :param center: Center of the circle in the canvas
    :type center: int
    :param color_graph: Color of the edge
    :type color_graph: str
    :param edges_width: Width of edge in pixels
    :type edges_width: int
    :return: Returns the Canvas widget
    :rtype: tkinter.Canvas
    """
    j = int(graph.modulo_result(i)*100)
    xA, yA = angle[i*100]
    xB, yB = angle[j]
    A = bv.coord(center, center, xA, yA)
    B = bv.coord(center, center, xB, yB)
    canvas.create_line(A, B, fill=color_graph, width=edges_width)
    return canvas

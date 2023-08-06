from tkinter import Tk, Canvas, Scale, Button, Toplevel, Label, Scrollbar, Text, END, Y
import multiplication_table as mt
import multiplication_table.process_vis.edges_vis as ev
import multiplication_table.process_vis.base_vis as bv
from PIL import Image
import imageio
import os
import shutil
import time


class Interface_gestion:
    """
    This class contains functions which are used, for the graphical interface
    and makes the link between the different aspects of the visualization,
    as well as design and movement. 

    :param speed: Speed of the circle's movement
    :type speed: float
    :param state_circle: Displays the circle's item if it takes True
    :type state_circle: boolean
    :param color_graph: List of colors to change the dots and edges color
    :type color_graph: list
    :param background_circle: Color of the circle's background
    :type background_circle: str
    :param outline_circle: Color of the circle's line
    :type outline_circle: str
    :param color_name: Color of text items for vertices's name
    :type color_name: str
    :param edges_width: Width of edges in pixels
    :type edges_width: int
    :param nb_frame: The number of images captured for a gif since the last gif. 
    :type nb_frame: int
    :param nb_video: The number of gif already created
    :type nb_video: int
    :param root: Interface window
    :type root: tkinter.Tk
    :param canvas: Canvas where all items will be created
    :type canvas: tkinter.Canvas
    :param radius: Corresponds to the circle's radius
    :type radius: int
    :param center: Coordinates of the circle's center in the Canvas
    :type center: tuple
    :param N: Corresponds to the multiplication table. This number is rounded to :math:`10^{-2}`
    :type N: float
    :param mod: Corresponds to the modulo number
    :type mod: int
    :param graph: Graph object which gives the modulo number
    :type graph: multiplication_table.process_math.Graph.Graph
    :param peak_cursor: Slider which changes the modulo value according to the user
    :type peak_cursor: tkinter.Scale
    :param table_cursor: Slider which changes the table value according to the user
    :type table_cursor: tkinter.Scale
    :param state_button: State of the button **Play/Pause
    :type state_button: boolean
    """

    def __init__(self, speed, state_button, background, state_circle, color_graph, background_circle, outline_circle, color_name, edges_width): 
        """
        This method is a constructor method, that instantiates the speed
        and all other aspects.
        """
        self.nb_frame = 0
        self.nb_video = 0
        self.design_aspect(speed, state_circle, color_graph, background_circle,
                           outline_circle, color_name, edges_width)
        self.window_init(background)
        self.graph_init()
        self.graph_vis()
        self.slider()
        if (state_button):
            self.motion_button()
        self.root.mainloop()

    def design_aspect(self, speed, state_circle, color_graph, background_circle, outline_circle, color_name, edges_width):
        """
        Initialization of the design aspect parameters.

        :param speed: Speed of the circle's movement
        :type speed: float
        :param state_circle: Displays the circle's item if it takes True
        :type state_circle: boolean
        :param color_graph: List of colors to change the dots and edges color
        :type color_graph: list
        :param background_circle: Color of the circle's background
        :type background_circle: str
        :param outline_circle: Color of the circle's line
        :type outline_circle: str
        :param color_name: Color of text items for vertices's name
        :type color_name: str
        :param edges_width: Width of edges in pixels
        :type edges_width: int 
        """
        self.state_circle = state_circle
        self.outline_circle = outline_circle
        self.background_circle = background_circle
        self.color_name = color_name
        self.color_graph = color_graph
        self.speed = speed
        self.edges_width = edges_width

    def window_init(self, background):
        '''
        This method initializes the interface's window which refers to a
        rectangular area.
        The user can display screen through which he can interact.

        :param background: Color of the Canvas's background
        :type background: str
        '''
        self.root = Tk()
        self.cnv = Canvas(self.root, width=750, height=750, bg=background)
        self.cnv.pack(side="left", fill="both", expand=True)

    def graph_init(self):
        '''
        This method initializes the graph by default, as one its radius, its
        center, its multiplication table and its modulo.
        '''
        self.radius = 300
        self.N = 2.0
        self.modulo = 2
        self.center = (360, 360)
        self.graph = mt.Graph(self.N, self.modulo)

    def graph_vis(self):
        '''
        This method displays its execution's time in the terminal and also the 
        visualization part of the graph in other words dots, circle and edges.
        '''
        start = time.time()
        bv.circle(self.cnv, self.center, self.radius, self.state_circle,
                  self.background_circle, self.outline_circle)
        bv.dot(self.cnv, self.graph, self.radius, self.center[0],
               self.color_graph, self.color_name)
        ev.all_edges(self.cnv, self.graph, self.radius, self.center[0],
                     self.color_graph, self.edges_width)
        end = time.time()
        print("graph_vis'time : " + str(end-start))

    def table(self, n):
        '''
        This method sets the value of table thanks to the cursor and calls the
        function :py:meth:`show_update` that will change the Canvas.

        :param n: Represent the table number. For example if the cursor is moved to position 40; we have called the table 2.40.
        :type n: str
        '''
        self.N = float(n)
        self.graph.N = float(n)
        self.show_update()

    def vertices(self, mod):
        '''
        This method sets the value of modulo thanks to the cursor and calls the
        function :py:meth:`show_update` that will change the Canvas.

        :param mod: Represent the modulo number. For example if the cursor is moved to position 40; we have called the table 42.
        :type n: str
        '''
        self.modulo = int(mod)
        self.graph.mod = int(mod)
        self.show_update()

    def show_update(self):
        '''
        This method removes all Canvas items and recreates them after all the
        modifications
        '''
        start = time.time()
        self.cnv.delete("all")
        self.graph_vis()
        end = time.time()
        # print("Show_update'time : " + str(end-start))

    def slider(self):
        '''
        This method generates the two cursors which captures the number of the
        table and the number of vertices (modulo). The table cursor captures
        all tables from 2 to 400 with a step of 0.01 and the modulo cursor
        captures all modulo from 2 to 200 with a step of 1. They are
        placed horizontally and are 250 pixels long.
        '''
        self.peak_cursor = Scale(self.root, label="Modulo",
                                 font="Arial 12 bold", orient="horizontal",
                                 command=self.vertices, from_=2, to=200,
                                 length=250, repeatdelay=500)         
        self.peak_cursor.pack(pady=10, anchor="center")
        self.peak_cursor.set(10)
        self.table_cursor = Scale(self.root, label="Table",
                                  font="Arial 12 bold", orient="horizontal",
                                  command=self.table, from_=2, to=400,
                                  length=250, resolution=0.01,
                                  repeatdelay=1000)
        self.table_cursor.pack(pady=10, anchor="center")

    def move_value(self):
        '''
        This method increases the table number with a step of 0.01
        automatically and continuously
        '''
        self.state_button = not self.state_button
        while (self.state_button):
            self.table_cursor.set(self.table_cursor.get()+0.01)
            self.root.after(self.speed)
            self.root.update()

    def save_frame(self):
        """
        This method captures the current canvas, converts it to .png format
        and saves it in the correct directory "/temp/png{number_video}".
        """
        text = self.cnv.create_text(640, 730, fill="black", 
                                    font="Arial 12 italic bold",
                                    text="Table de "+str(self.N) + " modulo "+str(self.modulo))
        self.cnv.postscript(file="package_table/temp/eps/frame.eps")
        img = Image.open("package_table/temp/eps/frame.eps")
        if (self.nb_frame == 0):
            os.mkdir('package_table/temp/png'+str(self.nb_video))
        img.save('package_table/temp/png'+str(self.nb_video)+'/'+str(self.nb_frame)+'.png')
        self.cnv.delete(text)
        self.nb_frame = self.nb_frame + 1

    def save_video(self):
        """
        This method accesses the folder where the corresponding images 
        are saved.
        Then it creates the gif from the captured images.
        This latter is saved in the folder "/gif" in the format: gif{number}.gif
        """
        if (os.path.exists('package_table/temp/png'+str(self.nb_video))):
            folder = 'package_table/temp/png' + str(self.nb_video)
            frame = []
            for i in range(self.nb_frame):
                frame.append(str(i) + ".png")
            files = [f"{folder}\{file}" for file in frame]
            images = [imageio.imread(file) for file in files]
            imageio.mimwrite('gif/gif'+str(self.nb_video)+'.gif',
                             images, fps=5)
            self.nb_video = self.nb_video + 1
            self.nb_frame = 0

    def destroy_root(self):
        """
        This method deletes all the folders whose format is
        "/temp/png{number_video}".
        Then, it destroys all the canvas and closes the window.
        """
        for i in range(self.nb_video):
            shutil.rmtree('package_table/temp/png'+str(i))
        self.root.destroy()

    def create_table_window(self):
        """ 
        This method creates another window which contains all the modular
        calculations of the current Canvas.
        This window is managed by a scrollbar.
        """
        self.state_button = False
        new_root = Tk()
        new_root.geometry("300x350")
        scrollbar = Scrollbar(new_root)
        scrollbar.pack(side='right', fill=Y)
        textbox = Text(new_root)
        textbox.pack()
        for i in range(self.modulo):
            textbox.insert(END, str(self.N)+" x " + str(i) + " modulo "+str(self.modulo) + " = " + str(round(self.N* i % self.modulo, 2)) + "\n")
        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)
        new_root.mainloop()

    def create_description(self):
        """ 
        This method creates another window which contains a description of
        the different graphical performances.
        """
        newWindow = Toplevel(self.root)
        text = Label(newWindow, text="Play/Pause : The buttom to play or stop the animation. \n  ")
        text.pack()
        text = Label(newWindow, text="Photo : Take pictures of the circle, at the moment to make the gif.\n  ")
        text.pack()
        text = Label(newWindow, text="Vidéo : Make a gif from the images captured.\n  ")
        text.pack()
        text = Label(newWindow, text="Table of : Open the multiplication table.\n  ")
        text.pack()
        text = Label(newWindow, text="Quit : To quit the interface. \n You should pass by there and quit it, to avoid errors .\n  ")
        text.pack()

    def motion_button(self):
        '''
        Provides the control buttons, for example, the motion button which
        actives the animation.
        '''
        self.state_button = False
        button_play = Button(self.root, text="Play/Pause",
                             command=self.move_value)
        button_play.pack(padx=50, pady=5, side="top")
        button_photo = Button(self.root, text="Photo",
                              command=self.save_frame)
        button_photo.pack(padx=50, pady=5, side="top")
        button_video = Button(self.root, text="Vidéo",
                              command=self.save_video)
        button_video.pack(padx=50, pady=5, side="top")
        button_table_window = Button(self.root, text="Table of",
                                     command=self.create_table_window)
        button_table_window.pack(padx=50, pady=5, side="top")
        button_description = Button(self.root, text="Description",
                                     command=self.create_description)
        button_description.pack(padx=50, pady=5, side="top")
        quit = Button(self.root, text="Quit", fg="black",
                      command=self.destroy_root)
        quit.pack(padx=50, pady=5, side="bottom")

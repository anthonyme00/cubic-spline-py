from tkinter import *
from tkinter.messagebox import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.figure as fig
import numpy as np

from Spline.spline import CubicSpline

class MainView:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x600")
        self.root.title("Spline Demo")
        
        self.valuesStringY = StringVar()
        Label(self.root, text = "Masukan Value Y: ").grid(row=6, column=1, pady=10, sticky="e")
        Entry(self.root, textvariable=self.valuesStringY, width=50).grid(row=6,column=2, pady=10, columnspan=5, sticky="w")
        
        self.valuesStringX = StringVar()
        Label(self.root, text = "Masukan Value X: ").grid(row=5, column=1, pady=10, sticky="e")
        self.__xEntry = Entry(self.root, textvariable=self.valuesStringX, width=50)
        self.__xEntry.grid(row=5,column=2, pady=10, columnspan=5, sticky="w")

        #input awal
        self.valuesStringY.set("0, 3, 3, 2, 5")
        self.valuesStringX.set("3, 4, 2, 1, 0")

        self.resolutionString = StringVar()
        Label(self.root, text = "Masukan Resolusi : ").grid(row=7, column=1, pady=10, sticky="e")
        resolutionInput = Entry(self.root, textvariable=self.resolutionString, width=10).grid(row=7,column=2, pady=10, columnspan=5, sticky="w")
        self.resolutionString.set("1000")

        self.isClosed = IntVar()
        Checkbutton(self.root, variable=self.isClosed).grid(row=7, column=4, sticky="w")
        Label(self.root, text = "Spline tertutup : ").grid(row=7, column=3, sticky="e")

        def set2D():
            self.__xEntry["state"] = DISABLED if self.is2D.get() != 1 else NORMAL

        self.is2D = IntVar()
        Checkbutton(self.root, variable=self.is2D, command=set2D).grid(row=8, column=4, sticky="w")
        Label(self.root, text = "Spline 2D : ").grid(row=8, column=3, sticky="e")
        self.is2D.set(1)

        submitValue = Button(self.root, command=self.update, text="Submit").grid(row=9, column=2, pady=10)

        self.figure = fig.Figure(figsize=(5, 4), dpi=100)

        self.plt = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=1,column=1,rowspan=4,columnspan=4)

        self.update()

        self.root.mainloop()

    def update(self):
        valuesY =  self.valuesStringY.get().split(',')
        valuesX =  self.valuesStringX.get().split(',')

        for i in valuesY:
            try:
                float(i)
            except ValueError:
                showwarning("Can't parse input Y", """Masukan angka dengan desimal titik dan dibatasi koma.\nContoh: "1, 2.3, 3, 4.5" """)
                return

        if(self.is2D.get() == 1):
            for i in valuesX:
                try:
                    float(i)
                except ValueError:
                    showwarning("Can't parse input X", """Masukan angka dengan desimal titik dan dibatasi koma.\nContoh: "1, 2.3, 3, 4.5" """)
                    return

        if(len(valuesY) != len(valuesX) and self.is2D.get() == 1):
            showwarning('Spline 2D harus memiliki jumlah titik yang sama!')
            return

        resolution = self.resolutionString.get()
        try:
            resolution = int(resolution)
        except ValueError:
            showwarning("Can't parse input", """Masukan resolusi berupa integer""")
            return

        valuesY = [float(i) for i in valuesY]
        valuesX = [float(i) for i in valuesX]

        nums = np.linspace(0, len(valuesY) - 1, num=resolution)
        if(self.isClosed.get() == 1):
            nums = np.linspace(0, len(valuesY), num=resolution)
            nums = nums[:-1]

        points = np.arange(0, len(valuesY))

        interpolatedY = []
        interpolatedX = []
        splineY = CubicSpline(valuesY, self.isClosed.get() == 1)
        splineX = CubicSpline(valuesX, self.isClosed.get() == 1)
        for i in nums:
            interpolatedY.append(splineY.getPoint(i))
            if(self.is2D.get() == 1):
                interpolatedX.append(splineX.getPoint(i))

        self.plt.clear()
        self.plt.plot(interpolatedX if self.is2D.get() == 1 else nums, interpolatedY)
        self.plt.scatter(valuesX if self.is2D.get() == 1 else points, valuesY, c="orange")
        old = self.canvas.get_tk_widget()
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=1,column=1,rowspan=4,columnspan=4)
        old.destroy()

app = MainView()
        
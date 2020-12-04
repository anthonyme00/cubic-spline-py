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
        
        self.valuesString = StringVar()
        Label(self.root, text = "Masukan Value").grid(row=5, column=1, pady=10, sticky="e")
        valuesInput = Entry(self.root, textvariable=self.valuesString, width=50).grid(row=5,column=2, pady=10, columnspan=5, sticky="w")
        self.valuesString.set("0, 3, 5.2, 1.3, 2.1, 3.5, 6.1, 1.3, 10.5, 12.1, 1.2, 0.5, 3.5, 5")

        self.resolutionString = StringVar()
        Label(self.root, text = "Masukan Resolusi").grid(row=6, column=1, pady=10, sticky="e")
        resolutionInput = Entry(self.root, textvariable=self.resolutionString, width=10).grid(row=6,column=2, pady=10, columnspan=5, sticky="w")
        self.resolutionString.set("1000")

        submitValue = Button(self.root, command=self.update, text="Submit").grid(row=7, column=2, pady=10)

        self.figure = fig.Figure(figsize=(5, 4), dpi=100)

        self.plt = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=1,column=1,rowspan=4,columnspan=4)

        self.update()

        self.root.mainloop()

    def update(self):
        values =  self.valuesString.get().split(',')

        for i in values:
            try:
                float(i)
            except ValueError:
                showwarning("Can't parse input", """Masukan angka dengan desimal titik dan dibatasi koma.\nContoh: "1, 2.3, 3, 4.5" """)

        resolution = self.resolutionString.get()
        try:
            resolution = int(resolution)
        except ValueError:
            showwarning("Can't parse input", """Masukan resolusi berupa integer""")

        values = [float(i) for i in values]

        nums = np.linspace(0, len(values) - 1, num=resolution)
        points = np.arange(0, len(values))

        
        interpolated = []
        spline = CubicSpline(values, False)
        for i in nums:
            interpolated.append(spline.getPoint(i))

        self.plt.clear()
        self.plt.plot(nums, interpolated)
        self.plt.scatter(points, values, c="orange")
        old = self.canvas.get_tk_widget()
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=1,column=1,rowspan=4,columnspan=4)
        old.destroy()

app = MainView()
        
# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

    
class MplWidget(QWidget):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.canvas = FigureCanvas(Figure(facecolor='black'))
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111, facecolor='black')
        self.canvas.axes.tick_params(labelcolor='green')
        self.canvas.axes.title.set_color('green')
        self.canvas.axes.spines['bottom'].set_color('green')
        self.canvas.axes.spines['left'].set_color('green')
        self.canvas.axes.spines['right'].set_color('green')
        self.canvas.axes.spines['top'].set_color('green')
        self.setLayout(vertical_layout)


from tkinter import *
from tkinter import ttk
import numpy as np

class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.add_point)
        #self.bind("<B1-Motion>", self.add_line)
        self.points = np.empty(shape=(0,2), dtype=int)
        self.polygon = None
        self.create_text((110,20), text="Click anywhere to place a vertex.")
        
    def add_point(self, event):
        self.points = np.vstack([self.points, [event.x, event.y]])
        print(self.points)
        self.update_polygon()
            
    def update_polygon(self):
        if self.points.shape[0] != 0:
            self.delete(self.polygon)
            self.polygon = self.create_polygon(
                np.reshape(self.points, (1,-1)).tolist(), 
                fill="white",
                outline="white")
    #def update_sdf(self):
        
        
root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sketch = Sketchpad(root)
sketch.grid(column=0, row=0, sticky=(N, W, E, S))

root.mainloop()
from tkinter import *
from tkinter import ttk
import numpy as np
from PIL import Image, ImageDraw

class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.add_point)
        self.create_text((110,20), text="Click anywhere to place a vertex.")
        self.vertices = []
        self.polygon = None
        
    def add_point(self, event):
        self.vertices += [event.x, event.y]
        self.update_polygon()
            
    def update_polygon(self):
        if len(self.vertices)>=4: # if at least 2 vertices have been placed
            self.delete(self.polygon)
            self.polygon = self.create_polygon(
                self.vertices,
                fill="white",
                outline="white"
            )

            canvas_width = self.winfo_width()
            canvas_height = self.winfo_height()
            self.image = Image.new("RGB",(canvas_width, canvas_height),"black")
            self.draw = ImageDraw.Draw(self.image)
            print(self.vertices)
            self.draw.polygon(
                self.vertices,
                fill="white",
                outline="white"
            )
        
root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sketch = Sketchpad(root)
sketch.grid(column=0, row=0, sticky=(N, W, E, S))

root.mainloop()
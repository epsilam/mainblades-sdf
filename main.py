from tkinter import *
from src.polygonsketchpad import PolygonSketchpad

if __name__ == "__main__":
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    sketch = PolygonSketchpad(root)
    sketch.grid(column=0, row=0, sticky=(N, W, E, S))
    
    root.mainloop()
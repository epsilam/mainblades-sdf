from tkinter import *
import numpy as np
from PIL import Image, ImageDraw, ImageTk
import skfmm

class PolygonSketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.add_point)
        self.create_text((110,20), text="Click anywhere to place a vertex.")
        self.vertices = []
        self.polygon = None
        
    def add_point(self, event):
        self.vertices += [event.x, event.y]
        if len(self.vertices)>=4: # if at least 2 vertices have been placed
            self.delete("all")
            self.add_sdf_image()
            self.add_polygon()
            self.create_text((110,20), text="Click anywhere to place a vertex.")
            
    def add_polygon(self):
        self.delete(self.polygon)
        self.polygon = self.create_polygon(self.vertices, 
                                           fill='',
                                           outline="blue")

    def add_sdf_image(self):
        # Create PIL image of polygon
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        image = Image.new("1",(canvas_width, canvas_height),"black")
        draw = ImageDraw.Draw(image)
        draw.polygon(self.vertices, fill="white", outline="white")
        # Extract the image to numpy array.
        polygon_image = np.array(image.getdata()) \
            .reshape(image.size[1], image.size[0])
        # Normalize the image so the polygon boundary is the zero contour.
        polygon_image[polygon_image == 255] = 1
        polygon_image[polygon_image == 0] = -1
        # Compute SDF
        sdf = skfmm.distance(polygon_image)
        # Separate SDF into positive and negative parts
        pos_img = np.copy(sdf)
        pos_img[pos_img < 0] = 0
        pos_img = np.rint(pos_img / np.max(pos_img) * 255)
        neg_img = np.copy(sdf)
        neg_img[neg_img > 0] = 0
        neg_img = np.rint(neg_img / np.min(neg_img) * 255)
        
        img = np.dstack((255*(neg_img>0)-neg_img, 255*(pos_img<0)-pos_img, 10*np.ones_like(sdf))) \
            .astype(np.uint8)
        
        photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        label = Label(image=photo)
        label.image = photo
        self.sdf_image = self.create_image(0,0, image=label.image, anchor='nw')
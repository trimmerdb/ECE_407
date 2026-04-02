
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from cartopy import crs as ccrs, feature as cfeature # pip install cartopy
import tkinter as tk


# The main tkinter window
window = tk.Tk()

# setting the title and 
window.title('Plotting in Tkinter')

# setting the dimensions of 
# the main window
window.geometry("500x500")



fig = plt.figure(figsize=(11, 8.5))
ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=-75))
ax.set_title("A Geo-referenced subplot, Plate Carree projection");

ax.coastlines()
# ax.stock_img()
ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='black')
ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='brown')

canvas = FigureCanvasTkAgg(fig, master = window)  
canvas.draw()

# placing the canvas on the Tkinter window
canvas.get_tk_widget().pack()

# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas,
                                window)
toolbar.update()

# placing the toolbar on the Tkinter window
canvas.get_tk_widget().pack()

# run the gui
window.mainloop()
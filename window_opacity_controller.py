import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import ctypes

def set_window_opacity(hwnd, opacity):
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    LWA_ALPHA = 0x00000002

    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, int(opacity * 255), LWA_ALPHA)

def pin_window(hwnd):
    HWND_TOPMOST = -1
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

def unpin_window(hwnd):
    HWND_NOTOPMOST = -2
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

def on_slider_change(value):
    opacity = float(value) / 100  # Convert the value to float
    if selected_window_hwnd:
        set_window_opacity(selected_window_hwnd, opacity)

def on_window_select(event):
    global selected_window_hwnd
    selection = window_list.curselection()
    if selection:
        selected_window_hwnd = window_hwnds[selection[0]]._hWnd

def on_pin_button_click():
    if selected_window_hwnd:
        pin_window(selected_window_hwnd)

def on_unpin_button_click():
    if selected_window_hwnd:
        unpin_window(selected_window_hwnd)

selected_window_hwnd = None

# Create the main application window
root = tk.Tk()
root.title("Window Opacity Controller")
root.geometry("400x400")
root.resizable(False, False)

# Create a frame for the slider
frame_slider = ttk.Frame(root, padding="10")
frame_slider.pack(fill=tk.BOTH, expand=True)

# Add a label for the slider
label = ttk.Label(frame_slider, text="Adjust Opacity:")
label.pack(anchor=tk.W, pady=5)

# Create the slider for opacity adjustment
slider = ttk.Scale(frame_slider, from_=0, to=100, orient='horizontal', command=on_slider_change)
slider.set(100)
slider.pack(fill=tk.X, pady=5)

# Create a frame for the window list
frame_list = ttk.Frame(root, padding="10")
frame_list.pack(fill=tk.BOTH, expand=True)

# Add a label for the window list
label_list = ttk.Label(frame_list, text="Select a Window:")
label_list.pack(anchor=tk.W, pady=5)

# Create a Listbox to show the window titles
window_list = tk.Listbox(frame_list, height=10)
window_titles = gw.getAllTitles()
window_hwnds = gw.getAllWindows()
for title in window_titles:
    window_list.insert(tk.END, title)
window_list.pack(fill=tk.BOTH, expand=True, pady=5)

window_list.bind('<<ListboxSelect>>', on_window_select)

# Create a frame for the pin/unpin buttons
frame_buttons = ttk.Frame(root, padding="10")
frame_buttons.pack(fill=tk.BOTH, expand=True)

# Add Pin and Unpin buttons
pin_button = ttk.Button(frame_buttons, text="Pin Window", command=on_pin_button_click)
pin_button.pack(side=tk.LEFT, padx=5, pady=5)

unpin_button = ttk.Button(frame_buttons, text="Unpin Window", command=on_unpin_button_click)
unpin_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Start the Tkinter main loop
root.mainloop()

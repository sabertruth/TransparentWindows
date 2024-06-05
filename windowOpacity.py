import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import ctypes

def get_application_name(title):
    return title.split(" - ")[0]

def set_window_opacity(hwnd, opacity):
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    LWA_ALPHA = 0x00000002

    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, int(opacity * 255), LWA_ALPHA)

def reset_window_opacity(hwnd):
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style & ~WS_EX_LAYERED)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, 0x00000002)

def pin_window(hwnd):
    HWND_TOPMOST = 0
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_SHOWWINDOW = 0x0040
    SWP_DRAWFRAME = 0x0020
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW | SWP_DRAWFRAME)
    #print("pin here")

def unpin_window(hwnd):
    HWND_NOTOPMOST = -2
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_SHOWWINDOW = 0x0040
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
    #print("unpin here")

def pin_selected_window():
    if selected_window_hwnd:
        pin_window(selected_window_hwnd)
        update_window_list()

def unpin_all_windows():
    for hwnd in window_hwnds:
        unpin_window(hwnd)
    update_window_list()

def revert_single_window():
    if selected_window_hwnd:
        reset_window_opacity(selected_window_hwnd)
        slider.set(100)

def reset_all_windows():
    for hwnd in window_hwnds:
        reset_window_opacity(hwnd)
    slider.set(100)

def on_slider_change(value):
    opacity = int(value) / 100
    if selected_window_hwnd:
        set_window_opacity(selected_window_hwnd, opacity)

def on_window_select(event):
    global selected_window_hwnd
    selection = window_list.curselection()
    if selection:
        selected_window_hwnd = window_hwnds[selection[0]]  # Use window handle directly

def refresh_window_list():
    window_list.delete(0, tk.END)
    window_hwnds.clear()
    window_titles.clear()
    for window in gw.getAllWindows():
        if window.title and window.title not in ["Program Manager", "Microsoft Text Input Application"]:
            window_hwnds.append(window._hWnd)
            window_titles.append(get_application_name(window.title))
    update_window_list()



def update_window_list():
    window_list.delete(0, tk.END)
    for i, title in enumerate(window_titles):
        window_list.insert(tk.END, title)
        hwnd = window_hwnds[i]
        if is_window_pinned(hwnd):
            window_list.itemconfig(i, {'bg': 'lightblue'})

def is_window_pinned(hwnd):
    return ctypes.windll.user32.GetWindowLongW(hwnd, -8) & 0x00000008 != 0  # WS_EX_TOPMOST is the extended window style

def on_closing():
    reset_all_windows()
    root.destroy()

selected_window_hwnd = None
window_hwnds = []
window_titles = []



root = tk.Tk()
root.title("Window Opacity Controller")

# Set the initial size of the window
root.geometry('450x400')  # Width x Height

root.protocol("WM_DELETE_WINDOW", on_closing)

slider = tk.Scale(root, from_=0, to=100, orient='horizontal', command=on_slider_change)
slider.set(100)  # Set default value to 100

window_list_frame = ttk.Frame(root)

window_list = tk.Listbox(window_list_frame)
refresh_window_list()

# Populating buttons on the frame
refresh_button = ttk.Button(root, text="Refresh", command=refresh_window_list)
reset_button = ttk.Button(root, text="Reset All", command=reset_all_windows)
revert_button = ttk.Button(root, text="Revert", command=revert_single_window)
pin_button = ttk.Button(root, text="Show Selected", command=pin_selected_window)
unpin_button = ttk.Button(root, text="Unpin All", command=unpin_all_windows)

# Use grid geometry manager
slider.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
window_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
refresh_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
reset_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
revert_button.grid(row=3, column=1, padx=10, pady=10, sticky='ew')
pin_button.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
unpin_button.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

window_list.pack(fill=tk.BOTH, expand=True)

window_list_frame.columnconfigure(0, weight=1)
window_list_frame.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

window_list.bind('<<ListboxSelect>>', on_window_select)

root.mainloop()

import tkinter as tk
from collect_data import collect_data,stop
import threading


root = tk.Tk()
root.title("data interface")
root.geometry("800x800")


collect_thread = -1


def button1_click():
    global collect_thread
    print("Collect clicked")
    text = entry.get()
    collect_thread = threading.Thread(target=collect_data,args=(text,))
    collect_thread.start()

def button2_click():
    global collect_thread
    print("Stop clicked")
    stop()
    print('false')
    collect_thread.join()
    print('stopped')

def button3_click():
    print("Button 3 clicked")

# Adding the background image
#img = PhotoImage(file="pictures\\background.png")
#background_label = tk.Label(root, image=img)
#background_label.place(x=0, y=0, relwidth=1000, relheight=1000)

button1 = tk.Button(root, text="Collect data", command=button1_click)
button2 = tk.Button(root, text="stop", command=button2_click)
button3 = tk.Button(root, text="Liam", command=button3_click)


label = tk.Label(root, text="Enter username:")
label.pack()

entry = tk.Entry(root)
entry.pack()

# Placing buttons on top of the background image
button1.place(x=100, y=100)
button2.place(x=600, y=100)
button3.pack()

root.mainloop()

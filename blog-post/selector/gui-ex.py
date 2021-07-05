from tkinter import *


top = Tk()

mb = Menubutton(top, text="Log level", relief=RAISED)
mb2 = Menubutton(top, text="Output location", relief=RAISED)
# mb3 = Message(top, text="Example output: -Xlog:gc*::tid")


w = Text(top, height=1, borderwidth=0)
w.insert(1.0, "Example output: -Xlog::gc*:./outputs/logfile.log")


w.configure(state="disabled")

# if tkinter is 8.5 or above you'll want the selection background
# to appear like it does when the widget is activated
# comment this out for older versions of Tkinter
w.configure(inactiveselectbackground=w.cget("selectbackground"))

mb.grid()
mb.menu = Menu(mb, tearoff=0)
mb["menu"] = mb.menu

Item0 = IntVar()
Item1 = IntVar()
Item2 = IntVar()
loglevel_options = [IntVar() for i in range(5)]
output_options = [IntVar(), IntVar(), Entry()]

mb.menu.add_checkbutton(label="Error", variable=loglevel_options[0])
mb.menu.add_checkbutton(label="Warning", variable=loglevel_options[1])
mb.menu.add_checkbutton(label="Info", variable=loglevel_options[2])
mb.menu.add_checkbutton(label="Trace", variable=loglevel_options[3])
mb.menu.add_checkbutton(label="Debug", variable=loglevel_options[4])

mb2.grid()
mb2.menu = Menu(mb2, tearoff=1)
mb2["menu"] = mb2.menu
mb2.menu.add_checkbutton(label="Stderr", variable=output_options[0])
mb2.menu.add_checkbutton(label="Stdout", variable=output_options[1])
mb2.menu.add_checkbutton(label="enter file name here", variable=output_options[2])

w.grid()

"""This part is only for testing
def Item_test():
    if Item0.get() == True:
        print "Item0 True"
    elif Item0.get() == False:
        print "Item0 False"
    else:
        print Item0.get()
    if Item1.get() == True:
        print "Item1 True"
    elif Item1.get() == False:
        print "Item1 False"
    else:
        print Item1.get()
    if Item2.get() == True:
        print "Item2 True"
    elif Item2.get() == False:
        print "Item2 False"
    else:
        print Item2.get()

button1 = Button(top, text="Item True/False Test", command = Item_test)
button1.pack()
"""
# mb.pack()
top.mainloop()

import Tkinter as tk
import ScrolledText as tkst
from net.PyEZ_Connect import JunOS_Connection

root=tk.Tk()

frame=tk.Frame(root)
frame.grid(row=0,column=0)


tvar=tk.StringVar()
r=str(JunOS_Connection().show())


tvar.set(r)



#scroll=tk.Label(frame, textvariable=tvar)
#scroll.grid(row=0, column=0, sticky="W")

t=tkst.ScrolledText(frame, width=40, height=40)
t.grid(row=0, column=0)

t.insert("insert", r)
root.mainloop()
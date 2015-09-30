import Tkinter as tk
import ScrolledText as tkst
from net.PyEZ_Connect import JunOS_Connection

class Log_box:
    root=tk.Tk()

    frame=tk.Frame(root)
    frame.grid(row=0,column=0)

    r=str(JunOS_Connection().show())
    #print r.replace("}")
    #r.strip("{")
    t=tkst.ScrolledText(frame, width=50, height=20)
    t.grid(row=0, column=0)
    t.insert("insert", r)

    with open("Configuration.config", "w") as text_file:
        text_file.write(r)
        text_file.close()

    #t.delete(0,10)
    root.mainloop()

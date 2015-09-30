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


    t=tkst.ScrolledText(frame, width=80, height=40)
    t.grid(row=0, column=0)

    with open("Configuration.config", "w") as text_file:
        text_file.write(r)
        text_file.close()


    t.insert("insert", r)

    #t.delete(0,10)
    root.mainloop()

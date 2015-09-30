import Tkinter as tk
import ScrolledText as tkst
from net.PyEZ_Connect import JunOS_Connection

class Log_box:
    root=tk.Tk()

    #########################
    #   Connect to JunOS    #
    #########################
    config=str(JunOS_Connection().show())    #return self.dev_Connect.cli("show configuration")

    #########################
    #   Create ScrolledText #
    #########################
    textarea=tkst.ScrolledText(root, width=50, height=20)
    textarea.grid(row=0, column=0)

    #########################
    #   EMPTY TEXT AREA     #
    #########################
    textarea.delete(0.0, "end")     #### 0.0 = row0, column0
                                    #### Specify which row to delete
    #########################
    #   Insert to Text Area #
    #########################
    textarea.insert("insert", config)

    #########################
    #   Write to Document   #
    #########################
    with open("Configuration.config", "w") as text_file:
        text_file.write(config)
        text_file.close()

    ###Run Inter
    root.mainloop()

####Run Program
run=Log_box()
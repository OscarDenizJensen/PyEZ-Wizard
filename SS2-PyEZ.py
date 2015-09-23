########################################################################
#layout=   http://pythonprogramming.net/change-show-new-frame-tkinter/ #
########################################################################

import Tkinter as tk

from net.PyEZ_Connect import JunOS_Connection

LARGE_FONT= ("Verdana", 12)

#########################
#   Main TKinter  Class #
#########################
class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        ####################################
        #Connect To Junos Connection Class #
        ####################################
        # self.main_connection=JunOS_Connection
        # self.connect=self.main_connection()

        #cu=Config(self.main_connection)
        #cu.rescue(self,action="load")

        #####################################
        #           Launch GUI              #
        #####################################
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #pages=()

        for F in (StartPage, HostConf, MangConf, SysServ, Vlans,VRs, Interfaces, Protocols):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

#########################
#   Class Start Page    #
#########################
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome to Quick JunOS Configuration App", font=LARGE_FONT)
        label.grid(row=0, column=0)

        #################################
        #   Button To go to Next Page   #
        #   Calls HostConf Class        #
        #################################
        button = tk.Button(self, text="Start Configurations",
                            command=lambda: controller.show_frame(HostConf))
        button.grid(row=1, column=0)

#########################
#   Host Configuration  #
#########################
class HostConf(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="HOST CONFIGURATIONS", font=LARGE_FONT)
        hostlabel = tk.Label(self,text='Enter a hostname for your system') # Text in GUI
        ###########Entry Field#############
        self.hostentry = tk.Entry(self,width=10) # Insert field
        ###########Button to Commit Host Name############
        hostbutton = tk.Button(self,text='Commit', command=self.hostcommit)
        hostlabel.grid(row=1,column=0)
        self.hostentry.grid(row=1,column=1)
        hostbutton.grid(row=1,column=2)
        label.grid(row=0, column=0)

        ##############################
        # Button to Go to Next Page  #
        # Calls MangConf Class       #
        ##############################
        button1 = tk.Button(self, text="Next: MANAGEMENT INTERFACE",
                            command=lambda: controller.show_frame(MangConf))
        button1.grid(row=2, column=0)

    #########################
    #  Host Commit Method   #
    #########################
    def hostcommit(self):
        JunOS_Connection().hostcommit(self.hostentry.get())

#############################################
#   Mangagement Interface Configurations    #
#############################################
class MangConf(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="MANAGEMENT INTERFACE", font=LARGE_FONT)
        label.grid(row=0, column=0)

        button1 = tk.Button(self, text="Next: SYSTEM SERVICES",
                            command=lambda: controller.show_frame(SysServ))
        button1.grid(row=1, column=0)

#####################################
#   System Services Configurations  #
#####################################
class SysServ(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SYSTEM SERVICES", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=6, sticky="W")

        self.controller=controller

        #############
        #   SSH     #
        #############
        self.ssh_Var=tk.IntVar()
        self.ssh_Var.set(0)
        ssh_Button=tk.Checkbutton(self, text="SSH",variable=self.ssh_Var)
        ssh_Button.grid(row=1,column=0, stick="W")

        #############
        #   TELNET  #
        #############
        self.telnet_Var=tk.IntVar()
        self.telnet_Var.set(0)
        telnet_Button=tk.Checkbutton(self, text="Telnet",variable=self.telnet_Var)
        telnet_Button.grid(row=2,column=0, sticky="W")

        #############
        #   FTP     #
        #############
        self.ftp_Var=tk.IntVar()
        self.ftp_Var.set(0)
        ftp_Button=tk.Checkbutton(self, text="FTP",variable=self.ftp_Var)
        ftp_Button.grid(row=3,column=0, sticky="W")

        #############
        #   NTP     #
        #############
        self.ntp_Var=tk.IntVar()
        self.ntp_Var.set(0)
        ntp_Button=tk.Checkbutton(self, text="NTP",variable=self.ntp_Var, command=self.ntp)
        ntp_Button.grid(row=4,column=0, sticky="W")

        #############
        #   DHCP    #
        #############
        self.dhcp_Var=tk.IntVar()
        self.dhcp_Var.set(0)
        self.dhcp_row=0
        self.r=0
        dhcp_Button=tk.Checkbutton(self, text="DHCP",variable=self.dhcp_Var, command=self.dhcp)
        dhcp_Button.grid(row=6,column=0,sticky="W")

        #####################
        #   COMMIT  All     #
        #   GO TO NEXT PAGE #
        #####################
        button1 = tk.Button(self, text="Next: VLANS", command=self.commit_SysServ)
        button1.grid(row=100, column=0)

    #################
    #   SSH COMMAND #
    #################
    def ssh(self):
        JunOS_Connection().ssh()

    #####################
    #   TELNET COMMAND  #
    #####################
    def telnet(self):
        JunOS_Connection().telnet()

    #################
    #   FTP COMMAND #
    #################
    def ftp(self):
        JunOS_Connection().ftp()

    #########################
    #   NTP SERVER INFO     #
    #########################
    def ntp(self,*args):
        self.boot_Srv_List=[]
        self.ntp_Srv_List=[]

        boot_Srv=tk.Label(self, text="Boot Server")
        boot_Srv.grid(row=4, column=1)

        ntp_Srv=tk.Label(self, text="Ntp Server")
        ntp_Srv.grid(row=5, column=1)

        for x in range(4):
                ###########Boot Server##############
                boot_Srv_Add=tk.Entry(self,width=3)
                boot_Srv_Add.grid(row=4, column=2+x)
                self.boot_Srv_List.append(boot_Srv_Add)
                ###########NTP Server###############
                ntp_Srv_Add=tk.Entry(self,width=3)
                ntp_Srv_Add.grid(row=5, column=2+x)
                self.ntp_Srv_List.append(ntp_Srv_Add)

    ##################
    #   NTP COMMAND  #
    ##################
    def ntp_Command(self,*args):
        JunOS_Connection().ntp(self.boot_Srv_List, self.ntp_Srv_List)

    ###########################
    #   DHCP # OF Servers     #
    #   NO COMMIT             #
    ###########################
    def dhcp(self,*args):
        srv_Nbr=str(self.r+1)
        #################################################
        #   FIXED LABELS: Pool, /, Router, Low, High    #
        #################################################
        server_Label=tk.Label(self,text="DHCP"+srv_Nbr)
        server_Label.grid(row=(6+4*self.r), column=1)

        pool_Label=tk.Label(self,text="Pool")
        pool_Label.grid(row=(6+4*self.r), column=2)

        pool_Filler=tk.Label(self,text="/")
        pool_Filler.grid(row=6+4*self.r, column=6)

        router_label=tk.Label(self, text="Router")
        router_label.grid(row=7+4*self.r, column=2)

        low_Label= tk.Label(self,text="Low")
        low_Label.grid(row=(8+4*self.r), column=2)

        high_Label= tk.Label(self,text="High")
        high_Label.grid(row=(9+4*self.r), column=2)

        self.router_List=[]
        self.add_Range_List=[]

        ##################
        #   Entry Fields #
        ##################
        for x in range(4):
            ###########POOL####################
            pool_Add=tk.Entry(self,width=3)
            pool_Add.grid(row=6+4*self.r, column=3+x)
            self.router_List.append(pool_Add)
            self.add_Range_List.append(pool_Add)

        pool_CDR=tk.Entry(self,width=2)
        pool_CDR.grid(row=6+4*self.r, column=7)
        self.router_List.append(pool_CDR)
        self.add_Range_List.append(pool_CDR)

            ###########DHCP ROUTER##############
        for x in range(4):
            router_Address1=tk.Entry(self,width=3)
            router_Address1.grid(row=(7+4*self.r), column=3+x)
            self.router_List.append(router_Address1)

            ###########LOW ADDRESS##############
        for x in range(4):
            low_Address1=tk.Entry(self,width=3)
            low_Address1.grid(row=(8+4*self.r), column=3+x)
            self.add_Range_List.append(low_Address1)

            ###########HIGHT ADDRESSS###########
        for x in range(4):
            high_Address1=tk.Entry(self,width=3)
            high_Address1.grid(row=(9+4*self.r), column=3+x)
            self.add_Range_List.append(high_Address1)

        new_Srv_But=tk.Button(self,text="New Server", command=self.dhcp_combi)
        new_Srv_But.grid(row=(9+4*self.r), column=9)


    ###############################################
    #   CREATE DHCP SERVERS & COMMIT PREVIOUS ONE #
    ###############################################
    def dhcp_combi(self, *args):
        self.r+=1
        check=self.router_List[0].get()
        if len(check)!=0:
            self.dhcp_Command(self.router_List, self.add_Range_List)
            self.dhcp()

    ###########################
    #   DHCP FINAL COMMAND    #
    ###########################
    def dhcp_Command(self,*args):
        JunOS_Connection().dhcp(self.router_List, self.add_Range_List)

    #########################
    #   ALL COMMIT COMMAND  #
    #########################
    def commit_SysServ(self,**kwargs):
        controller=self.controller

        ######Commit SSH
        ssh_Value=self.ssh_Var.get()
        if ssh_Value==1:
            self.ssh()

        ######Commmit TELNET
        telnet_Value=self.telnet_Var.get()
        if telnet_Value==1:
            self.telnet()

        ######Commit FTP
        ftp_Value=self.ftp_Var.get()
        if ftp_Value==1:
            self.ftp()

        ######Commit NTP
        ntp_Value=self.ntp_Var.get()
        if ntp_Value==1:
            self.ntp_Command()

        ######Commit DHCP
        dhcp_Value=self.dhcp_Var.get()
        if dhcp_Value==1:
            self.dhcp_Command()
        #lambda: controller.show_frame(Vlans)
        controller.show_frame(Vlans)

####################
#       VLANS      #
####################
class Vlans(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="VLANS", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=4)
        self.controller=controller

        self.vlan_Row=0 #####Variable to use dynamic rows with grid
        self.vlan()     #####Load TkInter and Etnry Fields

        button1 = tk.Button(self, text="Next: VIRTUAL ROUTERS", command=self.commit)
        button1.grid(row=100, column=0, columnspan=4, sticky="W")
    #######################
    #   GET VLAN FIELDS   #
    #######################
    def vlan(self,*args):
        self.vlan_List=[]
        self.vlan_Int_List=[]
        ###########Vlan NAME and ENTRY
        vlan_Name=tk.Label(self, text="Name")
        vlan_Name.grid(row=1+(self.vlan_Row*2), column=1)

        vlan_Name_Entry=tk.Entry(self, width="8")
        vlan_Name_Entry.grid(row=1+(self.vlan_Row*2), column=2, sticky="W",pady=5)
        self.vlan_List.append(vlan_Name_Entry)
        self.vlan_Int_List.append(vlan_Name_Entry)
        ##########VLAN ID and ENTRY
        vlan_ID=tk.Label(self, text="VLAN ID")
        vlan_ID.grid(row=1+(self.vlan_Row*2), column=3)

        vlan_ID_Entry=tk.Entry(self, width=5)
        vlan_ID_Entry.grid(row=1+(self.vlan_Row*2), column=4)
        self.vlan_List.append(vlan_ID_Entry)
        ##########INTERFACE and ENTRY
        vlan_int=tk.Label(self,text="Interface")
        vlan_int.grid(row=1+(self.vlan_Row*2), column=5)

        vlan_int_Entry=tk.Entry(self, width=10)
        vlan_int_Entry.grid(row=1+(self.vlan_Row*2), column=6)
        self.vlan_Int_List.append(vlan_int_Entry)


        vlan_Button=tk.Button(self,text="Add New Interface", command=self.combi)
        vlan_Button.grid(row=1+(self.vlan_Row*2), column=7, columnspan=3)

    #######################
    #   VLAN COMMANDLINE  #
    #######################
    def vlan_Command(self,add_Vlan,add_Interface):
        JunOS_Connection().vlan_Command(self.vlan_List, self.vlan_Int_List)

    #########################
    # IMPORT VLAN COMMANDS  #
    #########################
    def combi(self,*args):
        self.vlan_Row+=1
        check=self.vlan_List[0].get()
        if len(check)!=0:
            self.vlan_Command(self.vlan_List, self.vlan_Int_List)
            self.vlan()

    #####################################
    #   COMMIT VLAN AND GO TO NEXT PAGE #
    #####################################
    def commit(self,**kwargs):
        controller=self.controller
        self.vlan_Command(self.vlan_List, self.vlan_Int_List)
        controller.show_frame(VRs)

#########################
#   VIRTUAL ROUTERS     #
#########################
class VRs(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="VIRTUAL ROUTERS", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=3)
        ##### Labels and Entry fields #####
        VREntlab = tk.Label(self,text="Enter a VR Name:")
        VREntlab.grid(row=1, column=0)
        self.VREntry = tk.Entry(self,width=10 )
        self.VREntry.grid(row=1, column=1)
        IntLab = tk.Label(self, text="Interface:")
        IntLab.grid(row=2, column=0)
        self.IntEntry = tk.Entry(self,width=10)
        self.IntEntry.grid(row=2,column=1)
        UnitLab = tk.Label(self,text="Unit:")
        UnitLab.grid(row=2, column=3)
        self.UnitEnt = tk.Entry(self,width=3)
        self.UnitEnt.grid(row=2,column=4)
        ### Commit Button ###
        ComButton = tk.Button(self, text="commit",command=self.vrcommit)
        ComButton.grid(row=3, column=0)
        button1 = tk.Button(self, text="Next: Interfaces",
                            command=lambda: controller.show_frame(Interfaces))
        button1.grid(row=4, column=0)

    #########################
    # VIRTUAL ROUTER COMMIT #
    #########################

    def vrcommit(self):
        JunOS_Connection().vr(self.VREntry.get(), self.IntEntry.get(), self.UnitEnt.get())

#########################
#       INTERFACES      #
#########################
class Interfaces(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        ## Labels and Entries ##

        introlab = tk.Label(self,text="Select which interface and unit to work on")
        introlab.grid(row=1,column=0, columnspan=4)
        ## Interface ##
        interlab= tk.Label(self,text="Interface")
        interlab.grid(row=2,column=0)
        self.interent = tk.Entry(self,width=5)
        self.interent.grid(row=2,column=1,sticky='W')
        ## Unit ##
        unitlab = tk.Label(self,text="Unit")
        unitlab.grid(row=3,column=0)
        self.unitent= tk.Entry(self,width=5)
        self.unitent.grid(row=3, column=1, sticky="W")
        ## Ipv4 ##
        v4label = tk.Label(self, text ="Add IPv4 Address" ) ## label
        v4label.grid(row=4,column=0)
        self.v4ent = tk.Entry(self, width=30) ## Entry
        self.v4ent.grid(row=4,column=1)

        ## Ipv4 Mask ##
        v4masklab = tk.Label(self, text="/")
        v4masklab.grid(row=4, column=2)
        self.v4maskent = tk.Entry(self, width=3)
        self.v4maskent.grid(row=4,column=4)

        ## Ipv4 button ##
        v4but = tk.Button(self, text="Commit",command=self.v4commit)
        v4but.grid(row=4,column=5)

        ## Ipv6 ##
        v6label = tk.Label(self, text="Add IPv6 Address") ## Label
        v6label.grid(row=5, column=0)
        self.v6ent = tk.Entry(self,width=30) ## Entry
        self.v6ent.grid(row=5, column=1)

        ## Ipv6 Mask##
        v6masklab = tk.Label(self, text="/")
        v6masklab.grid(row=5, column=2)
        self.v6maskent = tk.\
        Entry(self, width=3)
        self.v6maskent.grid(row=5,column=4)

        ## Ipv6 Button ##
        v6but = tk.Button(self, text="Commit",command=self.v6commit)
        v6but.grid(row=5,column=5)
        label = tk.Label(self, text="INTERFACES", font=LARGE_FONT)
        label.grid(row=0, column=0)

        button1 = tk.Button(self, text="Next: Protocols",
                            command=lambda: controller.show_frame(Protocols))
        button1.grid(row=6, column=0)


    #########################
    #      IPv4 Commit      #
    #########################

    def v4commit(self):
        JunOS_Connection().ipV4(self.v4ent.get(),self.interent.get(), self.unitent.get(),self.v4maskent.get())

    #########################
    #      IPv6 Commit      #
    #########################

    def v6commit(self, *args):
        JunOS_Connection().ipV6(self.v6ent.get(),self.interent.get(), self.unitent.get(),self.v6maskent.get())



#########################
#       PROTOCOLS       #
#########################
class Protocols(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="PROTOCOLS", font=LARGE_FONT)
        label.grid(row=0, column=0)

        button1 = tk.Button(self, text="COMMIT",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=0)

#####################
#   START PROGRAM   #
#####################
app = MainWindow()
app.mainloop()
import Tkinter as tk
import ScrolledText as tkst

from net.PyEZ_Connect import JunOS_Connection

LARGE_FONT= ("Verdana", 12)

#########################
#   Main TKinter  Class #
#########################
class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        #####################################
        #           Launch GUI              #
        #####################################
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        #pages=()

        for F in (StartPage, HostConf, MangConf, SysServ, Vlans,VRs, Interfaces,
                  Protocols,Classes, Users, Firewalls,SaveConf):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        self.logBox()

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    #####################
    #   CREATE LOG BOX  #
    #####################
    def logBox(self):
        #####Log Box
        self.logbox=tkst.ScrolledText(self.container, width=50, height=30 )
        self.logbox.grid(row=0, column=1)

        #####Update Button
        log_update=tk.Button(self.container, text="Update Log", command=self.update_log)
        log_update.grid(row=1, column=1)

    #####################
    #   UPDATE LOG BOX  #
    #####################
    def update_log(self):
        #####Clear Box
        self.logbox.delete(0.1,"end")
        #####Get Config
        update=str(JunOS_Connection().show())
        #####Insert Config
        self.logbox.insert("insert",update)

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

        boot_Srv=tk.Label(self, text="Boot Server")
        boot_Srv.grid(row=4, column=1)

        ntp_Srv=tk.Label(self, text="Ntp Server")
        ntp_Srv.grid(row=5, column=1)

        ###########Boot Server##############
        self.boot_Ent=tk.Entry(self,width=15)
        self.boot_Ent.grid(row=4, column=2)

        ###########NTP Server###############
        self.ntp_Ent=tk.Entry(self,width=15)
        self.ntp_Ent.grid(row=5, column=2)

    ##################
    #   NTP COMMAND  #
    ##################
    def ntp_Command(self,*args):
        JunOS_Connection().ntp(self.boot_Ent.get(), self.ntp_Ent.get())

    ###########################
    #   DHCP SERVER INFO      #
    ###########################
    def dhcp(self,*args):
        ##############POOL###############
        server_Label=tk.Label(self,text="DHCP") ### DHCP Label
        server_Label.grid(row=(6), column=1)

        pool_Label=tk.Label(self,text="Pool")   ###Label
        pool_Label.grid(row=(6), column=2)

        self.pool_Ent=tk.Entry(self,width=15)   ###Entry
        self.pool_Ent.grid(row=6, column=3)

        pool_Filler=tk.Label(self,text="/")
        pool_Filler.grid(row=6, column=4)

        self.CDR=tk.Entry(self,width=2)     ###CDR Entry
        self.CDR.grid(row=6, column=5)

        #############ROUTER###############
        router_label=tk.Label(self, text="Router")  ###Label
        router_label.grid(row=7, column=2)

        self.router_Ent=tk.Entry(self, width="15")       ###Entry
        self.router_Ent.grid(row=7, column=3)

        ##############LOW################
        low_Label= tk.Label(self,text="Low")        ###Label
        low_Label.grid(row=8, column=2)

        self.low_Ent=tk.Entry(self, width="15")          ###Entry
        self.low_Ent.grid(row=8, column=3)

        ##############HIGH##############
        high_Label= tk.Label(self,text="High")      ###Label
        high_Label.grid(row=(9), column=2)

        self.high_Ent=tk.Entry(self, width="15")         ###Entry
        self.high_Ent.grid(row=9, column=3)

        ############DHCP COMMIT BUTTON##################
        dhcp_Commit_But=tk.Button(self,text="Commit", command= self.dhcp_Command)
        dhcp_Commit_But.grid(row=9, column=5)

    ###########################
    #   DHCP FINAL COMMAND    #
    ###########################
    def dhcp_Command(self,*args):
        JunOS_Connection().dhcp(self.pool_Ent.get(),self.CDR.get(),self.router_Ent.get(),
                                self.low_Ent.get(), self.high_Ent.get())
        self.pool_Ent.delete(0,"end")
        self.CDR.delete(0,"end")
        self.router_Ent.delete(0,"end")
        self.low_Ent.delete(0,"end")
        self.high_Ent.delete(0,"end")

    ###########################
    ###########################
    ##   ALL SYSTEM COMMITS  ##
    ###########################
    ###########################
    def commit_SysServ(self,**kwargs):
        controller=self.controller

        ######Commit SSH########
        ssh_Value=self.ssh_Var.get()
        if ssh_Value==1:
            self.ssh()

        ######Commmit TELNET####
        telnet_Value=self.telnet_Var.get()
        if telnet_Value==1:
            self.telnet()

        ######Commit FTP########
        ftp_Value=self.ftp_Var.get()
        if ftp_Value==1:
            self.ftp()

        ######Commit NTP########
        ntp_Value=self.ntp_Var.get()
        if ntp_Value==1:
            self.ntp_Command()

        ######Commit DHCP#######
        dhcp_Value=self.dhcp_Var.get()
        if dhcp_Value==1:
            self.dhcp_Command()

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

        ###########Vlan NAME#############
        vlan_Name=tk.Label(self, text="Name")
        vlan_Name.grid(row=1, column=1)

        self.name_Entry=tk.Entry(self, width="8")
        self.name_Entry.grid(row=1, column=2, sticky="W",pady=5)

        ##########VLAN ID##################
        vlan_ID=tk.Label(self, text="VLAN ID")
        vlan_ID.grid(row=1, column=3)

        self.ID_Entry=tk.Entry(self, width=5)
        self.ID_Entry.grid(row=1, column=4)
        ##########INTERFACE and ENTRY
        interface=tk.Label(self,text="Interface")
        interface.grid(row=1, column=5)

        self.int_Entry=tk.Entry(self, width=10)
        self.int_Entry.grid(row=1, column=6)

        ##########CREATE DHCP
        vlan_Button=tk.Button(self,text="Add New Interface", command=self.vlan_Command)
        vlan_Button.grid(row=1, column=7, columnspan=3)

        ##########NAVIGATE TO NEXT PAGE
        button1 = tk.Button(self, text="Next: VIRTUAL ROUTERS", command=lambda:controller.show_frame(VRs))
        button1.grid(row=2, column=0, columnspan=4, sticky="W")


    #######################
    #   VLAN COMMANDLINE  #
    #######################
    def vlan_Command(self):
        JunOS_Connection().vlan_Command(self.name_Entry.get(),self.ID_Entry.get(),self.int_Entry.get())
        self.name_Entry.delete(0,"end")
        self.ID_Entry.delete(0,"end")
        self.int_Entry.delete(0,"end")

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
    def v4commit(self, *args):
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
        label.grid(row=0, column=0, columnspan=3)
        ### Router ID ### (for ospf)
        IDlab = tk.Label(self, text='Router ID')
        IDlab.grid(row=2, column = 0)

        #########################
        #       OSPF            #
        #########################
        self.IDent = tk.Entry(self, width=10)
        self.IDent.grid(row=2, column=1)
        ## OSPF label ##
        OSPFlab = tk.Label (self, text="OSPF")
        OSPFlab.grid(row=1, column=0)
        ## Area ##
        Arealab = tk.Label(self, text="Area")
        Arealab.grid(row=3, column=0)
        self.Areaent = tk.Entry(self, width=10)
        self.Areaent.grid(row=3, column=1)
        ## Interface ##
        Interlab = tk.Label(self, text="Interface")
        Interlab.grid(row=3, column=2)
        self.Interent = tk.Entry(self, width=10)
        self.Interent.grid(row=3, column=3)
        ## OSPF Button ##
        OSPFbut = tk.Button(self, text="Commit",command=self.OSPFcommit)
        OSPFbut.grid(row=3,column=5)
        OSPFbut.grid(row=3,column=6)
        ## Unit ##
        unitlab = tk.Label(self, text="Unit")
        unitlab.grid(row=3, column=4)
        self.unitent = tk.Entry(self, width=10)
        self.unitent.grid(row=3, column=5)

        #########################
        #       OSPFv3          #
        #########################
        ### Router ID ### (for ospf)
        ID3lab = tk.Label(self, text='Router ID')
        ID3lab.grid(row=5, column = 0)
        self.ID3ent = tk.Entry(self, width=10)
        self.ID3ent.grid(row=5, column=1)
        OSPF3lab = tk.Label (self, text="OSPF3")
        OSPF3lab.grid(row=4, column=0)
        ## Area ##
        Area3lab = tk.Label(self, text="Area")
        Area3lab.grid(row=6, column=0)
        self.Area3ent = tk.Entry(self, width=10)
        self.Area3ent.grid(row=6, column=1)
        ## Interface ##
        Inter3lab = tk.Label(self, text="Interface")
        Inter3lab.grid(row=6, column=2)
        self.Inter3ent = tk.Entry(self, width=10)
        self.Inter3ent.grid(row=6, column=3)
        ## Unit ##
        unit3lab = tk.Label(self, text="Unit")
        unit3lab.grid(row=6, column=4)
        self.unit3ent = tk.Entry(self, width=10)
        self.unit3ent.grid(row=6, column=5)
        ## OSPF Button ##
        OSPF3but = tk.Button(self, text="Commit",command=self.OSPF3commit)
        OSPF3but.grid(row=6,column=6)

        #########################
        #       ISIS            #
        #########################

        ISLab = tk.Label(self, text="IS-IS")
        ISLab.grid(row=7,column=0)
        Lo0Lab = tk.Label(self, text="Lo0 ISO Address")
        Lo0Lab.grid(row=8,column=0)
        self.Lo0ent = tk.Entry(self,width=30)
        self.Lo0ent.grid(row=8, column=1, columnspan=3)
        ISObut = tk.Button(self, text="Commit",command=self.ISOcommit)
        ISObut.grid(row=8,column=4)
        ## Interface ##
        isInterlab = tk.Label(self, text="Interface")
        isInterlab.grid(row=9, column=0)
        self.isInterent = tk.Entry(self, width=10)
        self.isInterent.grid(row=9, column=1)
        ## Unit ##
        isunitlab = tk.Label(self, text="Unit")
        isunitlab.grid(row=9, column=2)
        self.isunitent = tk.Entry(self, width=10)
        self.isunitent.grid(row=9, column=3)
        ## ISIS Button ##
        ISObut = tk.Button(self, text="Commit",command=self.ISIScommit)
        ISObut.grid(row=9,column=4)


        button1 = tk.Button(self, text="Next: CLASSES",
                            command=lambda: controller.show_frame(Classes))
        button1.grid(row=10, column=0)

    ##############################
    #OSPF, OSPF3 and ISIS Commit #
    ##############################

    def OSPFcommit(self, *args):
        JunOS_Connection().OSPF(self.IDent.get(),self.Areaent.get(), self.Interent.get(),self.unitent.get())

    def OSPF3commit(self, *args):
        JunOS_Connection().OSPF3(self.ID3ent.get(),self.Area3ent.get(), self.Inter3ent.get(),self.unit3ent.get())

    def ISIScommit(self,*args):
        JunOS_Connection().ISIS(self.isInterent.get(),self.isunitent.get())

    def ISOcommit(self, *args):
        JunOS_Connection().ISO(self.Lo0ent.get())

#########################
#       CLASSES         #
#########################
class Classes(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="CLASSES", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=3)

        ##########CLASS NAME###################
        name=tk.Label(self, text="Name")
        name.grid(row=1, column=0)

        self.name_Ent=tk.Entry(self, width="15")
        self.name_Ent.grid(row=1, column=1)

        ##########CLASS PREVILAGE###############
        action=tk.Label(self, text="Previlage")
        action.grid(row=1,column=2)

        self.action_Ent=tk.Entry(self, width="15")
        self.action_Ent.grid(row=1, column=3)

        ##########PREVILAGE DETAIL##############
        self.det_Ent=tk.Entry(self, width="15")
        self.det_Ent.grid(row=1, column=4)

        ##########CLASS COMMIT BUTTON############
        class_Button=tk.Button(self, text="New Class/Actions", command=self.classes)
        class_Button.grid(row=2, column=0)

        ##########NAVIGATE TO NEXT PAGE##########
        button1 = tk.Button(self, text="Next: USERS",
                                command=lambda: controller.show_frame(Users))
        button1.grid(row=10, column=0)

     ####################
     #   CLASS COMMAND  #
     ####################
     def classes(self):
        JunOS_Connection().classes(self.name_Ent.get(),self.action_Ent.get(),self.det_Ent.get())
        self.name_Ent.delete(0,"end")
        self.action_Ent.delete(0,"end")
        self.det_Ent.delete(0,"end")

#########################
#       USERS           #
#########################
class Users(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="USERS", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=3)

        ####User Name
        user=tk.Label(self, text="User")
        user.grid(row=1, column=0)

        self.user_Ent=tk.Entry(self, width="15")
        self.user_Ent.grid(row=1, column=1)

        #####Class Name
        cls=tk.Label(self, text="Class")
        cls.grid(row=1, column=2)

        self.cls_Ent=tk.Entry(self, width="15")
        self.cls_Ent.grid(row=1, column=3)

        #####Password
        pass1=tk.Label(self, text="Enter Password")
        pass1.grid(row=2, column=0)

        self.pass1_Ent=tk.Entry(self, width="15")
        self.pass1_Ent.grid(row=2, column=1)

        #####Re-Enter Pass
        pass2=tk.Label(self, text="Re-Enter Password")
        pass2.grid(row=3, column=0)

        self.pass2_Ent=tk.Entry(self, width="15")
        self.pass2_Ent.grid(row=3, column=1)

        ####NEW USER BUTTON
        new_Usr=tk.Button(self, text="New User", command=self.new_User)
        new_Usr.grid(row=5, column=0)

        button1 = tk.Button(self, text="Next: FIREWALL",
                            command=lambda: controller.show_frame(Firewalls))
        button1.grid(row=10, column=0)

     def new_User(self):
         if self.pass1_Ent.get()== self.pass2_Ent.get():
             JunOS_Connection().users(self.user_Ent.get(),self.cls_Ent.get(),self.pass1_Ent.get())
         else:
             err_mss=tk.Label(self, text="Passwords DO NOT match")
             err_mss.grid(row=4, column=0, columnspan=4)

             self.user_Ent.delete(0,'end')
             self.cls_Entry.delete(0,'end')
             self.pass1.delete(0,'end')
             self.pass2.delete(0,'end')

#########################
#       FIREWALL        #
#########################
class Firewalls(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="FIREWALLS", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=3, sticky="W")

        self.controller=controller

        #####Filter Info
        filter=tk.Label(self, text="Filter")    #Label
        filter.grid(row=1, column=0, sticky="W")

        self.filter_ent=tk.Entry(self,width="15")#Entry
        self.filter_ent.grid(row=1, column=1)

        #####Term Info
        self.terms()

        #####BUttons to CLear Field and Get new Info
        new_term_button=tk.Button(self,text="New Term",command=self.new_Term)
        new_term_button.grid(row=99, column=0, sticky="SW")

        new_filter_button=tk.Button(self,text="New Filter", command=self.new_Filter)
        new_filter_button.grid(row=99, column=1, sticky="SW")

        #####Commit and Go to Next Page
        button1 = tk.Button(self, text="Next: SAVE CONFIGURATION", command=self.fw_Commit )
        button1.grid(row=100, column=0, sticky="SW", columnspan=3)

    #############
    #   TERMS   #
    #############
    def terms(self):
        term=tk.Label(self, text="Term")
        term.grid(row=2,column=0, sticky="W")

        self.term_Ent=tk.Entry(self,width=15)
        self.term_Ent.grid(row=2,column=1)
        ######Get From-Then Fields
        self.from_then()

    #################
    #   FROM/THEN   #
    #################
    def from_then(self):
        #####FROM
        from_lbl=tk.Label(self, text="From") ###Label
        from_lbl.grid(row=2,column=2)

        self.from_Ent=tk.Entry(self, width="20") ###Entry 1
        self.from_Ent.grid(row=2,column=3)

        self.from_Ent2=tk.Entry(self, width="20") ###Entry 2
        self.from_Ent2.grid(row=2,column=4)

        then_lbl=tk.Label(self, text="Then")    ###Label
        then_lbl.grid(row=3,column=2)

        self.then_Ent=tk.Entry(self, width="20") ###Entry
        self.then_Ent.grid(row=3,column=3)

        ######Commit Firewall and Clear Field
        new_from=tk.Button(self, text="Add From/Then", command=self.new_From)
        new_from.grid(row=3,column=4)

    #########################
    #   NEW FROM / THEN     #
    #########################
    def new_From(self):
        #####Commit
        JunOS_Connection().firewall(self.filter_ent.get(),self.term_Ent.get(),self.from_Ent.get()
                                    ,self.from_Ent2.get(),self.then_Ent.get())
        ######Empty From/Then Fields
        self.from_Ent.delete(0, 'end')
        self.from_Ent2.delete(0, 'end')
        self.then_Ent.delete(0, 'end')

    #################
    #   NEW TERM    #
    #################
    def new_Term(self):
        ######Commit
        JunOS_Connection().firewall(self.filter_ent.get(),self.term_Ent.get(),self.from_Ent.get()
                                    ,self.from_Ent2.get(),self.then_Ent.get())
        #####CLEAR FIELDS UP TO TERM
        self.new_From()
        self.name_Ent.delete(0, 'end')

    #################
    #   NEW FILTER  #
    #################
    def new_Filter(self):
        #####Commit
        JunOS_Connection().firewall(self,self.filter_ent.get(),self.term_Ent.get(),self.from_Ent.get()
                                    ,self.from_Ent2.get(),self.then_Ent.get())
        ######Empty All Fields
        self.new_Term()
        self.filter_ent.delete(0,"end")


    def fw_Commit(self, **kwargs):
        controller=self.controller
        if len(self.filter_ent.get())!=0:
            JunOS_Connection().firewall(self,self.filter_ent.get(),self.term_Ent.get(),self.from_Ent.get()
                                        ,self.from_Ent2.get(),self.then_Ent.get())
        controller.show_frame(SaveConf)

#########################
#   SAVE CONFIGURATION  #
#########################
class SaveConf(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SAVE CONFIGURATION", font=LARGE_FONT)
        label.grid(row=0, column=0)

        ##### FILE NAME
        file_Name=tk.Label(self, text="File Name")  ###Label
        file_Name.grid(row=1, column=0)

        self.name_Ent=tk.Entry(self, width="15")    ###Entry
        self.name_Ent.grid(row=1,column=1)

        #####FILE TYPE
        file_Type=tk.Label(self, text="Type")       ###Label
        file_Type.grid(row=1, column=2)

        self.type_Ent=tk.Entry(self,width="10")     ###Entry
        self.type_Ent.grid(row=1, column=3)

        #####Button to Save File to System
        save_button=tk.Button(self, text="Save Config", command=self.save_Conf)
        save_button.grid(row=2, column=0)

        #####Navigation Button
        button1 = tk.Button(self, text="Next: START PAGE",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=3, column=0)

    #########################
    #   SAVE FILE TO CONFIG #
    #########################
    def save_Conf(self):
        #####Create File name
        file_name=self.name_Ent.get()+"."+self.type_Ent.get() #####Combine Name + File Type

        #####Get Config from JunOS as STR
        config=str(JunOS_Connection().show())

        #####Create File
        with open(file_name, "w") as text_file:
                text_file.write(config) ####Write to File
                text_file.close()

app = MainWindow()
app.mainloop()
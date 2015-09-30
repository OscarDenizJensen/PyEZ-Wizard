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

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #pages=()

        for F in (StartPage, HostConf, MangConf, SysServ, Vlans,VRs, Interfaces,Protocols,Classes, Users, Firewalls):

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
        log_Info=str(JunOS_Connection().show())
        log_box=tkst.ScrolledText(self, width=50, height=40)
        log_box.grid(row=1, column=10, rowspan=40, columnspan=20)
        log_box.insert("insert",log_Info)

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

        log_Info=str(JunOS_Connection().show())
        log_box=tkst.ScrolledText(self, width=50, height=40)
        log_box.grid(row=1, column=10, rowspan=10, columnspan=10)
        log_box.insert("insert",log_Info)


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
        log_Info=str(JunOS_Connection().show())
        log_box=tkst.ScrolledText(self, width=50, height=40)
        log_box.grid(row=1, column=10, rowspan=10, columnspan=10)
        log_box.insert("insert",log_Info)
#########################
#       INTERFACES      #
#########################
class Interfaces(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        log_Info=str(JunOS_Connection().show())
        log_box=tkst.ScrolledText(self, width=50, height=40)
        log_box.grid(row=1, column=10, rowspan=40, columnspan=20)
        log_box.insert("insert",log_Info)

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
        log_Info=str(JunOS_Connection().show())
        log_box=tkst.ScrolledText(self, width=50, height=40)
        log_box.grid(row=1, column=10, rowspan=40, columnspan=20)
        log_box.insert("insert",log_Info)
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

        #####CLASS NAME
        name=tk.Label(self, text="Name")
        name.grid(row=1, column=0)

        self.name_Ent=tk.Entry(self, width="15")
        self.name_Ent.grid(row=1, column=1)

        ######CLASS ACTION
        action=tk.Label(self, text="Action")
        action.grid(row=1,column=2)

        self.action_Ent=tk.Entry(self, width="15")
        self.action_Ent.grid(row=1, column=3)

        #######ACTION DETAIL
        self.det_Ent=tk.Entry(self, width="15")
        self.det_Ent.grid(row=1, column=4)

        #######NEW CLASS BUTTON
        class_Button=tk.Button(self, text="New Class/Actions", command=self.classes)
        class_Button.grid(row=2, column=0)

        #######NEXT PAGE BUTTON
        button1 = tk.Button(self, text="Next: USERS",
                                command=lambda: controller.show_frame(Users))
        button1.grid(row=10, column=0)
     #################
     #   NEW CLASS   #
     #################

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
        button1 = tk.Button(self, text="Next: ROUTING PROTOCOLS", command=self.fw_Commit )
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
        controller.show_frame(StartPage)

#####################
#   START PROGRAM   #
#####################
app = MainWindow()
app.mainloop()
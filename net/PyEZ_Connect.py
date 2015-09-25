from jnpr.junos import Device
from jnpr.junos.utils.config import Config

#hostname= "Ozzy"

class JunOS_Connection():
    def __init__(self):
        self.dev_Connect = Device(host='192.168.56.2', user='root', password='Juniper1')
        #192.168.56.2
        self.dev_Connect.open()
        #pprint( dev.facts )

        print"Connection Established"

        self._conf_JunOS=Config(self.dev_Connect)

    def hostcommit(self,hostname):
        set_hostname='set system host-name %s' % hostname
        self._conf_JunOS.load(set_hostname, format='set')
        self._conf_JunOS.commit()
        print "Hostname Changed"

    def ssh(self):
        set_Ssh=("set system services ssh")
        self._conf_JunOS.load(set_Ssh, format='set')

        self._conf_JunOS.commit()
        print "SSH Enabled"

    def telnet(self):
        set_Telnet=("set system services telnet")
        self._conf_JunOS.load(set_Telnet, format='set')

        self._conf_JunOS.commit()
        print "TELNET Enabled"

    def ftp(self):
        set_Ftp=("set system services ftp")
        self._conf_JunOS.load(set_Ftp, format='set')

        self._conf_JunOS.commit()
        print"FTP Enabled"

    def ntp(self,boot,ntp):
        ###########Boot Server Command###########
        boot_Srv_List=[]
        for x in boot:
            boot_Srv_List.append(x.get())
        if len(boot_Srv_List[0])!=0:
            boot="set system ntp boot-server %s.%s.%s.%s" % tuple(boot_Srv_List)
            self._conf_JunOS.load(boot, format='set')
            ###########NTP Server Command###########
            ntp_Srv_List=[]
            for x in ntp:
                ntp_Srv_List.append(x.get())
            ntp="set system ntp server %s.%s.%s.%s" % tuple(ntp_Srv_List)
            self._conf_JunOS.load(ntp, format='set')

            self._conf_JunOS.commit()

    def dhcp(self,router,add_range):
        router_List=[]
        for x in router:
            router_List.append(x.get())

        self.dhcp_router=("set system services dhcp pool %s.%s.%s.%s/%s router %s.%s.%s.%s") % tuple(router_List)
        self._conf_JunOS.load(self.dhcp_router, format='set')

        address_Range_List=[]
        for x in add_range:
            address_Range_List.append(x.get())
        self.dhcp_add_Range=("set system services dhcp pool %s.%s.%s.%s/%s address-range low %s.%s.%s.%s "
                             "high %s.%s.%s.%s") % tuple(address_Range_List)
        self._conf_JunOS.load(self.dhcp_add_Range, format='set')

        self._conf_JunOS.commit()
        print "DHCP SERVER CREATED"

    def vlan_Command(self,add_Vlan,add_Interface):
        set_Vlan=[]
        for x in add_Vlan:
            set_Vlan.append(x.get())
        print "set vlans %s vlan-id %s" % tuple(set_Vlan)

        set_Interface=[]
        for x in add_Interface:
            set_Interface.append(x.get())
        print "set vlans %s interface %s" % tuple(set_Interface)

    def vr(self,vr_var,int_var,unit_var):
        ## Create first VR command ##
        self.set_VR='set routing-instances %s instance-type virtual-router' % vr_var
        ## Combine int and unit to get correct syntax ##
        self.int_var = int_var + "." + unit_var
        ## Make a list for next command ##
        vr_list = [vr_var, self.int_var]
        ## Create second VR command ##
        self.set_int="set routing-instances %s interface %s" % tuple(vr_list)
        ## Execute commands and commit ##
        self._conf_JunOS.load(self.set_VR, format='set')
        self._conf_JunOS.load(self.set_int, format='set')
        self._conf_JunOS.commit()

    def ipV4(self,v4, interface, unit, mask):
        ip = v4 + "/" + mask
        ip_list = (interface, unit, ip)

        self.set_ip="set interfaces %s unit %s family inet address %s" % tuple(ip_list)
        #T.insert(END, '\n' + self.set_ip)##logbox
        self._conf_JunOS.load(self.set_ip, format='set')
        self._conf_JunOS.commit()

    def ipV6(self,v6, interface, unit, mask):
        ip = v6 + "/" + mask
        ip_list = (interface, unit, ip)

        self.set_ip="set interfaces %s unit %s family inet address %s" % tuple(ip_list)
        #T.insert(END, '\n' + self.set_ip)##logbox
        self._conf_JunOS.load(self.set_ip, format='set')
        self._conf_JunOS.commit()

    def firewall(self,filter, term, from1, from2, then):
        if len(from1)!=0:
            from_List=[filter,term,from1,from2]
            self.fw_From="set firewall filter %s term %s from %s %s" % tuple(from_List)
            self._conf_JunOS.load(self.fw_From, format="set")

        if len(then)!=0:
            then_List=[filter,term,then]
            self.fw_Then="set firewall filter %s term %s then %s" % tuple(then_List)
            self._conf_JunOS.load(self.fw_Then, format="set")

        self._conf_JunOS.commit()
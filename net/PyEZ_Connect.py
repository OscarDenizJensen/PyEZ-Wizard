from jnpr.junos import Device
from jnpr.junos.utils.config import Config

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
        if len(boot[0])!=0:
            boot="set system ntp boot-server %s" % boot
            self._conf_JunOS.load(boot, format='set')
            ###########NTP Server Command###########
            ntp="set system ntp server %s" % ntp
            self._conf_JunOS.load(ntp, format='set')

            self._conf_JunOS.commit()

    def dhcp(self,pool, cdr, router,low, high):
        router_List=[pool, cdr, router]

        self.dhcp_router=("set system services dhcp pool %s/%s router %s") % tuple(router_List)
        self._conf_JunOS.load(self.dhcp_router, format='set')

        address_Range_List=[pool, cdr, low, high]
        self.dhcp_add_Range=("set system services dhcp pool %s/%s address-range low %s "
                             "high %s") % tuple(address_Range_List)
        self._conf_JunOS.load(self.dhcp_add_Range, format='set')

        self._conf_JunOS.commit()
        print "DHCP SERVER CREATED"

    def vlan_Command(self,name, id , interface):
        set_vlan=[name,id]
        if len(interface)==0:
            if len(id)==0:
                print("Err")
            else:
                print "set vlans %s vlan-id %s" % tuple(set_vlan)
        else:
            set_Interface=[name,id,interface]
            print "set vlans %s vlan-id %s interface %s" % tuple(set_Interface)

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

        self.set_ip="set interfaces %s unit %s family inet6 address %s" % tuple(ip_list)
        #T.insert(END, '\n' + self.set_ip)##logbox
        self._conf_JunOS.load(self.set_ip, format='set')
        self._conf_JunOS.commit()

    def OSPF(self, routerid, area, interface, unit):
        self.set_id="set routing-options router-id %s" % routerid
        ospflist = (area, interface, unit)
        self.set_ospf="set protocols ospf area %s interface %s.%s" % tuple(ospflist)
        self._conf_JunOS.load(self.set_id, format='set')
        self._conf_JunOS.load(self.set_ospf, format='set')
        self._conf_JunOS.commit()

    def ISIS(self,interface, unit):
        islist=(interface, unit)
        self.set_family="set interfaces %s unit %s family iso" % tuple(islist)
        self.set_protocol="set protocols isis interface %s.%s" % tuple(islist)
        self._conf_JunOS.load(self.set_family, format='set')
        self._conf_JunOS.load(self.set_protocol, format='set')
        self._conf_JunOS.commit()

    def ISO(self, iso):
        self.set_security="set security forwarding-options family iso mode packet-based"
        self.set_lo0="set interfaces lo0 unit 0 family iso address %s" % iso
        self.set_lo_int="set protocols isis interface lo0.0"
        # self._conf_JunOS.load(self.set_security, format='set')
        self._conf_JunOS.load(self.set_lo0, format='set')
        self._conf_JunOS.load(self.set_lo_int, format='set')
        self._conf_JunOS.commit()

    def OSPF3(self, routerid, area, interface, unit):
        self.set_id="set routing-options router-id %s" % routerid
        ospflist = (area, interface, unit)
        self.set_lo0="set protocols ospf3 area 0 interface lo0.0 passive"
        self.set_ospf3="set protocols ospf3 area %s interface %s.%s" % tuple(ospflist)
        self._conf_JunOS.load(self.set_id, format='set')
        self._conf_JunOS.load(self.set_lo0, format='set')
        self._conf_JunOS.load(self.set_ospf3, format='set')
        self._conf_JunOS.commit()

    def classes(self, name, action, detail):
        if len(name)!=0:
            class_info=[name,action,detail]
            self.class_set="set system login class %s %s %s" % tuple(class_info)
            self._conf_JunOS.load(self.class_set, format="set")

        self._conf_JunOS.commit()

    def users(self, user, class_Name, pass1):
        user_info=[user,class_Name,pass1]
        self.user_set="set system login user %s class % " \
                      "authentication plain-text-password-value %s" % tuple(user_info)
        self._conf_JunOS.load(self.user_set, format="set")
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

    def show(self):
        return self.dev_Connect.cli("show configuration")
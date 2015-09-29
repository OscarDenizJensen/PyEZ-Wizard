from unittest import TestCase
from net.PyEZ_Connect import JunOS_Connection

testHostname = "test"
vlan=["1","2"]
interface=["3","4"]
boot=["192","168","10","1"]
ntp=["192","168","20","1"]
router=["1"]
interface=["2"]
vr_var="VR1"
int_var="em2"
unit_var="100"

v4="192.168.1.1"
interface="em1"
unit="0"
mask="24"

filter_name="F1"
term="T1"
from1="address"
from2="192.168.1.1/30"
then="accept"

name="Per"
action="allow-command"
detail="ssh"

class TestJunOS_Connection(TestCase):
    def test_Constructor(self):
        c = JunOS_Connection()

    def test_hostcommit(self):
        c = JunOS_Connection()
        c.hostcommit( testHostname )

    def test_ssh(self):
        c=JunOS_Connection()
        c.ssh()

    def test_telnet(self):
        c=JunOS_Connection()
        c.telnet()

    def test_ftp(self):
        c=JunOS_Connection()
        c.ftp()

    def test_ntp(self):
        c=JunOS_Connection()
        c.ntp(boot,ntp)

    def test_dhcp(self):
        c=JunOS_Connection()
        c.dhcp(router,add_range)

    def test_vlan(self):
        c=JunOS_Connection()
        c.vlan_Command(vlan,interface)

    def test_vr(self):
        c=JunOS_Connection()
        c.vr(vr_var,int_var,unit_var)

    def test_IPv4(self):
        c=JunOS_Connection()
        c.ipV4(v4, interface, unit, mask)

    def test_IPv6(self):
        c=JunOS_Connection()
        c.ipV6(v4, interface, unit, mask)

    def test_Classes(self):
        c=JunOS_Connection()
        c.classes(name,action,detail)

    def test_fw(self):
        c=JunOS_Connection()
        c.firewall(filter_name, term, from1, from2, then)
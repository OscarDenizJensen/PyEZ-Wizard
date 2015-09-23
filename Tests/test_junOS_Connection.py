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
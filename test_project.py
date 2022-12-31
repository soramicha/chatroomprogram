from project import *

# test to make sure username is not empty
def test_checkusername():
    assert checkusername("") == False
    assert checkusername("Sofa") == True

# test to make sure the ip address is returned as a string
def test_getipaddress():
    assert type(getipaddress()) == str

# test to make sure port number is returned as an integer
def test_binding():
    ip = getipaddress()
    assert type(binding(ip)) == int
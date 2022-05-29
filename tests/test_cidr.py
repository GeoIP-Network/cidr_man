from cidr_man.cidr import CIDR


def test_cidr_init_empty():
    a = CIDR()
    assert a.prefix_len == 0
    assert a.version == 4
    assert a.ip == 0
    assert a.compressed == "0.0.0.0/0"
    assert a.packed == b"\0\0\0\0"
    assert a.network_address == CIDR("0.0.0.0")
    assert a.first_address == CIDR("0.0.0.1")
    assert a.broadcast_address == CIDR("255.255.255.255")
    assert a.last_address == CIDR("255.255.255.254")
    assert a.netmask == CIDR("0.0.0.0")


def test_cidr_init_1():
    a = CIDR("0.0.0.0/1")
    assert a.prefix_len == 1
    assert a.version == 4
    assert a.ip == 0
    assert a.compressed == "0.0.0.0/1"
    assert a.packed == b"\0\0\0\0"
    assert a.network_address == CIDR("0.0.0.0")
    assert a.first_address == CIDR("0.0.0.1")
    assert a.broadcast_address == CIDR("127.255.255.255")
    assert a.last_address == CIDR("127.255.255.254")
    assert a.netmask == CIDR("128.0.0.0")


def test_cidr_init_2():
    a = CIDR("128.0.0.0/1")
    assert a.prefix_len == 1
    assert a.version == 4
    assert a.ip == 2147483648
    assert a.compressed == "128.0.0.0/1"
    assert a.packed == b"\x80\0\0\0"
    assert a.network_address == CIDR("128.0.0.0")
    assert a.first_address == CIDR("128.0.0.1")
    assert a.broadcast_address == CIDR("255.255.255.255")
    assert a.last_address == CIDR("255.255.255.254")
    assert a.netmask == CIDR("128.0.0.0")


def test_cidr_left():
    a = CIDR()
    left = a.left
    assert left.prefix_len == 1
    assert left.version == 4
    assert left.ip == 0
    assert left.compressed == "0.0.0.0/1"
    assert left.packed == b"\0\0\0\0"


def test_cidr_right():
    a = CIDR()
    right = a.right
    assert right.prefix_len == 1
    assert right.version == 4
    assert right.ip == 2147483648
    assert right.compressed == "128.0.0.0/1"
    assert right.packed == b"\x80\0\0\0"


def test_cidr_contains():
    a = CIDR()
    right = a.right
    left = a.left
    assert right in a
    assert left in a
    assert left.left.left in a
    assert right.right.right in a
    assert CIDR("128.0.0.0/24") in a

def test_cidr_v6_init():
    a = CIDR("::/0")
    assert a.prefix_len == 0
    assert a.version == 6
    assert a.ip == 0
    assert a.compressed == "::/0"
    assert a.packed == b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
    assert a.network_address == CIDR("::")
    assert a.first_address == CIDR("::1")
    assert a.broadcast_address == CIDR("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    assert a.last_address == CIDR("ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffe")
    assert a.netmask == CIDR("::")


def test_cidr_v6_init_1():
    a = CIDR("::/1")
    assert a.prefix_len == 1
    assert a.version == 6
    assert a.ip == 0
    assert a.compressed == "::/1"
    assert a.packed == b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
    assert a.network_address == CIDR("::")
    assert a.first_address == CIDR("::1")
    assert a.broadcast_address == CIDR("7fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    assert a.last_address == CIDR("7fff:ffff:ffff:ffff:ffff:ffff:ffff:fffe")
    assert a.netmask == CIDR("8000::")

def test_cidr_v6_init_2():
    a = CIDR("8000::/1")
    assert a.prefix_len == 1
    assert a.version == 6
    assert a.ip == 170141183460469231731687303715884105728
    assert a.compressed == "8000::/1"
    assert a.packed == b"\x80\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
    assert a.network_address == CIDR("8000::")
    assert a.first_address == CIDR("8000::1")
    assert a.broadcast_address == CIDR("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    assert a.last_address == CIDR("ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffe")
    assert a.netmask == CIDR("8000::")


def test_cidr_v6_left():
    a = CIDR("::/0")
    left = a.left
    assert left.prefix_len == 1
    assert left.version == 6
    assert left.ip == 0
    assert left.compressed == "::/1"
    assert left.packed == b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"



def test_cidr_v6_right():
    a = CIDR("::/0")
    right = a.right
    assert right.prefix_len == 1
    assert right.version == 6
    assert right.ip == 170141183460469231731687303715884105728
    assert right.compressed == "8000::/1"
    assert right.packed == b"\x80\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"


def test_cidr_v6_contains():
    a = CIDR("::/0")
    right = a.right
    left = a.left
    assert right in a
    assert left in a
    assert left.left.left in a
    assert right.right.right in a



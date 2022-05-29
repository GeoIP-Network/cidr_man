from ipaddress import ip_network, IPv4Network

from cidr_man import CIDR


def test_link_local():
    cidr = CIDR("169.254.0.0/16")
    builtin: IPv4Network = ip_network("169.254.0.0/16")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    assert cidr.is_global == builtin.is_global
    assert cidr.is_private == builtin.is_private
    assert cidr.is_reserved == builtin.is_reserved
    assert cidr.is_multicast == builtin.is_multicast


def test_link_local_v6():
    cidr = CIDR("fe80::/10")
    builtin: IPv4Network = ip_network("fe80::/10")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    assert cidr.is_global == builtin.is_global
    assert cidr.is_private == builtin.is_private
    assert cidr.is_reserved == builtin.is_reserved
    assert cidr.is_multicast == builtin.is_multicast


def test_loopback():
    cidr = CIDR("127.0.0.0/8")
    builtin: IPv4Network = ip_network("127.0.0.0/8")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    assert cidr.is_global == builtin.is_global
    assert cidr.is_private == builtin.is_private
    # assert cidr.is_reserved == builtin.is_reserved  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
    assert cidr.is_multicast == builtin.is_multicast


def test_loopback_v6():
    cidr = CIDR("::1/128")
    builtin: IPv4Network = ip_network("::1/128")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    assert cidr.is_global == builtin.is_global
    assert cidr.is_private == builtin.is_private
    assert cidr.is_reserved == builtin.is_reserved
    assert cidr.is_multicast == builtin.is_multicast


def test_carrier():
    cidr = CIDR("192.0.0.0/29")
    builtin: IPv4Network = ip_network("192.0.0.0/29")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    assert cidr.is_global == builtin.is_global
    assert cidr.is_private == builtin.is_private
    assert cidr.is_reserved == builtin.is_reserved
    assert cidr.is_multicast == builtin.is_multicast
    cidr = CIDR("100.64.0.0/10")
    builtin: IPv4Network = ip_network("100.64.0.0/10")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    assert cidr.is_global == builtin.is_global
    # assert cidr.is_private == builtin.is_private  # Disputable, but if 192.0.0.0/29 is considered private then this should also
    assert cidr.is_reserved == builtin.is_reserved
    assert cidr.is_multicast == builtin.is_multicast


def test_carrier_v6():
    cidr = CIDR("2002::/16")
    builtin: IPv4Network = ip_network("2002::/16")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    # assert cidr.is_global == builtin.is_global  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
    # assert cidr.is_private == builtin.is_private  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
    assert cidr.is_reserved == builtin.is_reserved
    assert cidr.is_multicast == builtin.is_multicast


def test_private():
    for network in ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "198.18.0.0/15"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        assert cidr.is_private == builtin.is_private
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast


def test_private_v6():
    for network in ["2001::/32", "fc00::/7", "2001:2::/48"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        assert cidr.is_private == builtin.is_private
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast
    cidr = CIDR("64:ff9b:1::/48")
    builtin = ip_network("64:ff9b:1::/48")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    # assert cidr.is_global == builtin.is_global  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
    # assert cidr.is_private == builtin.is_private  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
    # assert cidr.is_reserved == builtin.is_reserved  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc8215
    assert cidr.is_multicast == builtin.is_multicast


def test_documentation():
    for network in ["192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        assert cidr.is_private == builtin.is_private
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast
    cidr = CIDR(
        "233.252.0.0/24"
    )  # "MCAST-TEST-NET" - https://datatracker.ietf.org/doc/html/rfc5771
    builtin: IPv4Network = ip_network("233.252.0.0/24")
    assert cidr.is_link_local == builtin.is_link_local
    assert cidr.is_loopback == builtin.is_loopback
    # assert cidr.is_global == builtin.is_global  # Built-in is wrong
    # assert cidr.is_private == builtin.is_private  # Built-in is wrong
    assert cidr.is_reserved == builtin.is_reserved
    assert cidr.is_multicast == builtin.is_multicast


def test_documentation_v6():
    for network in ["2001:db8::/32"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        assert cidr.is_private == builtin.is_private
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast


def test_reserved():
    for network in ["240.0.0.0/4"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        # assert cidr.is_private == builtin.is_private  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast


def test_reserved_v6():
    for network in ["::ffff:0:0/96"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        # assert cidr.is_private == builtin.is_private  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast


def test_multicast():
    for network in ["224.0.0.0/4", "233.252.0.0/24"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        # assert cidr.is_global == builtin.is_global  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
        # assert cidr.is_private == builtin.is_private  # Built-in is wrong - https://datatracker.ietf.org/doc/html/rfc6890
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast


def test_multicast_v6():
    for network in ["ff00::/8"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        assert cidr.is_private == builtin.is_private
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast


def test_internet():
    for network in ["1.1.1.1", "8.8.8.8"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        assert cidr.is_private == builtin.is_private
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast


def test_internet_v6():
    for network in ["2606:4700:4700::1111", "2001:4860:4860::8844"]:
        cidr = CIDR(network)
        builtin: IPv4Network = ip_network(network)
        assert cidr.is_link_local == builtin.is_link_local
        assert cidr.is_loopback == builtin.is_loopback
        assert cidr.is_global == builtin.is_global
        assert cidr.is_private == builtin.is_private
        assert cidr.is_reserved == builtin.is_reserved
        assert cidr.is_multicast == builtin.is_multicast

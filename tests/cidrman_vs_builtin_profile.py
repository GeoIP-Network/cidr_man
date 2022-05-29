from ipaddress import IPv4Network

from cidr_man.cidr import CIDR

for i in range(1000):
    subnets = []
    subnets2 = []
    with open("data/children_test_data") as f:
        for line in f:
            net = CIDR(line.strip())
            subnets += list(net.subnets)
            net2 = IPv4Network(line.strip())
            subnets2 += list(net2.subnets())
    for i in range(1000):
        supernet = CIDR(f"{i%255}.0.0.0/8")
        subnet = CIDR(f"{i % 255}.{i % 255}.0.0/24")
        a = subnet in supernet
        supernet = IPv4Network(f"{i % 255}.0.0.0/8")
        subnet = IPv4Network(f"{i % 255}.{i % 255}.0.0/24")
        b = subnet.subnet_of(supernet)
    for i in range(1000):
        subnet = CIDR(f"{i % 255}.{i % 255}.0.0/24")
        a = subnet.compressed
        subnet = IPv4Network(f"{i % 255}.{i % 255}.0.0/24")
        b = subnet.compressed


print(subnets.sort() == subnets2.sort())

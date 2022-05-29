# CIDR-Man
![Release Badge](https://gitlab.com/geoip.network/cidr_man/-/badges/release.svg)
![Pipeline Badge](https://gitlab.com/geoip.network/cidr_man/badges/main/pipeline.svg)

Built due to frustrations with python's built-in `ipaddress` library's performance, code complexity, and accuracy.
CIDR-Man is an accurate high-performance IP address subnetting library.


CIDR (or Classless Inter-Domain Routing) is a way of representing and handling IP addresses and networks. 
Introduced in 1993 to replace the previous IP address class architecture, CIDRs offer more flexibility in addressing hierarchy in network designs.
A block of IP addresses in CIDR notation would be represented as the first IP in the block followed by the number of bits in the bitmask separated by a forward slash. 

For example, the CIDR 192.0.2.0/24 represents an IP address block spanning 192.0.2.0 to 192.0.2.255.
Expanding this out we get the following:

    Network:                                192.0.2.0
    Network (as binary):                    11000000000000000000001000000000
    Netmask:                                255.255.255.0
    Netmask (as binary):                    11111111111111111111111100000000
    Broadcast IP:                           192.0.2.255
    Broadcast IP (as binary):               11000000000000000000001011111111
    First usable IP (normally the Gateway): 192.0.2.1
    First usable IP (as binary):            11000000000000000000001000000001
    Last usable IP:                         192.0.2.255
    Last usable IP (as binary):             11000000000000000000001011111110

Using this representation a single IP address is simply one with a full bitmask, thus 192.0.2.1/32 is the same as 192.0.2.1.

This means that our network subnetting library only needs a single class `CIDR`. 
Utilising a single type `CIDR` to represent both network objects and individual addresses results in considerably more concise code.

While the interface of this new library is a little different from that of the built-in library, we think you'll find it to be more "pythonic", and quite intuitive.

*NOTE: While writing tests for this library we discovered that a number of the `is_<address type>` flags from the python built-in library were returning incorrect results. CIDR-Man is accurate as per the RFCs at the time of writing, thus our responses may differ.*

## Usage
### Initialisation

Initialising a new CIDR object is easy and supports all common input types (presentation format, integer format, network/big-endian byte format, and built-in IP & Network types).
```python
from cidr_man import CIDR, Version

## Create from string (presentation format)
network = CIDR("192.0.2.0/24")
ip = CIDR("192.0.2.1")

network_v6 = CIDR("2001:db8::/56")
machine_alloc_v6 = CIDR("2001:db8::/64")
ip_v6 = CIDR("2001:db8::1")

## Create from built-in
network = CIDR(IPv4Network("192.0.2.0/24"))
ip = CIDR(IPv4Address("192.0.2.1"))

network_v6 = CIDR(IPv6Network("2001:db8::/56"))
machine_alloc_v6 = CIDR(IPv6Network("2001:db8::/64"))
ip_v6 = CIDR(IPv6Address("2001:db8::1"))


## Create from integer
network = CIDR(3221225984, version=Version.v4, prefix_len=24)
ip = CIDR(3221225985, version=Version.v4)

network_v6 = CIDR(42540766411282592856903984951653826560, version=Version.v6, prefix_len=56)
ip_v6 = CIDR(42540766411282592856903984951653826561, version=Version.v6)


## Create from byte
network = CIDR(b'\xc0\x00\x02\x01', prefix_len=24)
ip = CIDR(b'\xc0\x00\x02\x01')

network_v6 = CIDR(b' \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01', prefix_len=56)
ip_v6 = CIDR(b' \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
```

## Get subnets
Retrieving the direct subnets of a network is easy.

To get the pair
```python
network = CIDR("192.0.2.0/24")
subnets = network.subnets  # (CIDR("192.0.2.0/25"), CIDR("192.0.2.128/25"))
```
To get only the "left" (low-bit subnet)
```python
left = network.left  # CIDR("192.0.2.0/25")
```
To get only the "right" (high-bit subnet)
```python
right = network.right  # CIDR("192.0.2.128/25")
```
These can be chained for quick traversal
```python
left_of_left = network.left.left  # CIDR("192.0.2.0/26")
right_of_left = network.left.right  # CIDR(192.0.2.64/26")
```

## Contains
Checking if one network is the subnet of another
```python
network_1 = CIDR("192.0.2.0/24")
network_2 = CIDR("192.0.2.0/26")
result = network_2 in network_1
```

Alternatively
```python
network_1.contains(network_2)
```


## Packed (Byte format)
```python
ip_b = ip.packed  # b'\xc0\x00\x02\x01'

ipv6_b = ip.packed  # b' \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
```

## Compressed (String / Presentation format)
CIDRs that have a `prefix_len` equal to the maximum for their IP version (that is 32 for IPv4, and 128 for IPv6) will be presented in IP presentation format.
Therefore, both `CIDR("192.0.2.1")` and `CIDR("192.0.2.1/32")` produce the presentation format `"192.0.2.1"`.
```python
# IPv4

ip_s = ip.compressed  # "192.0.2.1"
### or
ip_s = str(ip)  # "192.0.2.1"

## CIDRs who's prefix is not the max_prefix are presented in CIDR presentation format
network_s = network.compressed  # "192.0.2.0/24"
### or
network_s = str(ip)  # "192.0.2.0/24"


# IPv6
ipv6_s = ip.compressed  # "2001:db8::1"
### or
ipv6_s = str(ip)  # "2001:db8::1"

network_v6_s = network.compressed  # "2001:db8::/56"
## or
network_v6_s = str(ip)  # "2001:db8::/56"
```

## Important addresses
`network_address`, `broadcast_address`, `netmask`, `first_address`, and `last_address` each provide the relevant addresses as new CIDR objects.
```python
# IPv4
net_address         = network.network_address  # 192.0.2.0
first_address       = network.first_address  # 192.0.2.1
last_address        = network.last_address  # 192.0.2.254
broadcast_address   = network.network_address  # 192.0.2.255
netmask             = network.netmask  # 255.255.255.0

# IPv6
net_address_v6         = network_v6.network_address  # 2001:db8::
first_address_v6       = network_v6.first_address  # 2001:db8::1
last_address_v6        = network_v6.last_address  # 2001:db8:0:ff:ffff:ffff:ffff:fffe
broadcast_address_v6   = network_v6.network_address  # 2001:db8:0:ff:ffff:ffff:ffff:ffff
netmask_v6             = network_v6.netmask  # ffff:ffff:ffff:ff00::
```


## Installation (from pip):
```shell
pip install cidr_man
```

## Installation (from source):
```shell
git clone https://gitlab.com/geoip.network/cidr_man
poetry install
```

## Theme song
CIDR-Man, CIDR-Man, Does what ever a CIDR can... 

*Thwip! Thwip! """""""""""""""""""""""""""""""""""""""""""""""""*
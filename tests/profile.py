from cidr_man.web import Web

for i in range(1000):
    root = Web()
    subnets = []
    with open("data/children_test_data") as f:
        for line in f:
            root.insert(line.strip())
            subnets.append(line.strip())
    result = [node.prefix.compressed for node in root.children()]

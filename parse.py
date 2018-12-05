#!/usr/bin/python3

from kinparse import parse_netlist

class Component:
    ''' Store the details of a graphical componenet Reference, Type and Address '''

    def __init__(self, ref, node_type, address):
        self.ref = ref
        self.node_type = node_type
        self.address = address
        child_nodes = []

components = []

nlst = parse_netlist('Test/Test.net')

for component in nlst.components:
    print('%s  %s  %s' %(component.ref.val, component.part.val, component.value.val,))
    components.append(Component(component.ref.val, component.part.val, component.value.val))

for net in nlst.nets:
    nodes = []
    for node in net.nodes:
        nodes.append(node.ref.val)
#        print("%s" % (node.ref.val,))
    print(net.name.val)
    for ref in nodes:
        print("\t%s" % (node,))

#
# This is just a hard coded output file for the moment. It's picked up from an
# MPLAB-X Project for the controller.
#
output_file = open("/home/john/Private/es/programming/mcp/CinnamonBun/Firmware/CAN_Node.X/src/application/Controller/network.h","w")

output_file.write('#define NUM_NET_NODES %d\n' % (len(nlst.components),))
output_file.write('static struct net_node nnodes[NUM_NET_NODES];\n')


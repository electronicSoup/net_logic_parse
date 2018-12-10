#!/usr/bin/python3

from kinparse import parse_netlist

class Component:
    ''' Store the details of a graphical componenet Reference, Type and Address '''

    def __init__(self, ref, node_type, address):
        self.ref = ref
        self.node_type = node_type
        self.address = address
        self.child_nodes = []
        self.logic = None

components = []

def find_component(ref):
    for index, component in enumerate(components):
        if component.ref == ref:
            return index

    return None

nlst = parse_netlist('Test/Test.net')

for component in nlst.components:
    print('%s  %s  %s' %(component.ref.val, component.part.val, component.value.val,))
    components.append(Component(component.ref.val, component.part.val, component.value.val))

for net in nlst.nets:
    net_nodes = []
    input_node = None
    input_ref = None

    for node in net.nodes:
        net_nodes.append(node.ref.val)
    print(net.name.val)

    # Find the input node on the current net
    for ref in net_nodes:
        index = find_component(ref)
        if index is not None:
            print("Found {}".format(components[index].ref))
            if components[index].node_type == 'bool_input_431':
                input_node = index
                input_ref = components[index].ref
        else:
            print("NOT FOUND!")

    # Now have the input node so add all other nodes on the net to the Input nodes
    # list of effected outputs.
            

#
# This is just a hard coded output file for the moment. It's picked up from an
# MPLAB-X Project for the controller.
#
output_file = open("/home/john/Private/es/programming/mcp/CinnamonBun/Firmware/CAN_Node.X/src/application/Controller/network.h","w")

output_file.write('#define NUM_NET_NODES %d\n' % (len(nlst.components),))
output_file.write('static struct net_node nnodes[NUM_NET_NODES] = {\n')

for component in components:
    output_file.write('\t{\n')

    # define the type of each component in the component list.
    output_file.write('\t\t.type = ')
    if component.node_type == 'bool_input_431':
        output_file.write('b431_in,\n')
    if component.node_type == 'bool_output_431':
        output_file.write('b431_out,\n')

    # The Address of the component
    output_file.write('\t\t.address = %s,\n' % (component.address,))

    output_file.write('\t},\n')
output_file.write('};\n')



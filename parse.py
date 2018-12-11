#!/usr/bin/python3

from kinparse import parse_netlist

class Component:
    ''' Store the details of a graphical componenet Reference, Type and Address '''

    def __init__(self, ref, node_type, address):
        self.ref = ref
        self.node_type = node_type
        self.address = address
        self.effected_nodes = []
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
    in431_nodes = []
    out431_nodes = []
    input_node = None
    input_ref = None

    for node in net.nodes:
        index = find_component(node.ref.val)

        if index is None:
            print("Error Node {} not found".format(node.ref.val))
            exit
            
        if components[index].node_type == 'bool_input_431':
            print("Added Input node for net {}".format(index))
            in431_nodes.append(index)
        if components[index].node_type == 'bool_output_431':
            print("Added Output node for net {}".format(index))
            out431_nodes.append(index)

    for in_index in in431_nodes:
        for out_index in out431_nodes:
            components[in_index].effected_nodes.append(out_index)

#
# This is just a hard coded output file for the moment. It's picked up from an
# MPLAB-X Project for the controller.
#
output_file = open("/home/john/Private/es/programming/mcp/CinnamonBun/Firmware/CAN_Node.X/src/application/Controller/network.h","w")

for component in components:
    if len(component.effected_nodes) > 0:
        output_file.write('uint16_t {}_effected[{}] = '.format(component.ref, len(component.effected_nodes)))
        output_file.write('{')        
        for node in component.effected_nodes:
            output_file.write('{},'.format(node))
        output_file.write('};\n')

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
    output_file.write('\t\t.address.es_bool.byte = %s,\n' % (component.address,))

    # Effected component list
    output_file.write('\t\t.number_effected = {},\n'.format(len(component.effected_nodes)))
    if len(component.effected_nodes):
        output_file.write('\t\t.effected = (uint16_t *)&{}_effected[0],\n'.format(component.ref))
    else:
        output_file.write('\t\t.effected = NULL,\n')
        
    output_file.write('\t\t.logic = NULL,\n')

    output_file.write('\t},\n')
output_file.write('};\n')



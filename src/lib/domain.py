
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

import xml.etree.ElementTree as Etree


class Domain(object):

    def __init__(self, template='linux'):
        template_file = '/var/lib/tina/templates/%s.tpl.xml' % template
        self.tree = Etree.parse(template_file)
        self.root = self.tree.getroot()
        self.devices = self.root.find('devices')

    def set_name(self, name):
        """ Define domain name
        """
        xname = self.root.find('name')
        xname.text = name

    def set_uuid(self, uuid):
        """ Define domain uuid
        """
        xuuid = self.root.find('uuid')
        xuuid.text = str(uuid)

    def set_vcpus(self, value=1):
        """ Define vcpu number
        """
        vcpu = self.root.find('vcpu')
        vcpu.text = str(value)

    def set_memory(self, value=1):
        """ Define memory value (Gigabytes)
        """
        memory = self.root.find('memory')
        memory.text = str(value)

    def set_disks(self, disk_list=[]):
        """ Define disks on domain
        """
        for disk in disk_list:
            self._add_disk(disk['slot'], disk['path'], disk['device'])

    def _add_disk(self, path, device):
        """ Create disk
        """
        disk = SubElement(self.devices, 'disk', {'type': 'file',
                                                 'device': 'disk'
                                                 })

        SubElement(disk, 'driver', {'name': 'qemu',
                                    'type': 'qcow2',
                                    'cache': 'none',
                                    'io': 'native'
                                    })
        SubElement(disk, 'source', {'file': str(path)})
        SubElement(disk, 'target', {'dev': str(device),
                                    'bus': 'virtio'
                                    })

    def _add_interface(self, mac, vlan):
        """ Create network interface
        """
        iface = SubElement(self.devices, 'interface', {'type': 'bridge'})
        SubElement(iface, 'mac', {'address': str(mac)})
        SubElement(iface, 'source', {'bridge': 'ovsbr0'})
        vlan = SubElement(iface, 'vlan')
        SubElement(vlan, 'tag', {'id': str(vlan)})
        SubElement(iface, 'virtualport', {'type': 'openvswitch'})
        SubElement(iface, 'model', {'type': 'virtio'})

    def create(self):
        """ Return complete domain xml
        """
        output = _prettify(self.root)
        return output

    def _prettify(self, element):
        """ Return a pretty-printed XML string for the element
        """
        raw = ETree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(raw)
        return reparsed.toprettyxml(indent="  ")

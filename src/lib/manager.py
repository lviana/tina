
import libvirt


class Manager(object):

    def __init__(self, hypervisor):
        self.conn = libvirt.open("qemu+tls://%s/system" % hypervisor)

    def list_domains(self):
        """ List available domains
        """
        domains = []
        for id in self.conn.listDomainsID():
            dom = self.conn.lookupByID(id)
            name = dom.name()
            info = dom.info()
            domains.append({name: info})

        return domains

    def create_domain(self, xmlschema):
        """ Create domain
        """
        output = self.conn.defineXML(xmlschema)

    def start_domain(self, name):
        """ Power on virtual domain
        """
        try:
            domain = self.conn.lookupByName(name)
            domain.create()

        except libvirt.libvirtError, e:
            return e

    def get_domain_status(self, name):
        """ Domain execution status
        """
        domain = self.conn.lookupByName(name)
        status = domain.isActive()
        if status == 0:
            output = 'stopped'
        else:
            output = 'running'

        return output

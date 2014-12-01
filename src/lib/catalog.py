
import ConfigParser
import uuid
import virtinst.util

from tina.model import Machine, Disk, Interface, Pool

from sqlalchemy import create_engine
from sqlalchemy.orm import exc
from sqlalchemy.orm import sessionmaker


class Catalog(object):

    def __init__(self, name):
        self.name = name
        config = self.get_config()
        self.engine = create_engine('%s://%s:%s@%s/%s' % 
                                    config.get('driver'),
                                    config.get('dbuser'),
                                    config.get('dbpass'),
                                    config.get('dbhost'),
                                    config.get('dbname'))
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_config(self):
        configp   = ConfigParser.ConfigParser()
        configp.read('/etc/locaweb/tina.conf')
        config = {}
        config['driver'] = configp.get('driver')        
        config['dbuser'] = configp.get('username')
        config['dbpass'] = configp.get('password')
        config['dbhost'] = configp.get('server')
        config['dbname'] = configp.get('database')
        return config

    def create_machine(self, pool, machine={}):
        """ Create new virtual machine on database
        """
        vmuuid = str(uuid.uuid1())
        name = machine['name']
        vcpu = machine['vcpu']
        memory = machine['memory']
        
        newvm = Machine(vmuuid, name, vcpu, memory, pool)

        newvm.disks = []
        for disk in machine['disks']:
            newvm.disks.append(Disk(disk['name'], disk['device'], disk['dataset']))

        newvm.interfaces = []
        for iface in machine['interfaces']:
            newvm.interfaces.append(Interface(iface['mac'], iface['vlan']))

        # ToDo: Generating new mac address: virtinst.util.randomMAC()
        # Maybe it shouldn't be here!

        self.session.add(newvm)
        self.session.commit()

    def get_machine_info(self, name):
        """ Load virtual machine attributes
        """
        vm = self.session.query(Machine).filter_by(name=name).one()
        machine = {'name': vm.name,
                   'uuid': vm.uuid,
                   'vcpu': vm.vcpu,
                   'memory': vm.memory,
                   'pool': vm.pool,
                   'disks': [],
                   'interfaces': []
                   }
        for disk in vm.disks:
            machine['disks'].append({'name': disk.name,
                                     'pciid': disk.pciid,
                                     'device': disk.device,
                                     'dataset': disk.dataset
                                     }
                                    )

        for iface in vm.interfaces:
            machine['interfaces'].append({'id': iface.id,
                                          'mac': iface.mac,
                                          'vlan': iface.vlan
                                          }
                                         )

        return machine

    def remove_machine(self, name):
        """ Remove virtual machine from database
        """
        vm = self.session.query(Machine).filter_by(name=name).one()

        self.session.delete(vm)
        self.session.commit()

    def get_pool_info(self, name):
        """ Load pool attributes
        """
        pool = self.session.query(Pool).filter_by(name=name).one()
        output = {'name': pool.name,
                  'address': pool.address,
                  'cores': pool.cores,
                  'memory': pool.memory
                  }

        return output
        
    def create_pool(self, name, address, memory=0, cores=0):
        """ Create new virtualzation host on database
        """
        newpool = Pool(name, memory, cores, address)
        self.session.add(newpool)
        self.session.commit()

    def remove_pool(self, name):
        """ Remove virtualization host from database
        """
        try:
            pool = self.session.query(Pool).filter_by(name=name).one()
        except exc.NoResultFound:
            return False

        self.session.delete(pool)
        self.session.commit()

    def update_machine(self, name):
        """ Update virtual machine information
        """
        # To do!
        pass


from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://orchestrator:orchpassword@localhost/orchestratordb', echo=True)

Base = declarative_base()


class Machine(Base):
    __tablename__ = 'machines'

    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    vcpu = Column(Integer)
    memory = Column(Integer)
    pool_id = Column(Integer, ForeignKey('pools.id'))

    disks = relationship('Disk', backref='machine', cascade='all, delete, delete-orphan')
    interfaces = relationship('Interface', backref='machine', cascade='all, delete, delete-orphan')

    def __init__(self, uuid, name, vcpu, memory, pool_id):
        self.uuid = uuid
        self.name = name
        self.vcpu = vcpu
        self.memory = memory
        self.pool_id = pool_id

    def __repr__(self):
        return "<Machine('%s', '%s', '%s', '%s', '%s')>" % (self.uuid,
                                                            self.name,
                                                            self.vcpu,
                                                            self.memory)


class Disk(Base):
    __tablename__ = 'disks'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    device = Column(String, nullable=False)
    dataset = Column(String, nullable=False)
    machine_id = Column(Integer, ForeignKey('machines.id'))

    def __init__(self, name, device, dataset):
        self.name = name
        self.device = device
        self.dataset = dataset

    def __repr__(self):
        return "<Disk('%s', '%s', '%s', '%s')>" % (self.name,
                                                   self.device,
                                                   self.dataset)


class Interface(Base):
    __tablename__ = 'interfaces'

    id = Column(Integer, autoincrement=True, primary_key=True)
    mac = Column(String, nullable=False, unique=True)
    vlan = Column(Integer)
    machine_id = Column(Integer, ForeignKey('machines.id'))

    def __init__(self, mac, vlan):
        self.mac = mac
        self.vlan = vlan

    def __repr__(self):
        return "<Interface('%s', '%s')>" % (self.mac, self.vlan)


class Pool(Base):
    __tablename__ = 'pools'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    memory = Column(Integer)
    cores = Column(Integer)
    address = Column(String, nullable=False, unique=True)

    machines = relationship("Machine", backref="pool")

    def __init__(self, name, memory, cores, address):
        self.name = name
        self.memory = memory
        self.cores = cores
        self.address = address

    def __repr__(self):
        return "<Pool('%s', '%s')>" % (self.name,
                                       self.memory,
                                       self.cores,
                                       self.address)


# Creating database and modifying it during development only!    
Base.metadata.create_all(engine) 

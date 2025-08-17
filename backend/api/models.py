from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Ассоциативные таблицы (many-to-many)
alteration_to_product = Table(
    'alteration_to_product', Base.metadata,
    Column('iid_product', Integer, ForeignKey('product.iid'), primary_key=True),
    Column('iid_alteration', Integer, ForeignKey('alteration.iid'), primary_key=True)
)

incident_to_appeal = Table(
    'incident_to_appeal', Base.metadata,
    Column('iid_appeal', Integer, ForeignKey('appeal.iid'), primary_key=True),
    Column('iid_incident', Integer, ForeignKey('incident.iid'), primary_key=True)
)

user_to_workgroup = Table(
    'user_to_workgroup', Base.metadata,
    Column('iid_workgroup', Integer, ForeignKey('workgroup.iid'), primary_key=True),
    Column('iid_user', Integer, ForeignKey('portal_user.iid'), primary_key=True)
)

workgroup_to_product = Table(
    'workgroup_to_product', Base.metadata,
    Column('iid_workgroup', Integer, ForeignKey('workgroup.iid'), primary_key=True),
    Column('iid_product', Integer, ForeignKey('product.iid'), primary_key=True)
)


class UserRole(Base):
    __tablename__ = 'user_role'

    iid = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    create_incident = Column(Boolean)
    direct_incident = Column(Boolean)
    create_alteration = Column(Boolean)
    create_task = Column(Boolean, default=False)
    create_order = Column(Boolean, default=False)
    create_appeal = Column(Boolean, default=True)

    # Обратная связь с пользователями
    users = relationship("PortalUser", back_populates="role")

    def __repr__(self):
        return f"<UserRole(iid={self.iid}, title='{self.title}')>"


class PortalUser(Base):
    __tablename__ = 'portal_user'

    iid = Column(Integer, primary_key=True, autoincrement=True)
    ad_login = Column(Text, nullable=False)
    ad_name = Column(Text, nullable=False)
    ad_email = Column(Text, nullable=False)
    additional_email = Column(Text)
    mobile_phone = Column(Text, nullable=False)
    portal_role = Column(Integer, ForeignKey('user_role.iid'), default=1, nullable=False)

    # Связи
    role = relationship("UserRole", back_populates="users")
    alterations_created = relationship("Alteration", foreign_keys="[Alteration.iid_user]", back_populates="creator")
    alterations_assigned = relationship("Alteration", foreign_keys="[Alteration.iid_executor]", back_populates="executor")
    
    appeals_created = relationship("Appeal", foreign_keys="[Appeal.iid_user]", back_populates="creator")
    appeals_assigned = relationship("Appeal", foreign_keys="[Appeal.iid_executor]", back_populates="executor")
    
    tasks_created = relationship("Task", foreign_keys="[Task.iid_user]", back_populates="creator")
    tasks_assigned = relationship("Task", foreign_keys="[Task.iid_executor]", back_populates="executor")
    
    orders_created = relationship("Order", foreign_keys="[Order.iid_user]", back_populates="creator")
    orders_assigned = relationship("Order", foreign_keys="[Order.iid_executor]", back_populates="executor")
    
    managed_workgroups = relationship("Workgroup", back_populates="manager")
    products_managed = relationship("Product", back_populates="manager")

    # Many-to-many с рабочими группами
    workgroups = relationship("Workgroup", secondary=user_to_workgroup, back_populates="users")

    def __repr__(self):
        return f"<PortalUser(iid={self.iid}, ad_login='{self.ad_login}', ad_name='{self.ad_name}')>"


class Alteration(Base):
    __tablename__ = 'alteration'

    iid = Column(Integer, primary_key=True, autoincrement=True)
    iid_user = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    iid_executor = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)

    # Связи
    creator = relationship("PortalUser", foreign_keys=[iid_user], back_populates="alterations_created")
    executor = relationship("PortalUser", foreign_keys=[iid_executor], back_populates="alterations_assigned")
    
    # Связь с продуктами через many-to-many
    products = relationship("Product", secondary=alteration_to_product, back_populates="alterations")

    def __repr__(self):
        return f"<Alteration(iid={self.iid}, title='{self.title}')>"


class Appeal(Base):
    __tablename__ = 'appeal'

    iid = Column(Integer, primary_key=True, autoincrement=True)
    iid_user = Column(Integer, ForeignKey('portal_user.iid'), nullable=False, default=-1)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    iid_executor = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)

    # Связи
    creator = relationship("PortalUser", foreign_keys=[iid_user], back_populates="appeals_created")
    executor = relationship("PortalUser", foreign_keys=[iid_executor], back_populates="appeals_assigned")
    
    incidents = relationship("Incident", secondary=incident_to_appeal, back_populates="appeals")

    def __repr__(self):
        return f"<Appeal(iid={self.iid}, title='{self.title}')>"


class Incident(Base):
    __tablename__ = 'incident'

    iid = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    # Связь с обращениями
    appeals = relationship("Appeal", secondary=incident_to_appeal, back_populates="incidents")

    def __repr__(self):
        return f"<Incident(iid={self.iid}, title='{self.title}')>"


class Order(Base):
    __tablename__ = 'order'

    iid = Column(Integer, primary_key=True, autoincrement=True)
    iid_user = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    iid_executor = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)

    # Связи
    creator = relationship("PortalUser", foreign_keys=[iid_user], back_populates="orders_created")
    executor = relationship("PortalUser", foreign_keys=[iid_executor], back_populates="orders_assigned")

    def __repr__(self):
        return f"<Order(iid={self.iid}, title='{self.title}')>"


class Product(Base):
    __tablename__ = 'product'

    iid = Column(Integer, primary_key=True, autoincrement=True)
    short_title = Column(Text, nullable=False)
    long_title = Column(Text)
    iid_manager = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)

    # Связи
    manager = relationship("PortalUser", back_populates="products_managed")
    alterations = relationship("Alteration", secondary=alteration_to_product, back_populates="products")
    workgroups = relationship("Workgroup", secondary=workgroup_to_product, back_populates="products")

    def __repr__(self):
        return f"<Product(iid={self.iid}, short_title='{self.short_title}')>"


class Task(Base):
    __tablename__ = 'task'

    iid = Column(Integer, primary_key=True, autoincrement=True)
    iid_user = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    iid_executor = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)

    # Связи
    creator = relationship("PortalUser", foreign_keys=[iid_user], back_populates="tasks_created")
    executor = relationship("PortalUser", foreign_keys=[iid_executor], back_populates="tasks_assigned")

    def __repr__(self):
        return f"<Task(iid={self.iid}, title='{self.title}')>"


class Workgroup(Base):
    __tablename__ = 'workgroup'

    iid = Column(Integer, primary_key=True, autoincrement=True)
    short_title = Column(Text, nullable=False)
    long_title = Column(Text)
    location = Column(Text, nullable=False)
    iid_manager = Column(Integer, ForeignKey('portal_user.iid'), nullable=False)

    # Связи
    manager = relationship("PortalUser", back_populates="managed_workgroups")
    users = relationship("PortalUser", secondary=user_to_workgroup, back_populates="workgroups")
    products = relationship("Product", secondary=workgroup_to_product, back_populates="workgroups")

    def __repr__(self):
        return f"<Workgroup(iid={self.iid}, short_title='{self.short_title}')>"
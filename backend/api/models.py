from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from typing import List, Optional


class Base(DeclarativeBase):
    pass


# Модель: user_role
class UserRole(Base):
    __tablename__ = "user_role"
    __doc__ = "Роли пользователей портала"

    iid = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    create_incident = Column(Boolean, nullable=True)
    direct_incident = Column(Boolean, nullable=True)
    create_alteration = Column(Boolean, nullable=True)
    create_task = Column(Boolean, default=False)
    create_order = Column(Boolean, default=False)
    create_appeal = Column(Boolean, default=True)

    # Обратные связи
    users = relationship("PortalUser", back_populates="role")
    # workgroups = relationship("Workgroup", back_populates="manager_role")
    # products = relationship("Product", back_populates="manager_role")


# Модель: portal_user
class PortalUser(Base):
    __tablename__ = "portal_user"
    __doc__ = "Пользователи портала"

    iid = Column(Integer, primary_key=True, autoincrement=True)
    ad_login = Column(Text, nullable=False)
    ad_name = Column(Text, nullable=False)
    ad_email = Column(Text, nullable=False)
    additional_email = Column(Text, nullable=True)
    mobile_phone = Column(Text, nullable=False)
    portal_role = Column(Integer, ForeignKey("user_role.iid"), nullable=False, default=1)

    # Связи
    role = relationship("UserRole", back_populates="users")
    alterations_created = relationship("Alteration", foreign_keys="[Alteration.iid_user]", back_populates="creator")
    alterations_executed = relationship("Alteration", foreign_keys="[Alteration.iid_executor]", back_populates="executor")
    appeals_created = relationship("Appeal", foreign_keys="[Appeal.iid_user]", back_populates="creator")
    appeals_executed = relationship("Appeal", foreign_keys="[Appeal.iid_executor]", back_populates="executor")
    orders_created = relationship("Order", foreign_keys="[Order.iid_user]", back_populates="creator")
    orders_executed = relationship("Order", foreign_keys="[Order.iid_executor]", back_populates="executor")
    tasks_created = relationship("Task", foreign_keys="[Task.iid_user]", back_populates="creator")
    tasks_executed = relationship("Task", foreign_keys="[Task.iid_executor]", back_populates="executor")
    managed_workgroups = relationship("Workgroup", foreign_keys="[Workgroup.iid_manager]", back_populates="manager")
    managed_products = relationship("Product", foreign_keys="[Product.iid_manager]", back_populates="manager")
    workgroups = relationship("UserToWorkgroup", back_populates="user")
    incidents = relationship("Incident", back_populates="executors")  # через appeal
    appeals = relationship("Appeal", back_populates="executors")


# Модель: alteration (изменение)
class Alteration(Base):
    __tablename__ = "alteration"
    __doc__ = "Изменение: может быть создано только разработчиком в рамках существующего Продукта"

    iid = Column(Integer, primary_key=True, autoincrement=True)
    iid_user = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    iid_executor = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)

    # Связи
    creator = relationship("PortalUser", foreign_keys=[iid_user], back_populates="alterations_created")
    executor = relationship("PortalUser", foreign_keys=[iid_executor], back_populates="alterations_executed")
    products = relationship("AlterationToProduct", back_populates="alteration")


# Модель: appeal (обращение)
class Appeal(Base):
    __tablename__ = "appeal"
    __doc__ = "Обращение"

    iid = Column(Integer, primary_key=True, autoincrement=True)
    iid_user = Column(Integer, ForeignKey("portal_user.iid"), nullable=False, default=-1)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    iid_executor = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)

    # Связи
    creator = relationship("PortalUser", foreign_keys=[iid_user], back_populates="appeals_created")
    executor = relationship("PortalUser", foreign_keys=[iid_executor], back_populates="appeals_executed")
    incidents = relationship("IncidentToAppeal", back_populates="appeal")
    executors = relationship("PortalUser", back_populates="appeals")


# Модель: incident (инцидент)
class Incident(Base):
    __tablename__ = "incident"
    __doc__ = "Инцидент"

    iid = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    # Связи
    appeals = relationship("IncidentToAppeal", back_populates="incident")
    executors = relationship("PortalUser", secondary="incident_to_appeal", back_populates="incidents")


# Модель: order (заказ)
class Order(Base):
    __tablename__ = "order"
    __doc__ = "Заказ: специально для кадровых или иных служб, работающих с предметами, существующими в реале - заказ документов, справок, канцелярии и тд. Создается ответственными пользователями, должность или подразделение которых соответствует условию в системе"

    iid = Column(Integer, primary_key=True, autoincrement=True)
    iid_user = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    iid_executor = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)

    # Связи
    creator = relationship("PortalUser", foreign_keys=[iid_user], back_populates="orders_created")
    executor = relationship("PortalUser", foreign_keys=[iid_executor], back_populates="orders_executed")


# Модель: product (продукт)
class Product(Base):
    __tablename__ = "product"
    __doc__ = "Продукт: информация по продукту. В рамках него могут создаваться изменения. Продукт может создать только Администратор. К продукту привязан список рабочих групп, который может менять только Админ. Изменения сразу направляются на рабочую группу, которую выберет разработчик."

    iid = Column(Integer, primary_key=True, autoincrement=True)
    short_title = Column(Text, nullable=False)
    long_title = Column(Text, nullable=True)
    iid_manager = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)

    # Связи
    manager = relationship("PortalUser", foreign_keys=[iid_manager], back_populates="managed_products")
    alterations = relationship("AlterationToProduct", back_populates="product")
    workgroups = relationship("WorkgroupToProduct", back_populates="product")
    manager_role = relationship("UserRole", back_populates="products")


# Модель: task (задача)
class Task(Base):
    __tablename__ = "task"
    __doc__ = "Задача: вариант инцидента, не требующий получения обратной связи от пользователя. Создается автоматически Роботом или Администратором"

    iid = Column(Integer, primary_key=True, autoincrement=True)
    iid_user = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    iid_executor = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)

    # Связи
    creator = relationship("PortalUser", foreign_keys=[iid_user], back_populates="tasks_created")
    executor = relationship("PortalUser", foreign_keys=[iid_executor], back_populates="tasks_executed")


# Модель: workgroup (рабочая группа)
class Workgroup(Base):
    __tablename__ = "workgroup"
    __doc__ = "Рабочая группа, которая содержит множество исполнителей"

    iid = Column(Integer, primary_key=True, autoincrement=True)
    short_title = Column(Text, nullable=False)
    long_title = Column(Text, nullable=True)
    location = Column(Text, nullable=False)
    iid_manager = Column(Integer, ForeignKey("portal_user.iid"), nullable=False)

    # Связи
    manager = relationship("PortalUser", foreign_keys=[iid_manager], back_populates="managed_workgroups")
    users = relationship("UserToWorkgroup", back_populates="workgroup")
    products = relationship("WorkgroupToProduct", back_populates="workgroup")
    manager_role = relationship("UserRole", back_populates="workgroups")


# Модель связи: alteration_to_product
class AlterationToProduct(Base):
    __tablename__ = "alteration_to_product"
    __doc__ = "В продукте может быть много изменений"

    iid_product = Column(Integer, ForeignKey("product.iid"), primary_key=True)
    iid_alteration = Column(Integer, ForeignKey("alteration.iid"), primary_key=True)

    # Связи
    product = relationship("Product", back_populates="alterations")
    alteration = relationship("Alteration", back_populates="products")


# Модель связи: incident_to_appeal
class IncidentToAppeal(Base):
    __tablename__ = "incident_to_appeal"
    __doc__ = "Множество инцидентов в одном обращении"

    iid_appeal = Column(Integer, ForeignKey("appeal.iid"), primary_key=True)
    iid_incident = Column(Integer, ForeignKey("incident.iid"), primary_key=True)

    # Связи
    appeal = relationship("Appeal", back_populates="incidents")
    incident = relationship("Incident", back_populates="appeals")


# Модель связи: user_to_workgroup
class UserToWorkgroup(Base):
    __tablename__ = "user_to_workgroup"
    __doc__ = "В рабочей группе много исполнителей"

    iid_workgroup = Column(Integer, ForeignKey("workgroup.iid"), primary_key=True)
    iid_user = Column(Integer, ForeignKey("portal_user.iid"), primary_key=True)

    # Связи
    workgroup = relationship("Workgroup", back_populates="users")
    user = relationship("PortalUser", back_populates="workgroups")


# Модель связи: workgroup_to_product
class WorkgroupToProduct(Base):
    __tablename__ = "workgroup_to_product"
    __doc__ = "Несколько рабочих групп в продукте"

    iid_workgroup = Column(Integer, ForeignKey("workgroup.iid"), primary_key=True)
    iid_product = Column(Integer, ForeignKey("product.iid"), primary_key=True)

    # Связи
    workgroup = relationship("Workgroup", back_populates="products")
    product = relationship("Product", back_populates="workgroups")
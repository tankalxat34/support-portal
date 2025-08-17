from pydantic import BaseModel
from typing import Any, List, Optional

# —————————————————————————————
# 1. user_role
# —————————————————————————————
class UserRoleBase(BaseModel):
    """Роли пользователей портала"""
    iid: int
    title: str
    create_incident: Optional[bool] = None
    direct_incident: Optional[bool] = None
    create_alteration: Optional[bool] = None
    create_task: bool = False
    create_order: bool = False
    create_appeal: bool = True

class UserRoleCreate(BaseModel):
    iid: int
    title: str
    create_incident: Optional[bool] = None
    direct_incident: Optional[bool] = None
    create_alteration: Optional[bool] = None
    create_task: bool = False
    create_order: bool = False
    create_appeal: bool = True

class UserRoleUpdate(BaseModel):
    title: Optional[str] = None
    create_incident: Optional[bool] = None
    direct_incident: Optional[bool] = None
    create_alteration: Optional[bool] = None
    create_task: Optional[bool] = None
    create_order: Optional[bool] = None
    create_appeal: Optional[bool] = None

class UserRoleSchema(UserRoleBase):
    class Config:
        from_attributes = True


# —————————————————————————————
# 2. portal_user
# —————————————————————————————
class PortalUserBase(BaseModel):
    """Пользователи портала"""
    ad_login: str
    ad_name: str
    ad_email: str
    additional_email: Optional[str] = None
    mobile_phone: str
    portal_role: int = 1

class PortalUserCreate(PortalUserBase):
    pass

class PortalUserUpdate(BaseModel):
    ad_name: Optional[str] = None
    additional_email: Optional[str] = None
    mobile_phone: Optional[str] = None
    portal_role: Optional[int] = None

class PortalUserSchema(PortalUserBase):
    iid: int
    role: Optional[UserRoleSchema] = None  # связь
    workroups: List[Any] = None
    appeals: List[Any] = None

    class Config:
        from_attributes = True


# —————————————————————————————
# 3. alteration (изменение)
# —————————————————————————————
class AlterationBase(BaseModel):
    """Изменение: может быть создано только разработчиком в рамках существующего Продукта"""
    title: str
    description: str
    iid_user: int
    iid_executor: int

class AlterationCreate(AlterationBase):
    pass

class AlterationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    iid_executor: Optional[int] = None

class AlterationSchema(AlterationBase):
    iid: int
    creator: Optional[PortalUserSchema] = None
    executor: Optional[PortalUserSchema] = None
    products: List["ProductSchema"] = []  # через связь alteration_to_product

    class Config:
        from_attributes = True


# —————————————————————————————
# 4. appeal (обращение)
# —————————————————————————————
class AppealBase(BaseModel):
    """Обращение"""
    title: str
    description: str
    iid_user: int = -1
    iid_executor: int

class AppealCreate(AppealBase):
    pass

class AppealUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    iid_executor: Optional[int] = None

class AppealSchema(AppealBase):
    iid: int
    creator: Optional[PortalUserSchema] = None
    executor: Optional[PortalUserSchema] = None
    incidents: List["IncidentSchema"] = []

    class Config:
        from_attributes = True


# —————————————————————————————
# 5. incident (инцидент)
# —————————————————————————————
class IncidentBase(BaseModel):
    """Инцидент"""
    title: str
    description: str

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class IncidentSchema(IncidentBase):
    iid: int
    appeals: List[AppealSchema] = []

    class Config:
        from_attributes = True


# —————————————————————————————
# 6. order
# —————————————————————————————
class OrderBase(BaseModel):
    """Заказ: специально для кадровых или иных служб..."""
    title: str
    description: str
    iid_user: int
    iid_executor: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    iid_executor: Optional[int] = None

class OrderSchema(OrderBase):
    iid: int
    creator: Optional[PortalUserSchema] = None
    executor: Optional[PortalUserSchema] = None

    class Config:
        from_attributes = True


# —————————————————————————————
# 7. product
# —————————————————————————————
class ProductBase(BaseModel):
    """Продукт: информация по продукту. В рамках него могут создаваться изменения..."""
    short_title: str
    long_title: Optional[str] = None
    iid_manager: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    short_title: Optional[str] = None
    long_title: Optional[str] = None
    iid_manager: Optional[int] = None

class ProductSchema(ProductBase):
    iid: int
    manager: Optional[PortalUserSchema] = None
    alterations: List[AlterationSchema] = []
    workgroups: List["WorkgroupSchema"] = []

    class Config:
        from_attributes = True


# —————————————————————————————
# 8. task
# —————————————————————————————
class TaskBase(BaseModel):
    """Задача: вариант инцидента, не требующий получения обратной связи..."""
    title: str
    description: str
    iid_user: int
    iid_executor: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    iid_executor: Optional[int] = None

class TaskSchema(TaskBase):
    iid: int
    creator: Optional[PortalUserSchema] = None
    executor: Optional[PortalUserSchema] = None

    class Config:
        from_attributes = True


# —————————————————————————————
# 9. workgroup
# —————————————————————————————
class WorkgroupBase(BaseModel):
    """Рабочая группа, которая содержит множество исполнителей"""
    short_title: str
    long_title: Optional[str] = None
    location: str
    iid_manager: int

class WorkgroupCreate(WorkgroupBase):
    pass

class WorkgroupUpdate(BaseModel):
    short_title: Optional[str] = None
    long_title: Optional[str] = None
    location: Optional[str] = None
    iid_manager: Optional[int] = None

class WorkgroupSchema(WorkgroupBase):
    iid: int
    manager: Optional[PortalUserSchema] = None
    users: List[PortalUserSchema] = []
    products: List[ProductSchema] = []

    class Config:
        from_attributes = True


# —————————————————————————————
# 10. Связующие таблицы (Many-to-Many)
# —————————————————————————————

# alteration_to_product
class AlterationToProductBase(BaseModel):
    iid_product: int
    iid_alteration: int

class AlterationToProductCreate(AlterationToProductBase):
    pass

class AlterationToProductSchema(AlterationToProductBase):
    product: Optional[ProductSchema] = None
    alteration: Optional[AlterationSchema] = None

    class Config:
        from_attributes = True


# incident_to_appeal
class IncidentToAppealBase(BaseModel):
    iid_appeal: int
    iid_incident: int

class IncidentToAppealCreate(IncidentToAppealBase):
    pass

class IncidentToAppealSchema(IncidentToAppealBase):
    appeal: Optional[AppealSchema] = None
    incident: Optional[IncidentSchema] = None

    class Config:
        from_attributes = True


# user_to_workgroup
class UserToWorkgroupBase(BaseModel):
    iid_workgroup: int
    iid_user: int

class UserToWorkgroupCreate(UserToWorkgroupBase):
    pass

class UserToWorkgroupSchema(UserToWorkgroupBase):
    user: Optional[PortalUserSchema] = None
    workgroup: Optional[WorkgroupSchema] = None

    class Config:
        from_attributes = True


# workgroup_to_product
class WorkgroupToProductBase(BaseModel):
    iid_workgroup: int
    iid_product: int

class WorkgroupToProductCreate(WorkgroupToProductBase):
    pass

class WorkgroupToProductSchema(WorkgroupToProductBase):
    workgroup: Optional[WorkgroupSchema] = None
    product: Optional[ProductSchema] = None

    class Config:
        from_attributes = True
from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, EmailStr
from fastapi_users import schemas

class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


# Create plan schema
class PlanCreate(BaseModel):
    name: str
    credits_monthly: int
    credits_anual: int


# Create subscription
class SubscriptionCreate(BaseModel):
    user_id: int
    plan_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

# Create available credits
class AvailableCreditsCreate(BaseModel):
    user_id: int
    plan_id: int
    credits_available: int

#Plan read
class PlanRead(BaseModel):
    id: int
    name: str
    credits_monthly: int
    credits_anual: int

#Subscription read
class SubscriptionRead(BaseModel):
    id: int
    user_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime
    tipo: str

# Available credits read
class AvailableCreditsRead(BaseModel):
    id: int
    user_id: int
    plan_id: int
    credits_available: int

class UserRead(schemas.BaseUser[uuid.UUID]):
    subscriptions: List[SubscriptionRead]
    credits: List[AvailableCreditsRead]

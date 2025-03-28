from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BaseLead(BaseModel):
    id: int
    time: datetime
    phone: str
    wechat: str
    remark: Optional[str] = None
    intention_level: int
    is_read: bool = False
    assigned_user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class LeadCreate(BaseModel):
    time: datetime
    phone: str
    wechat: str
    remark: Optional[str] = None
    intention_level: int = Field(ge=1, le=5)
    assigned_user_id: int


class LeadUpdate(BaseModel):
    id: int
    time: Optional[datetime] = None
    phone: Optional[str] = None
    wechat: Optional[str] = None
    remark: Optional[str] = None
    intention_level: Optional[int] = Field(None, ge=1, le=5)
    is_read: Optional[bool] = None
    assigned_user_id: Optional[int] = None


class LeadBatchCreate(BaseModel):
    leads: List[LeadCreate]


class LeadBatchAssign(BaseModel):
    lead_ids: List[int]
    assigned_user_id: int 
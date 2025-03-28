from typing import List, Optional

from fastapi.exceptions import HTTPException
from tortoise.expressions import Q

from app.core.crud import CRUDBase
from app.models.admin import Lead
from app.schemas.leads import LeadCreate, LeadUpdate, LeadBatchCreate, LeadBatchAssign

from .user import user_controller


class LeadController(CRUDBase[Lead, LeadCreate, LeadUpdate]):
    def __init__(self):
        super().__init__(model=Lead)

    async def get_by_user(self, user_id: int, page: int = 1, page_size: int = 10) -> tuple[int, List[Lead]]:
        total = await self.model.filter(assigned_user_id=user_id).count()
        leads = await self.model.filter(assigned_user_id=user_id).offset((page - 1) * page_size).limit(page_size)
        return total, leads

    async def batch_create(self, leads_in: LeadBatchCreate) -> List[Lead]:
        leads = []
        for lead_in in leads_in.leads:
            lead = await self.create(lead_in)
            leads.append(lead)
        return leads

    async def batch_assign(self, assign_in: LeadBatchAssign) -> None:
        # 验证用户是否存在
        user = await user_controller.get(id=assign_in.assigned_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 批量更新分配用户
        await self.model.filter(id__in=assign_in.lead_ids).update(assigned_user_id=assign_in.assigned_user_id)

    async def mark_as_read(self, lead_id: int) -> None:
        await self.model.filter(id=lead_id).update(is_read=True)

    async def mark_as_unread(self, lead_id: int) -> None:
        await self.model.filter(id=lead_id).update(is_read=False)


lead_controller = LeadController() 
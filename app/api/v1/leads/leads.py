from fastapi import APIRouter, Body, Query, Depends
from tortoise.expressions import Q

from app.controllers.lead import lead_controller
from app.controllers.user import user_controller
from app.core.security import get_current_user
from app.models.admin import User
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.leads import LeadCreate, LeadUpdate, LeadBatchCreate, LeadBatchAssign

router = APIRouter()


@router.get("/list", summary="查看线索列表")
async def list_leads(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    phone: str = Query("", description="号码，用于搜索"),
    wechat: str = Query("", description="微信，用于搜索"),
    is_read: bool = Query(None, description="是否已读"),
    assigned_user_id: int = Query(None, description="分配用户ID"),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        return Fail(msg="只有超级管理员可以访问此接口")
        
    q = Q()
    if phone:
        q &= Q(phone__contains=phone)
    if wechat:
        q &= Q(wechat__contains=wechat)
    if is_read is not None:
        q &= Q(is_read=is_read)
    if assigned_user_id:
        q &= Q(assigned_user_id=assigned_user_id)

    total, lead_objs = await lead_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in lead_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/my", summary="查看我的线索")
async def list_my_leads(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    phone: str = Query("", description="号码，用于搜索"),
    wechat: str = Query("", description="微信，用于搜索"),
    is_read: bool = Query(None, description="是否已读"),
    current_user: User = Depends(get_current_user),
):
    q = Q(assigned_user_id=current_user.id)
    if phone:
        q &= Q(phone__contains=phone)
    if wechat:
        q &= Q(wechat__contains=wechat)
    if is_read is not None:
        q &= Q(is_read=is_read)

    total, lead_objs = await lead_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in lead_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.post("/create", summary="创建线索")
async def create_lead(
    lead_in: LeadCreate,
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        return Fail(msg="只有超级管理员可以创建线索")
    new_lead = await lead_controller.create(obj_in=lead_in)
    return Success(msg="Created Successfully")


@router.post("/batch_create", summary="批量创建线索")
async def batch_create_leads(
    leads_in: LeadBatchCreate,
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        return Fail(msg="只有超级管理员可以批量创建线索")
    await lead_controller.batch_create(leads_in)
    return Success(msg="Created Successfully")


@router.post("/batch_assign", summary="批量分配线索")
async def batch_assign_leads(
    assign_in: LeadBatchAssign,
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        return Fail(msg="只有超级管理员可以分配线索")
    await lead_controller.batch_assign(assign_in)
    return Success(msg="Assigned Successfully")


@router.post("/update", summary="更新线索")
async def update_lead(
    lead_in: LeadUpdate,
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        return Fail(msg="只有超级管理员可以更新线索")
    await lead_controller.update(id=lead_in.id, obj_in=lead_in)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="删除线索")
async def delete_lead(
    lead_id: int = Query(..., description="线索ID"),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        return Fail(msg="只有超级管理员可以删除线索")
    await lead_controller.remove(id=lead_id)
    return Success(msg="Deleted Successfully")


@router.post("/mark_read", summary="标记为已读")
async def mark_as_read(
    lead_id: int = Body(..., description="线索ID", embed=True),
    current_user: User = Depends(get_current_user),
):
    lead = await lead_controller.get(id=lead_id)
    if not lead:
        return Fail(msg="线索不存在")
    if lead.assigned_user_id != current_user.id and not current_user.is_superuser:
        return Fail(msg="无权操作此线索")
    await lead_controller.mark_as_read(lead_id)
    return Success(msg="Marked as read")


@router.post("/mark_unread", summary="标记为未读")
async def mark_as_unread(
    lead_id: int = Body(..., description="线索ID", embed=True),
    current_user: User = Depends(get_current_user),
):
    lead = await lead_controller.get(id=lead_id)
    if not lead:
        return Fail(msg="线索不存在")
    if lead.assigned_user_id != current_user.id and not current_user.is_superuser:
        return Fail(msg="无权操作此线索")
    await lead_controller.mark_as_unread(lead_id)
    return Success(msg="Marked as unread") 
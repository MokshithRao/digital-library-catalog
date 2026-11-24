from fastapi import APIRouter, Request, Depends
from typing import Annotated
from auth_dependencies import require_admin
from models import User
from template_config import templates

router = APIRouter(prefix="/admin")


@router.get("/", name="Admin_dashboard")
def admin_dashboard(
    request: Request,
    current_user: Annotated[User, Depends(require_admin)]
):
    return templates.TemplateResponse(
        name="admin/dashboard.html",
        request=request,
        context={"current_user": current_user}
    )
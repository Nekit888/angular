from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, Request

from application.auth.admin_auth_service import (
    admin_sign_in,
    admin_sign_out,
)
from .admin_auth_deps import require_admin
from .admin_auth_schemas import AdminSignInIn

router = APIRouter(prefix="/admins", tags=["admins.auth"])


@router.post("/admin_sign_in")
def route_admin_sign_in(data: AdminSignInIn, response: Response, request: Request):
    result = admin_sign_in(data.admin_login, data.admin_password)
    if not result:
        raise HTTPException(status_code=401, detail="invalid credentials")

    admin, admin_session_id = result

    origin = (request.headers.get("origin") or "").lower()
    is_local = (
        origin.startswith("http://localhost")
        or origin.startswith("http://127.0.0.1")
        or "://192.168." in origin
        or "://10." in origin
        or "://172." in origin
    )

    cookie_kwargs = {
        "key": "admin_session_id",
        "value": admin_session_id,
        "httponly": True,
        "secure": True,
        "path": "/",
    }

    if is_local:
        cookie_kwargs["samesite"] = "none"
    else:
        cookie_kwargs["samesite"] = "lax"

    response.set_cookie(**cookie_kwargs)

    return {"ok": True, "admin": admin}


@router.get("/get_current_admin")
def route_get_current_admin(admin: dict = Depends(require_admin)):
    return {"ok": True, "admin": admin}


@router.post("/admin_sign_out")
def route_admin_sign_out(
    response: Response,
    request: Request,
    admin_session_id: str | None = Cookie(default=None, alias="admin_session_id"),
    _admin: dict = Depends(require_admin),
):
    if admin_session_id:
        admin_sign_out(admin_session_id)

    origin = (request.headers.get("origin") or "").lower()
    is_local = (
        origin.startswith("http://localhost")
        or origin.startswith("http://127.0.0.1")
        or "://192.168." in origin
        or "://10." in origin
        or "://172." in origin
    )

    delete_kwargs = {
        "key": "admin_session_id",
        "path": "/",
    }

    if not is_local:
        delete_kwargs["domain"] = ".primer.com"

    response.delete_cookie(**delete_kwargs)
    return {"ok": True}
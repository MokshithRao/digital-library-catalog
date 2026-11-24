from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from typing import Annotated
from sqlalchemy.orm import Session
import secrets
import hashlib
from datetime import datetime, timedelta

from template_config import templates
from dependencies import get_db
from models import User, UserSession
from security import hash_password, verify_password
from validators import validate_username, validate_email_address, validate_password
from auth_dependencies import get_current_user


router = APIRouter()



@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        name="register.html",
        request=request
    )



@router.post("/register")
def register_user(
    request: Request,
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Annotated[Session, Depends(get_db)]
):

    # Validate registration details on the server.
    try:
        username = validate_username(username)
        email = validate_email_address(email)
        validate_password(password)

    except ValueError as error:
        return templates.TemplateResponse(
            name="register.html",
            request=request,
            context={"error": str(error)},
            status_code=400
        )
    
    # Check whether the email is already registered.
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        return templates.TemplateResponse(
            name="register.html",
            request=request,
            context={"error": "Email is already registered."},
            status_code=400
        )

    # Create a new user with a securely hashed password.
    new_user = User(
        username=username,
        email=email.lower(),
        password_hash=hash_password(password)
    )

    db.add(new_user)
    db.commit()

    return templates.TemplateResponse(
        name="register.html",
        request=request,
        context={"success": "Registration successful! You can now log in."}
    )



@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        request=request
    )



@router.post("/login")
def login_user(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Annotated[Session, Depends(get_db)]
):
    # Find the registered user by email.
    user = db.query(User).filter(User.email == email.strip().lower()).first()

    # Verify the password and account status.
    if not user or not verify_password(password, user.password_hash) or not user.is_active:
        return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={"error": "Invalid email or password."},
            status_code=401
        )

    # Generate a secure session token and store only its hash.
    session_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(session_token.encode()).hexdigest()

    expires_at = datetime.utcnow() + timedelta(days=7)

    user_session = UserSession(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )

    db.add(user_session)
    db.commit()


    # Redirect to the home page and store the session token in an HTTP-only cookie.
    response = RedirectResponse(url="/", status_code=303)

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/"
    )

    return response




@router.post("/logout")
def logout_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Find and revoke the current user's session.
    session_token = request.cookies.get("session_token")
    token_hash = hashlib.sha256(session_token.encode()).hexdigest()

    user_session = db.query(UserSession).filter(
        UserSession.token_hash == token_hash
    ).first()


    if user_session:
        user_session.revoked_at = datetime.utcnow()
        db.commit()


    # Clear the session cookie and redirect to the login page.
    response = RedirectResponse(
        url="/login", status_code=303
    )

    response.delete_cookie(key="session_token", path="/")

    return response

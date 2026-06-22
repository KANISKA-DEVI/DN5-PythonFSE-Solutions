from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security       import OAuth2PasswordBearer
from sqlalchemy.orm         import Session
from jose                   import JWTError

from database import User, get_db
from schemas  import UserRegister, UserLogin, TokenResponse
from security import get_password_hash, verify_password, create_access_token, decode_access_token

app = FastAPI(title="Auth API", version="1.0.0")

# ---- CORS Configuration ----
# Allows the frontend at localhost:3000 to call this API
# CORS is enforced by the BROWSER, not the server
# Server-to-server calls ignore CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["http://localhost:3000"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


# ---- Dependency: get current user from JWT ----
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail      = "Invalid or expired token",
        headers     = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# ---- Register ----
@app.post("/api/v1/auth/register/", status_code=201, tags=["Auth"])
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if email already registered
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Hash the password — NEVER store plain text
    hashed = get_password_hash(user_data.password)

    user = User(email=user_data.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully", "email": user.email, "id": user.id}


# ---- Login ----
@app.post("/api/v1/auth/login/", response_model=TokenResponse, tags=["Auth"])
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Incorrect email or password"
        )

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


# ---- Protected Routes ----

@app.get("/api/v1/courses/", tags=["Courses — Public"])
def list_courses():
    """This endpoint is PUBLIC — no auth required."""
    return [{"id": 1, "name": "Data Structures"}, {"id": 2, "name": "DBMS"}]


@app.post("/api/v1/courses/", tags=["Courses — Protected"])
def create_course(current_user: User = Depends(get_current_user)):
    """This endpoint is PROTECTED — requires a valid JWT token."""
    return {"message": f"Course created by {current_user.email}"}


@app.delete("/api/v1/courses/{course_id}", tags=["Courses — Protected"])
def delete_course(course_id: int, current_user: User = Depends(get_current_user)):
    """Protected endpoint — returns 401 without a valid token."""
    return {"message": f"Course {course_id} deleted by {current_user.email}"}


# ---- OAuth2 Explanation (in comments) ----
# OAuth2 Authorization Code Flow (concept):
# 1. User clicks "Login with Google"
# 2. Browser redirects to Google's auth server with client_id and redirect_uri
# 3. User logs in on Google and grants permission
# 4. Google redirects back with an authorization CODE
# 5. Our server exchanges the CODE for an access token (server-to-server)
# 6. We use the access token to call Google APIs on behalf of the user
#
# How it differs from our simple JWT login:
# - Our login: user sends credentials directly to OUR server → we issue a JWT
# - OAuth2: user authenticates with a THIRD-PARTY (Google, GitHub) → they issue a token
# - OAuth2 is for DELEGATED access. Our JWT is for direct authentication.
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas, auth, dependencies
from app.database import get_db, engine
from app.redis_client import add_to_blacklist
from datetime import datetime, timedelta
import uuid

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", version="1.0.0")

@app.post("/register", response_model=schemas.Token)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    # 检查邮箱是否已存在
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 创建新用户
    hashed_password = auth.get_password_hash(user_data.password)
    user = models.User(email=user_data.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 生成令牌
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    refresh_token = auth.create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/login", response_model=schemas.Token)
def login(
    user_data: schemas.UserLogin, 
    request: Request,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not auth.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # 记录登录历史
    user_agent = request.headers.get("user-agent", "")
    login_history = models.LoginHistory(
        user_id=user.id,
        user_agent=user_agent
    )
    db.add(login_history)
    db.commit()
    
    # 生成令牌
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    refresh_token = auth.create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh", response_model=schemas.Token)
def refresh_token(token_data: schemas.TokenRefresh):
    payload = auth.verify_token(token_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # 生成新的访问令牌
    access_token = auth.create_access_token(data={"sub": user_id})
    refresh_token = auth.create_refresh_token(data={"sub": user_id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.put("/user/update")
def update_user(
    user_data: schemas.UserUpdate,
    current_user: models.User = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    update_data = {}
    
    if user_data.email is not None:
        # 检查新邮箱是否已被使用
        existing_user = db.query(models.User).filter(
            models.User.email == user_data.email,
            models.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        update_data["email"] = user_data.email
    
    if user_data.password is not None:
        update_data["hashed_password"] = auth.get_password_hash(user_data.password)
    
    if update_data:
        db.query(models.User).filter(models.User.id == current_user.id).update(update_data)
        db.commit()
    
    return {"message": "User updated successfully"}

@app.get("/user/history", response_model=list[schemas.LoginHistoryResponse])
def get_login_history(
    current_user: models.User = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(models.LoginHistory).filter(
        models.LoginHistory.user_id == current_user.id
    ).order_by(models.LoginHistory.login_datetime.desc()).all()
    
    return history

@app.post("/logout")
def logout(
    credentials: dependencies.HTTPAuthorizationCredentials = Depends(dependencies.security)
):
    token = credentials.credentials
    payload = auth.verify_token(token)
    
    if payload:
        # 计算令牌剩余过期时间
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            expire_time = datetime.fromtimestamp(exp_timestamp) - datetime.utcnow()
            expire_seconds = max(int(expire_time.total_seconds()), 1)
            
            # 将令牌加入黑名单
            add_to_blacklist(token, expire_seconds)
    
    return {"message": "Successfully logged out"}
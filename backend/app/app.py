from fastapi import Depends, FastAPI, status, HTTPException
from datetime import datetime, timedelta
from app.db import User, create_db_and_tables, get_db
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserRead, UserUpdate, PlanCreate, PlanRead, SubscriptionRead, SubscriptionCreate
from app.db import Plan, Subscription
from app.users import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)

@app.post('/subs', response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(sub: SubscriptionCreate, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_db)):
    query = select(Subscription).where(Subscription.user_id == sub.user_id)
    exist_subcription_user = (await db.execute(query)).scalar_one_or_none()
    subcription_user = Subscription(sub.user_id, sub.plan_id, sub.start_date, sub.end_date)
    if exist_subcription_user:
        exist_subcription_user = subcription_user
        db.add(exist_subcription_user)
    else:
        db.add(subcription_user)
    
    await db.commit()
    await db.refresh()
    return subcription_user
    

@app.get('/plans', status_code=status.HTTP_200_OK)
async def get_plans(user: User = Depends(current_active_user), db: AsyncSession = Depends(get_db)):
    query = select(Plan)
    plans = await db.execute(query)
    await db.commit()
    return plans.scalar()

@app.post("/plans", response_model=PlanRead, status_code=status.HTTP_201_CREATED)
async def create_plan(plan: PlanCreate, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_db)):
    query = select(Plan).where(Plan.name == plan.name)
    existing_plan = (await db.execute(query)).scalar_one_or_none()
    if existing_plan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The plan name alredy exist")

    db_plan = Plan(name = plan.name, credits_monthly=plan.credits_monthly, credits_anual=plan.credits_anual)
    db.add(db_plan)
    await db.commit()
    await db.refresh(db_plan)
    return db_plan

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()

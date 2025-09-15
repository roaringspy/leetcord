# main.py
from fastapi import FastAPI, HTTPException, Body, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import httpx
import os
from fastapi.middleware.cors import CORSMiddleware

from database import problems_collection, submissions_collection, users_collection
from models import Problem, SubmissionCreate, SubmissionInDB, Token, UserCreate, UserPublic, UserInDB
import leetcode_service
import auth

DISCORD_BOT_URL = os.getenv("DISCORD_BOT_URL")

app = FastAPI()

origins = [
    # For development, allowing all origins is the easiest.
    # For production, you would list your specific extension's origin.
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
# --- Helper Functions (no changes) ---
async def notify_discord_of_submission(username: str, problem: Problem, score: int):
    if not DISCORD_BOT_URL:
        print("DISCORD_BOT_URL not set. Skipping notification.")
        return

    payload = {
        "username": username,
        "problem_title": problem.title,
        "problem_difficulty": problem.difficulty,
        "problem_url": f"https://leetcode.com/problems/{problem.title_slug}/",
        "score": score
    }
    
    async with httpx.AsyncClient() as client:
        try:
            await client.post(f"{DISCORD_BOT_URL}/events/new-submission", json=payload, timeout=5)
        except httpx.RequestError as e:
            # Log the error, but don't fail the main request
            print(f"Failed to notify Discord: {e}")

def calculate_score(difficulty: str) -> int:
    if difficulty == "Easy": return 10
    elif difficulty == "Medium": return 25
    elif difficulty == "Hard": return 50
    return 0

async def get_problem_from_cache_or_api(problem_slug: str) -> Problem:
    problem_doc = await problems_collection.find_one({"title_slug": problem_slug})
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    if not problem_doc or problem_doc["last_updated"] < one_week_ago:
        fresh_data = await leetcode_service.get_problem_details(problem_slug)
        if not fresh_data: raise HTTPException(status_code=404, detail=f"Problem '{problem_slug}' not found.")
        fresh_data["last_updated"] = datetime.utcnow()
        await problems_collection.update_one({"title_slug": problem_slug}, {"$set": fresh_data}, upsert=True)
        problem_doc = await problems_collection.find_one({"title_slug": problem_slug})
    return Problem(**problem_doc)

# --- API Endpoints ---

# No changes to this endpoint
@app.get("/api/v1/problems/{problem_slug}", response_model=Problem)
async def get_problem(problem_slug: str):
    return await get_problem_from_cache_or_api(problem_slug)

# --- CORRECTED AUTH ENDPOINTS ---

@app.post("/api/v1/auth/register", response_model=UserPublic)
async def register_user(user_data: UserCreate = Body(...)):
    db_user = await users_collection.find_one({"username": user_data.username})
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(user_data.password)
    
    # Create a UserInDB object, which does NOT contain the plain password
    user_in_db = UserInDB(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    # Insert the correct object into the database
    result = await users_collection.insert_one(user_in_db.dict(by_alias=True, exclude=["id"]))
    
    # Return the newly created user's public data
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    return created_user

# No changes to this endpoint
@app.post("/api/v1/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_doc = await users_collection.find_one({"username": form_data.username})
    if not user_doc or not auth.verify_password(form_data.password, user_doc["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user_doc["username"]}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- UPDATED SUBMISSIONS ENDPOINT ---

@app.post("/api/v1/submissions", response_model=SubmissionInDB)
async def create_submission(
    background_tasks: BackgroundTasks, # Add this parameter
    submission: SubmissionCreate = Body(...),
    current_user: UserInDB = Depends(auth.get_current_user)
):
    problem = await get_problem_from_cache_or_api(submission.problem_slug)
    score = calculate_score(problem.difficulty)
    
    new_submission = SubmissionInDB(
        user_id=str(current_user.id),
        problem_id=problem.id,
        contest_id=submission.contest_id,
        score=score
    )
    
    result = await submissions_collection.insert_one(new_submission.dict(by_alias=True, exclude=["id"]))
    created_doc = await submissions_collection.find_one({"_id": result.inserted_id})
    
    # Add the notification task to run in the background
    background_tasks.add_task(
        notify_discord_of_submission,
        username=current_user.username,
        problem=problem,
        score=score
    )
    
    return created_doc
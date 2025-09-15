# models.py
from pydantic import BaseModel, Field, EmailStr
from pydantic_core import core_schema
from datetime import datetime
from typing import Any, Optional
from bson import ObjectId

# This helper class is correct, no changes needed here.
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        def validate(v: Any) -> ObjectId:
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)
        return core_schema.union_schema(
            [core_schema.is_instance_schema(ObjectId), core_schema.no_info_plain_validator_function(validate)],
            serialization=core_schema.to_string_ser_schema(),
        )

# --- Problem Model (no change) ---
class Problem(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title_slug: str
    title: str
    difficulty: str
    acceptance_rate: float
    last_updated: datetime
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# --- NEW, CORRECTED AUTH MODELS ---

class Token(BaseModel):
    access_token: str
    token_type: str

# Model for the request body when creating a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Model for the public response (what we send back to the client)
class UserPublic(BaseModel):
    id: PyObjectId = Field(alias="_id")
    username: str
    email: EmailStr
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Model for what's stored in the database
class UserInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: EmailStr
    hashed_password: str
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# --- Submission Models (no change) ---
class SubmissionCreate(BaseModel):
    problem_slug: str
    contest_id: str

class SubmissionInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    problem_id: PyObjectId
    contest_id: str
    score: int
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
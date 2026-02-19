from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

# --- Pydantic Schemas for Validation ---

class AuthorSchema(BaseModel):
    name: str
    role: str = "farmer"
    profilePicture: Optional[str] = None

class CommentSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author: str
    content: str
    createdAt: datetime = Field(default_factory=datetime.now)
    isAnswer: bool = False

class PostCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=10)
    type: str = Field(..., pattern="^(question|discussion|tip|problem|success_story)$")
    category: str
    language: str = "en"
    tags: List[str] = []

class PostResponse(PostCreate):
    id: str
    author: AuthorSchema
    views: int = 0
    reactionCount: int = 0
    commentCount: int = 0
    comments: List[CommentSchema] = []
    createdAt: datetime
    isResolved: bool = False

# --- Mock Database ---
# In a real app, this would be replaced by MongoDB or PostgreSQL logic
db_posts: List[dict] = []

# --- Endpoints ---

@router.get("/feed", response_model=List[PostResponse])
async def get_community_feed(
    category: Optional[str] = None,
    limit: int = Query(20, gt=0, le=100)
):
    """
    Retrieves the community feed with optional category filtering.
    """
    if category and category != "all":
        filtered_posts = [p for p in db_posts if p["category"] == category]
        return filtered_posts[-limit:]
    
    return db_posts[-limit:]

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_community_post(post_data: PostCreate):
    """
    Creates a new community post with validated data.
    """
    new_post = {
        "id": str(uuid.uuid4()),
        "author": {
            "name": "Medhansh Reddy", # Mocked current user
            "role": "farmer",
            "profilePicture": None
        },
        **post_data.model_dump(),
        "views": 0,
        "reactionCount": 0,
        "commentCount": 0,
        "comments": [],
        "createdAt": datetime.now(),
        "isResolved": False
    }
    
    db_posts.insert(0, new_post) # Add to the top of the feed
    return new_post

@router.post("/react/{post_id}", status_code=status.HTTP_200_OK)
async def react_to_post(post_id: str, type: str = "like"):
    """
    Increments the reaction count for a specific post.
    """
    for post in db_posts:
        if post["id"] == post_id:
            post["reactionCount"] += 1
            return {"success": True, "new_count": post["reactionCount"]}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with id {post_id} not found"
    )

@router.get("/trending", response_model=dict)
async def get_trending_tags():
    """
    Returns simulated trending tags for the sidebar.
    """
    return {
        "tags": [
            {"_id": "chilli", "count": 42},
            {"_id": "gadwal", "count": 28},
            {"_id": "organic", "count": 15}
        ]
    }

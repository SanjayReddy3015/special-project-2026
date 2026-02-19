from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

# Helper class to handle MongoDB's ObjectId in Pydantic
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

# --- Sub-Models ---

class AuthorModel(BaseModel):
    id: str
    name: str
    role: str = "farmer"  # e.g., "farmer", "expert", "admin"
    profile_pic: Optional[str] = None

class CommentModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author: AuthorModel
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    likes: int = 0
    is_expert_answer: bool = False

# --- Main Models ---

class CommunityPost(BaseModel):
    """
    Represents a discussion or question in the WikiKisan community.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(..., min_length=5, max_length=150)
    content: str
    post_type: str = Field(..., pattern="^(question|discussion|tip|success_story)$")
    category: str = Field(..., pattern="^(crops|livestock|market|weather|general)$")
    tags: List[str] = []
    
    author: AuthorModel
    comments: List[CommentModel] = []
    
    views: int = 0
    reaction_count: int = 0
    is_resolved: bool = False
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Best fertilizer for Gadwal Chilli?",
                "content": "I am looking for organic recommendations for my red chilli farm...",
                "post_type": "question",
                "category": "crops",
                "tags": ["chilli", "organic", "gadwal"]
            }
        }
    )

class CommunityGroup(BaseModel):
    """
    Represents a specialized group (e.g., 'Telangana Paddy Farmers').
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., unique=True)
    description: str
    category: str
    avatar_url: Optional[str] = None
    
    member_count: int = 0
    is_private: bool = False
    
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(populate_by_name=True)

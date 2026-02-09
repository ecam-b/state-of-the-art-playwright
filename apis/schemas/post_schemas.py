from pydantic import BaseModel, ConfigDict


class PostResponse(BaseModel):
    """Schema for post data from JSONPlaceholder API."""
    
    model_config = ConfigDict(extra="allow")
    
    userId: int
    id: int
    title: str
    body: str


class PostCreateResponse(BaseModel):
    """Schema for post creation response from JSONPlaceholder API."""
    
    model_config = ConfigDict(extra="allow")
    
    id: int
    title: str
    body: str
    userId: int

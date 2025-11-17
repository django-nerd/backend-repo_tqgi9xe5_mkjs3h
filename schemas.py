"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (you can keep or ignore these):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Herbal tea brand specific schemas

class TeaBlend(BaseModel):
    """
    Tea blends collection schema
    Collection name: "teablend"
    """
    name: str = Field(..., description="Blend name, e.g., 'Calm Chamomile'")
    description: Optional[str] = Field(None, description="Short calming description")
    ingredients: List[str] = Field(default_factory=list, description="List of herbs")
    flavor_notes: Optional[str] = Field(None, description="Tasting notes")
    caffeine_free: bool = Field(True, description="Is this caffeine-free?")
    price: float = Field(..., ge=0, description="Price in dollars")
    image: Optional[str] = Field(None, description="Image URL for the blend")
    tags: List[str] = Field(default_factory=list, description="Tags like 'sleep', 'stress', 'digestive'")

class Testimonial(BaseModel):
    """
    Customer testimonials
    Collection name: "testimonial"
    """
    name: str = Field(..., description="Customer first name")
    quote: str = Field(..., description="What they said")
    blend: Optional[str] = Field(None, description="Blend they enjoyed")
    rating: Optional[int] = Field(5, ge=1, le=5, description="Star rating")

class Subscriber(BaseModel):
    """
    Newsletter subscribers
    Collection name: "subscriber"
    """
    email: EmailStr = Field(..., description="Subscriber email")
    name: Optional[str] = Field(None, description="Optional name")
    interests: List[str] = Field(default_factory=list, description="Tags of interest, e.g., ['sleep','stress']")

# Note: The Flames database viewer can read these via GET /schema endpoint.

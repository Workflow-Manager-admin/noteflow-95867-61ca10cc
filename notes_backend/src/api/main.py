from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

# PUBLIC_INTERFACE
class Recipe(BaseModel):
    """Recipe data model"""
    id: str = Field(..., description="Unique ID for the recipe")
    title: str = Field(..., description="Recipe title or name")
    description: Optional[str] = Field("", description="Short description")
    image: str = Field(..., description="Image filename (asset path)")
    meta: Optional[str] = Field("", description="Short metadata (time/kcal/chip)")
    # You could add more fields such as ingredients, steps, etc.

class RecipeCreate(BaseModel):
    """Input model for creating/updating a recipe"""
    title: str = Field(..., description="Recipe title or name")
    description: Optional[str] = Field("", description="Short description")
    image: str = Field(..., description="Image filename (asset path)")
    meta: Optional[str] = Field("", description="Short metadata (time/kcal/chip)")

app = FastAPI(
    title="Noteflow Recipe Backend",
    version="1.0.0",
    description="Backend API for Noteflow Notes & Recipes App. Provides endpoints to manage recipes/notes.",
    openapi_tags=[{"name": "recipes", "description": "Manage recipe cards"}]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory pseudo-database for demonstration (replace with DB later)
recipes_db = [
    Recipe(
        id=str(uuid4()),
        title="Berry Smoothie Bowl",
        description="A vibrant bowl topped with banana, kiwi, and berries.",
        image="berry_smoothie_bowl.jpg",
        meta="10 min • 320 kcal"
    ),
    Recipe(
        id=str(uuid4()),
        title="Vegetarian Pizza",
        description="Wood-fired pizza with assorted vegetables and fresh herbs.",
        image="vegetarian_pizza.jpg",
        meta="25 min • 540 kcal"
    ),
    Recipe(
        id=str(uuid4()),
        title="Salmon Teriyaki Bowl",
        description="Salmon teriyaki served over rice with broccoli.",
        image="salmon_teriyaki.jpg",
        meta="20 min • 470 kcal"
    ),
]

# PUBLIC_INTERFACE
@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get("/recipes", response_model=List[Recipe], tags=["recipes"], summary="List all recipes")
def list_recipes():
    """List all recipe cards"""
    return recipes_db

# PUBLIC_INTERFACE
@app.get("/recipes/{recipe_id}", response_model=Recipe, tags=["recipes"], summary="Retrieve a recipe by ID")
def get_recipe(recipe_id: str):
    """Get details of a recipe"""
    for recipe in recipes_db:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

# PUBLIC_INTERFACE
@app.post("/recipes", response_model=Recipe, tags=["recipes"], summary="Create a new recipe")
def create_recipe(data: RecipeCreate):
    """Create a new recipe"""
    recipe = Recipe(
        id=str(uuid4()),
        title=data.title,
        description=data.description,
        image=data.image,
        meta=data.meta
    )
    recipes_db.append(recipe)
    return recipe

# PUBLIC_INTERFACE
@app.put("/recipes/{recipe_id}", response_model=Recipe, tags=["recipes"], summary="Update a recipe")
def update_recipe(recipe_id: str, data: RecipeCreate):
    """Update an existing recipe"""
    for i, recipe in enumerate(recipes_db):
        if recipe.id == recipe_id:
            updated = recipe.copy(update=data.model_dump())
            recipes_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Recipe not found")

# PUBLIC_INTERFACE
@app.delete("/recipes/{recipe_id}", tags=["recipes"], summary="Delete a recipe")
def delete_recipe(recipe_id: str):
    """Delete a recipe by ID"""
    for i, recipe in enumerate(recipes_db):
        if recipe.id == recipe_id:
            del recipes_db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Recipe not found")

"""
Example API router - can be extended for actual features
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.models import BaseResponse


# Example models for demonstration
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_active: bool = True


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_active: bool = True


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


# Mock data storage (replace with actual database)
mock_items = [
    Item(id=1, name="Sample Item", description="A sample item", price=29.99),
    Item(id=2, name="Another Item", description="Another sample item", price=19.99)
]


@router.get("/", response_model=List[Item], summary="List all items")
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return")
) -> List[Item]:
    """
    Retrieve a list of items with pagination
    
    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return
        
    Returns:
        List[Item]: List of items
    """
    return mock_items[skip:skip + limit]


@router.get("/{item_id}", response_model=Item, summary="Get item by ID")
async def get_item(item_id: int) -> Item:
    """
    Get a specific item by its ID
    
    Args:
        item_id: The ID of the item to retrieve
        
    Returns:
        Item: The requested item
        
    Raises:
        HTTPException: If item not found
    """
    for item in mock_items:
        if item.id == item_id:
            return item
    
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/", response_model=Item, status_code=201, summary="Create new item")
async def create_item(item: ItemCreate) -> Item:
    """
    Create a new item
    
    Args:
        item: Item data to create
        
    Returns:
        Item: The created item
    """
    new_id = max([i.id for i in mock_items], default=0) + 1
    new_item = Item(id=new_id, **item.dict())
    mock_items.append(new_item)
    return new_item


@router.delete("/{item_id}", response_model=BaseResponse, summary="Delete item")
async def delete_item(item_id: int) -> BaseResponse:
    """
    Delete an item by its ID
    
    Args:
        item_id: The ID of the item to delete
        
    Returns:
        BaseResponse: Deletion confirmation
        
    Raises:
        HTTPException: If item not found
    """
    global mock_items
    
    for i, item in enumerate(mock_items):
        if item.id == item_id:
            mock_items.pop(i)
            return BaseResponse(message=f"Item {item_id} deleted successfully")
    
    raise HTTPException(status_code=404, detail="Item not found")

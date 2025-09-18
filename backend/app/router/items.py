"""
Items API router with database integration
"""

from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.item import item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.models import BaseResponse


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.get("/", response_model=List[ItemResponse], summary="List all items")
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    db: Session = Depends(get_db)
) -> List[ItemResponse]:
    """
    Retrieve a list of items with pagination
    
    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return
        db: Database session
        
    Returns:
        List[ItemResponse]: List of items
    """
    items = item.get_multi(db, skip=skip, limit=limit)
    return [ItemResponse.model_validate(item_obj) for item_obj in items]


@router.get("/{item_id}", response_model=ItemResponse, summary="Get item by ID")
async def get_item(
    item_id: int,
    db: Session = Depends(get_db)
) -> ItemResponse:
    """
    Get a specific item by its ID
    
    Args:
        item_id: The ID of the item to retrieve
        db: Database session
        
    Returns:
        ItemResponse: The requested item
        
    Raises:
        HTTPException: If item not found
    """
    item_obj = item.get(db, item_id=item_id)
    if not item_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item_obj)


@router.post("/", response_model=ItemResponse, status_code=201, summary="Create new item")
async def create_item(
    item_data: ItemCreate,
    db: Session = Depends(get_db)
) -> ItemResponse:
    """
    Create a new item
    
    Args:
        item_data: Item data to create
        db: Database session
        
    Returns:
        ItemResponse: The created item
    """
    created_item = item.create(db=db, obj_in=item_data)
    return ItemResponse.model_validate(created_item)


@router.put("/{item_id}", response_model=ItemResponse, summary="Update item")
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db)
) -> ItemResponse:
    """
    Update an existing item
    
    Args:
        item_id: The ID of the item to update
        item_update: Updated item data
        db: Database session
        
    Returns:
        ItemResponse: The updated item
        
    Raises:
        HTTPException: If item not found
    """
    item_obj = item.get(db, item_id=item_id)
    if not item_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = item.update(db=db, db_obj=item_obj, obj_in=item_update)
    return ItemResponse.model_validate(updated_item)


@router.delete("/{item_id}", response_model=BaseResponse, summary="Delete item")
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
) -> BaseResponse:
    """
    Delete an item by its ID
    
    Args:
        item_id: The ID of the item to delete
        db: Database session
        
    Returns:
        BaseResponse: Deletion confirmation
        
    Raises:
        HTTPException: If item not found
    """
    item_obj = item.delete(db=db, item_id=item_id)
    if not item_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return BaseResponse(message=f"Item {item_id} deleted successfully")

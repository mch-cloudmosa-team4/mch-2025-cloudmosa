"""
CRUD operations for Item model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.items import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemCRUD:
    """
    CRUD operations for Item model
    """
    
    def get(self, db: Session, item_id: int) -> Optional[Item]:
        """
        Get item by ID
        
        Args:
            db: Database session
            item_id: Item ID
            
        Returns:
            Item or None if not found
        """
        return db.query(Item).filter(Item.id == item_id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = True
    ) -> List[Item]:
        """
        Get multiple items with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: Whether to return only active items
            
        Returns:
            List of items
        """
        query = db.query(Item)
        
        if active_only:
            query = query.filter(Item.is_active == True)
            
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: ItemCreate) -> Item:
        """
        Create new item
        
        Args:
            db: Database session
            obj_in: Item creation data
            
        Returns:
            Created item
        """
        db_obj = Item(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        db_obj: Item, 
        obj_in: ItemUpdate
    ) -> Item:
        """
        Update existing item
        
        Args:
            db: Database session
            db_obj: Existing item from database
            obj_in: Update data
            
        Returns:
            Updated item
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, item_id: int) -> Optional[Item]:
        """
        Delete item by ID
        
        Args:
            db: Database session
            item_id: Item ID
            
        Returns:
            Deleted item or None if not found
        """
        db_obj = self.get(db, item_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj
    
    def count(self, db: Session, active_only: bool = True) -> int:
        """
        Count total items
        
        Args:
            db: Database session
            active_only: Whether to count only active items
            
        Returns:
            Total count
        """
        query = db.query(Item)
        
        if active_only:
            query = query.filter(Item.is_active == True)
            
        return query.count()


# Create instance
item = ItemCRUD()

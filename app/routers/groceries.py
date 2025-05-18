from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db

router = APIRouter()

@router.post("/lists/", response_model=schemas.GroceryList)
async def create_grocery_list(
    list_data: schemas.GroceryListCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_list = models.GroceryList(**list_data.dict(), owner_id=current_user.id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.get("/lists/", response_model=List[schemas.GroceryList])
async def read_grocery_lists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    lists = db.query(models.GroceryList).filter(
        models.GroceryList.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return lists

@router.post("/lists/{list_id}/items/", response_model=schemas.GroceryItem)
async def create_grocery_item(
    list_id: int,
    item: schemas.GroceryItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Verify list exists and belongs to user
    db_list = db.query(models.GroceryList).filter(
        models.GroceryList.id == list_id,
        models.GroceryList.owner_id == current_user.id
    ).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Grocery list not found")
    
    db_item = models.GroceryItem(**item.dict(), grocery_list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/items/{item_id}", response_model=schemas.GroceryItem)
async def update_grocery_item(
    item_id: int,
    item_update: schemas.GroceryItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_item = db.query(models.GroceryItem).join(models.GroceryList).filter(
        models.GroceryItem.id == item_id,
        models.GroceryList.owner_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item_update.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grocery_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_item = db.query(models.GroceryItem).join(models.GroceryList).filter(
        models.GroceryItem.id == item_id,
        models.GroceryList.owner_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return None

@router.put("/items/{item_id}/complete", response_model=schemas.GroceryItem)
async def toggle_item_completion(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_item = db.query(models.GroceryItem).join(models.GroceryList).filter(
        models.GroceryItem.id == item_id,
        models.GroceryList.owner_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.is_completed = not db_item.is_completed
    db.commit()
    db.refresh(db_item)
    return db_item 
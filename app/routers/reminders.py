from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app import models, schemas, auth
from app.database import get_db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

router = APIRouter()
scheduler = BackgroundScheduler()
scheduler.start()

def send_reminder(user_email: str, item_name: str):
    # In a real application, you would implement email/notification sending here
    print(f"Sending reminder to {user_email} about {item_name}")

@router.post("/", response_model=schemas.Reminder)
async def create_reminder(
    reminder: schemas.ReminderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Verify item exists and belongs to user
    db_item = db.query(models.GroceryItem).join(models.GroceryList).filter(
        models.GroceryItem.id == reminder.item_id,
        models.GroceryList.owner_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_reminder = models.Reminder(
        item_id=reminder.item_id,
        user_id=current_user.id,
        reminder_date=reminder.reminder_date,
        is_active=reminder.is_active
    )
    
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    
    # Schedule the reminder
    if db_reminder.is_active and db_reminder.reminder_date > datetime.utcnow():
        scheduler.add_job(
            send_reminder,
            trigger=DateTrigger(run_date=db_reminder.reminder_date),
            args=[current_user.email, db_item.name],
            id=f"reminder_{db_reminder.id}"
        )
    
    return db_reminder

@router.get("/", response_model=List[schemas.Reminder])
async def read_reminders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    reminders = db.query(models.Reminder).filter(
        models.Reminder.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return reminders

@router.put("/{reminder_id}", response_model=schemas.Reminder)
async def update_reminder(
    reminder_id: int,
    reminder_update: schemas.ReminderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id,
        models.Reminder.user_id == current_user.id
    ).first()
    
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Update reminder
    for key, value in reminder_update.dict().items():
        setattr(db_reminder, key, value)
    
    db.commit()
    db.refresh(db_reminder)
    
    # Update scheduled job
    job_id = f"reminder_{reminder_id}"
    if job_id in scheduler.get_jobs():
        scheduler.remove_job(job_id)
    
    if db_reminder.is_active and db_reminder.reminder_date > datetime.utcnow():
        db_item = db.query(models.GroceryItem).filter(
            models.GroceryItem.id == db_reminder.item_id
        ).first()
        scheduler.add_job(
            send_reminder,
            trigger=DateTrigger(run_date=db_reminder.reminder_date),
            args=[current_user.email, db_item.name],
            id=job_id
        )
    
    return db_reminder

@router.delete("/{reminder_id}", status_code=204)
async def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id,
        models.Reminder.user_id == current_user.id
    ).first()
    
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Remove scheduled job
    job_id = f"reminder_{reminder_id}"
    if job_id in scheduler.get_jobs():
        scheduler.remove_job(job_id)
    
    db.delete(db_reminder)
    db.commit()
    return None 
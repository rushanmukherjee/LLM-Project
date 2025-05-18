from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import groceries, users, reminders
from app.database import engine, Base

app = FastAPI(title="Smart Grocery Assistant")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(groceries.router, prefix="/api/groceries", tags=["groceries"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Grocery Assistant API"} 
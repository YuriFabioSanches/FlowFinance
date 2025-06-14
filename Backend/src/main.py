from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import engine, Base
from src.routes.transactions_routes import router as finance_router
from src.routes.auth_routes import router as auth_router
from src.routes.user_routes import router as user_router
from src.routes.category_routes import router as category_router
from src.routes.account_routes import router as account_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flow Finance API")

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080", # Your frontend might be served from here if you use a simple server
    "null", # For local file access, if you open index.html directly
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(finance_router)
app.include_router(category_router)
app.include_router(account_router) 
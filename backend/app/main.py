from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import recommendation
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ✅ CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include your router
app.include_router(recommendation.router)

# ✅ Root endpoint
@app.get("/")
def home():
    return {"message": "HabitQuest API is running"}

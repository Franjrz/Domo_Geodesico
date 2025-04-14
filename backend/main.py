from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should specify the exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Domo Geodesico API"}

@app.get("/api/example")
async def example():
    """
    Example endpoint to demonstrate API functionality.
    This will be replaced with actual endpoints later.
    """
    return {
        "status": "success",
        "data": {
            "example": "This is an example response from the API",
            "items": ["item1", "item2", "item3"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

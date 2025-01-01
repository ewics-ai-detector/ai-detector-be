from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from contextlib import asynccontextmanager
from pydantic import BaseModel

class Input(BaseModel):
    text: str

def load_model():
    model_name = "EwicGoat/ai-gen-1"
    global classifier
    classifier = pipeline("text-classification", model=model_name)

# load the model before starting the server
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    # Can use `yield` for cleanup if needed in future
    yield
    print("API shutting down...")

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173"]

# simple middleware to allow react front end to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(data: Input):
    try:
        # Check input length
        if len(data.text) > 512:
            raise HTTPException(
                status_code=400, 
                detail="Length of text must not exceed 512 tokens"
            )

        # Perform prediction
        result = classifier(data.text)[0]  # Always only 1 result
        return {
            "label": result["label"],
            "score": result["score"]
        }

    except HTTPException as e:
        # Rethrow HTTP exceptions to let FastAPI handle them
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,  
            detail=f"An error occurred during prediction: {str(e)}"
        )


@app.get("/")
def read_root():
    return {"Hello": "World"}
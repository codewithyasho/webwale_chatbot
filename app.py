from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from main import main


# ========== Initialize FastAPI ==========
app = FastAPI(
    title="WebWale Agency Chatbot API",
    description="A RAG-based chatbot that answers questions about WebWale Agency's services, offerings, and information.",
    version="1.0.0"
)

# ========== Configure CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's query to the chatbot.", examples=[
                       "What is the refund policy?"])


@app.get("/")
def home():
    return {"message": "Welcome to WebWale Agency Chatbot API! Use the /chat endpoint to interact with the chatbot."}


rag_chain = main()


@app.post("/chat")
async def chat(query_request: QueryRequest):
    try:
        response = rag_chain.invoke({
            "input": query_request.query
        })

        # Remove all * symbols
        clean_text = response['answer'].replace("*", "")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"answer": clean_text}

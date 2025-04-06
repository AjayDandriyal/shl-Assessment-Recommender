from fastapi import FastAPI
from pydantic import BaseModel
from recommend import recommend_assessments
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional: Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryInput(BaseModel):
    query: str

@app.post("/recommend", response_class=JSONResponse)
async def get_recommendations(input: QueryInput):
    try:
        result_df = recommend_assessments(input.query)
        result = result_df.to_dict(orient="records")
        return {"results": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

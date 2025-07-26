import time
start_time = time.time()
from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title= "Voice Bot Api",
    description="REST API for audio-based AI query bot with MurfAi Integration",
    version="0.1"
)


app.include_router(router)

@app.get("/ping")
async def ping():
    return {"message" : "api is live"}
print(f"✅ App initialized in {time.time() - start_time:.2f} seconds")
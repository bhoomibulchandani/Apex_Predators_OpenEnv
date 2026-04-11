import sys
sys.path.append('.')
import uvicorn
from openenv.core.env_server import create_app


from models import CleanAction, Observation


from server.environment import ApexDataCleanerEnv



app = create_app(lambda: ApexDataCleanerEnv(dataset_path='data/task_easy.csv'), CleanAction, Observation)

@app.get("/")
async def healthcheck():
    """Dummy endpoint for Scaler's automated health check."""
    return {"status": "ok", "message": "Server is healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
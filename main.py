import json
from fastapi import FastAPI, HTTPException
import subprocess
import shlex
import os
from dotenv import load_dotenv
from models.stages import TestParams

app = FastAPI()
load_dotenv()

@app.post("/start-test/")
async def start_test(test_params: TestParams):
    test_url = os.getenv("TEST_URL")
    stages_config = [{"duration": stage.duration, "target": stage.target} for stage in test_params.stages]
    config_json = json.dumps({"stages": stages_config, "sleep": test_params.sleep})
    
    command = f"k6 run -e URL={test_url} -e CONFIG='{config_json}' create_load_test.js"
    print(test_url)
    try:
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print(stdout.decode())
            return {"message": "Test started successfully", "stdout": stdout.decode()}
        else:
            return {"error": "Failed to start test", "stderr": stderr.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/healthy")
async def healthy():
    return {"status": "healthy"}
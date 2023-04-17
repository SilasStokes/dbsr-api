from fastapi import FastAPI, Body, Request
from pydantic import BaseModel
import json

app = FastAPI()
# {
#   "data": {
#     "Id": 1,
#     "Title": "Sample Text",
#     "CreatedAt": "2023-03-13T23:13:08.229Z",
#     "UpdatedAt": "2023-03-13T23:13:08.229Z"
#   }
# }
class Test(BaseModel):
    test: str
    
# {{ json data }}

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/test")
# def main(req: Dict[Any, Any]):
#     print(req)
#     return 'hello world'

@app.post("/test")
async def main(req: Request):
    js = await req.json()
    json_formatted_str = json.dumps(js, indent=4)
    print(json_formatted_str)
    return 'hello world'

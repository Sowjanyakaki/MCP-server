from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import sys
import os

from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(title="Google MCP Server")

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    expected_api_key = os.environ.get("API_SECRET_KEY")
    
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        if not expected_api_key:
            raise HTTPException(status_code=500, detail="API_SECRET_KEY not configured on server")
        if api_key != expected_api_key:
            raise HTTPException(status_code=403, detail="Invalid API Key")
    else:
        if expected_api_key and api_key != expected_api_key:
            raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

class DocAppendRequest(BaseModel):
    doc_id: str
    content: str

class EmailDraftRequest(BaseModel):
    to: str
    subject: str
    body: str

def ask_for_approval(action_name: str, payload: dict) -> bool:
    import os
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        print(f"[Production] Auto-approving action: {action_name}")
        return True
        
    print(f"\n--- ACTION REQUIRED ---")
    print(f"Action: {action_name}")
    print(f"Payload: {payload}")
    response = input("Approve? (y/n): ")
    if response.strip().lower() == 'y':
        return True
    return False

@app.post("/append_to_doc")
def api_append_to_doc(req: DocAppendRequest, api_key: str = Depends(verify_api_key)):
    # Using model_dump() for pydantic v2 compatibility, fallback to dict() if v1
    payload = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    
    if not ask_for_approval("append_to_doc", payload):
        raise HTTPException(status_code=403, detail="Action not approved by user")
    
    try:
        result = append_to_doc(req.doc_id, req.content)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_email_draft")
def api_create_email_draft(req: EmailDraftRequest, api_key: str = Depends(verify_api_key)):
    payload = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    
    if not ask_for_approval("create_email_draft", payload):
        raise HTTPException(status_code=403, detail="Action not approved by user")
    
    try:
        result = create_email_draft(req.to, req.subject, req.body)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

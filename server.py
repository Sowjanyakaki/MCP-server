from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys

from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(title="Google MCP Server")

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
def api_append_to_doc(req: DocAppendRequest):
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
def api_create_email_draft(req: EmailDraftRequest):
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

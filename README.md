# MCP-server

A FastAPI-based Model Context Protocol (MCP) server that integrates with Google APIs for document management and email functionality. This server provides API endpoints for appending content to Google Docs and creating email drafts in Gmail.

## Overview

MCP-server is a Python application that exposes REST API endpoints for interacting with Google services through FastAPI. It includes built-in approval workflows for user actions and supports both local and production deployments.

## Features

- **Google Docs Integration**: Append content to Google Documents
- **Gmail Integration**: Create email drafts in Gmail
- **Action Approval Workflow**: User confirmation for sensitive operations
- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **OAuth2 Authentication**: Secure Google API authentication
- **Production Ready**: Support for Railway.app deployment

## Technology Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Authentication**: Google OAuth2
- **Python Libraries**:
  - `fastapi` - Web framework
  - `uvicorn` - ASGI server
  - `google-api-python-client` - Google API client
  - `google-auth-httplib2` - Google authentication
  - `google-auth-oauthlib` - OAuth flow support
  - `pydantic` - Data validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sowjanyakaki/MCP-server.git
cd MCP-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google API credentials:
   - Download your Google API credentials from Google Cloud Console
   - Save as `credentials.json` in the project root

## Configuration

### Environment Variables

- `GOOGLE_CREDENTIALS_JSON`: JSON string containing Google API credentials
- `GOOGLE_TOKEN_JSON`: JSON string containing the Google OAuth token
- `RAILWAY_ENVIRONMENT`: Set to enable production mode (auto-approves actions)

### Local Setup

Run the authentication script first to generate `token.json`:
```bash
python auth.py
```

## Running the Server

Start the server locally:
```bash
python server.py
```

The server will run on `http://0.0.0.0:8000` by default.

Access the interactive API documentation at: `http://localhost:8000/docs`

## API Endpoints

### 1. Append to Document
**Endpoint**: `POST /append_to_doc`

**Description**: Appends text content to the end of a Google Document.

**Request Body**:
```json
{
  "doc_id": "string",
  "content": "string"
}
```

**Parameters**:
- `doc_id` (string, required): The ID of the Google Document
- `content` (string, required): The content to append to the document

**Success Response** (200):
```json
{
  "status": "success",
  "result": {
    "documentId": "string",
    "replies": []
  }
}
```

**Error Responses**:
- `403 Forbidden`: Action not approved by user
- `500 Internal Server Error`: Server-side error with details

**Example**:
```bash
curl -X POST "http://localhost:8000/append_to_doc" \
  -H "Content-Type: application/json" \
  -d '{"doc_id":"1ABC2DEF3GHI","content":"New paragraph text"}'
```

---

### 2. Create Email Draft
**Endpoint**: `POST /create_email_draft`

**Description**: Creates a draft email in Gmail with the specified recipient, subject, and body.

**Request Body**:
```json
{
  "to": "string",
  "subject": "string",
  "body": "string"
}
```

**Parameters**:
- `to` (string, required): Recipient email address
- `subject` (string, required): Email subject line
- `body` (string, required): Email body content

**Success Response** (200):
```json
{
  "status": "success",
  "result": {
    "id": "string",
    "message": {
      "id": "string",
      "threadId": "string"
    }
  }
}
```

**Error Responses**:
- `403 Forbidden`: Action not approved by user
- `500 Internal Server Error`: Server-side error with details

**Example**:
```bash
curl -X POST "http://localhost:8000/create_email_draft" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Meeting Reminder",
    "body": "Hi there, just a reminder about our meeting tomorrow at 2 PM."
  }'
```

---

## API Documentation

Once the server is running, access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces provide:
- Complete endpoint documentation
- Request/response schema details
- Try-it-out functionality for testing endpoints
- Parameter validation information

## Approval Workflow

All API endpoints require user approval before execution:

**Local Environment**:
- Server displays action details in the console
- Prompts user to approve with `Approve? (y/n):`
- Proceeds only on 'y' confirmation

**Production Environment** (Railway):
- Auto-approves actions when `RAILWAY_ENVIRONMENT` is set
- Logs action details for audit purposes

## Deployment

### Railway Deployment

Configuration file: `railway.toml`

Deploy to Railway:
```bash
railway up
```

For detailed deployment instructions, see [deployment.md](./deployment.md)

## Project Structure

```
MCP-server/
├── server.py              # FastAPI application and endpoints
├── auth.py                # Google OAuth2 authentication
├── gmail_tool.py          # Gmail draft creation functionality
├── docs_tool.py           # Google Docs append functionality
├── requirements.txt       # Python dependencies
├── credentials.json       # Google API credentials (local only)
├── token.json             # OAuth token (generated locally)
├── railway.toml           # Railway deployment config
├── deployment.md          # Deployment instructions
└── README.md              # This file
```

## Google API Scopes

The server uses the following Google API scopes:
- `https://www.googleapis.com/auth/documents` - Google Docs access
- `https://www.googleapis.com/auth/gmail.compose` - Gmail compose access

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK` - Successful operation
- `403 Forbidden` - User did not approve the action
- `500 Internal Server Error` - Server-side error with error message

## Security Considerations

- Credentials are stored securely via environment variables in production
- Local development uses `credentials.json` and `token.json`
- All API calls require valid Google OAuth tokens
- Action approval workflow prevents unauthorized operations

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on GitHub: https://github.com/Sowjanyakaki/MCP-server/issues

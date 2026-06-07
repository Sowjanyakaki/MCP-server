from googleapiclient.discovery import build
from auth import get_credentials

def append_to_doc(doc_id: str, content: str):
    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)

    # First, get the document to find its end index
    document = service.documents().get(documentId=doc_id).execute()
    content_list = document.get('body').get('content')
    
    # The last element in the body content contains the end index.
    last_element = content_list[-1]
    end_index = last_element.get('endIndex') - 1 # Insert before the final newline

    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index,
                },
                'text': content
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=doc_id, body={'requests': requests}).execute()
    return result

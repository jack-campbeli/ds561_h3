import functions_framework
from flask import Request, Response
from google.cloud import storage

def get_file_name(request: Request):
    url_path = request.path
    # Split the URL path using '/' as a separator and get the last element
    file_name = url_path.split('/')[-1]
    
    return file_name

# https://us-central1-jacks-project-398813.cloudfunctions.net/files_get
@functions_framework.http
def files_get(request):
    """HTTP Cloud Function.
    Args:
       
    Returns:
       
    """
    # Get the HTTP method (GET, POST, etc.)
    method = request.method
    if method != 'GET':
        return 'Not Implemented', 501
    else:
        file_name = get_file_name(request)

        client = storage.Client()
        bucket_name = 'bu-ds561-jawicamp'
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        try:

            content = blob.download_as_text()

            response = Response(content, status=200, headers={'Content-Type': 'text/html'})

            return response

        except Exception as e:
            return str(e), 404  # Return a 404 Not Found response if the file is not found or an error occurs

# Notes:
# - python http-client.py -d "us-central1-jacks-project-398813.cloudfunctions.net" -b "none" -w "files_get" -v -n 5 -i 10000 
import functions_framework
from flask import Request, Response
from google.cloud import storage
from google.cloud import pubsub_v1

banned = ['north korea', 'iran', 'cuba', 'myanmar', 'iraq', 'libya', 'sudan', 'zimbabwe', 'syria']

def get_file_name(request: Request):
    url_path = request.path
    # split url path with '/' and get the last element
    file_name = url_path.split('/')[-1]
    
    return file_name

# https://us-central1-jacks-project-398813.cloudfunctions.net/files_get
@functions_framework.http
def files_get(request):
    """HTTP Cloud Function.
    Args:
       
    Returns:
       
    """
    method = request.method
    if method != 'GET':
        print("Method not implemented: ", method)
        return 'Not Implemented', 501
    else:

        country = request.headers.get('X-country')
        print("Country: ", country.lower())
        
        if country.lower() not in banned:

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
                print("File not found: ",file_name)
                return str(e), 404  
            
        else:
            print("Permission Denied")
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path('jacks-project-398813', 'banned_countries-sub')
    
            data_str = f"{country}"
            # Data must be a bytestring
            data = data_str.encode("utf-8")
            # When you publish a message, the client returns a future.
            future = publisher.publish(topic_path, data)
            print(future.result())
            return "Permission Denied", 400

# Notes:
# - python http-client.py -d "us-central1-jacks-project-398813.cloudfunctions.net" -b "none" -w "files_get" -v -n 5 -i 10000 
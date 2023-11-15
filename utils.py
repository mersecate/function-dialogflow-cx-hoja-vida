import uuid
import json
from google.cloud import storage
from google.cloud import firestore
from google.cloud import functions_v1
from xhtml2pdf import pisa

def generate_token(filename):
    """
    Generate a unique token for the given filename and store it in Firestore.

    Args:
        filename (str): The name of the file.

    Returns:
        str: The generated document ID.
    """
    document_id = ""
    data = {"fileName": filename}
    db = firestore.Client()
    update_time, doc_ref = db.collection("curriv").add(data)
    document_id = doc_ref.id
    return document_id

async def send_mail(name, mail_request):
    """
    Asynchronously send an email using Google Cloud Functions.

    Args:
        name (str): The name of the function to call.
        mail_request (dict): The data to send in the email request.
    """
    client = functions_v1.CloudFunctionsServiceAsyncClient()

    request = functions_v1.CallFunctionRequest(
        name=name,
        data=json.dumps(mail_request),
    )

    response = await client.call_function(request=request)

    print(f"Function response: {response}")

def generate_file_url(ambiente, file_name):
    """
    Generate a file URL based on the environment and file information.

    Args:
        ambiente (str): The environment ("HML" or "PROD").
        file_name (str): The name of the file.

    Returns:
        str: The generated file URL.
    """
    token_result = generate_token(file_name)

    if ambiente == "HML":
        base_url = "https://us-west1-bogotatrabaja-hml.cloudfunctions.net/function-dialogflow-get-file"
    elif ambiente == "PROD":
        base_url = "https://us-west1-bogotatrabaja-prd.cloudfunctions.net/function-dialogflow-get-file"
    else:
        raise ValueError("Invalid environment")

    url_file = f"{base_url}?env={ambiente}&token={token_result}&namefile={file_name}"

    return url_file

def create_json_response(url_file):
    """
    Create a JSON response with a link to the generated file.

    Args:
        url_file (str): The URL of the generated file.

    Returns:
        dict: The JSON response.
    """
    json_response = {
        "fulfillment_response": {
            "messages": [
                {
                    "payload": {
                        "richContent": [
                            [
                                {
                                    "text": "Resume",
                                    "icon": {
                                        "color": "#1E88E5",
                                        "type": "article"
                                    },
                                    "link": url_file,
                                    "type": "button"
                                }
                            ]
                        ]
                    }
                }
            ]
        }
    }

    return json_response

def create_and_upload_pdf(source_html, bucket_name):
    """
    Create a PDF file from HTML and upload it to Google Cloud Storage.

    Args:
        source_html (str): The HTML content to convert to PDF.
        bucket_name (str): The name of the Google Cloud Storage bucket.

    Returns:
        str: The generated PDF file's name.
    """
    # Create a storage client
    storage_client = storage.Client()

    # Generate a unique filename with a .pdf extension
    file_name = str(uuid.uuid4()) + ".pdf"

    # Get the storage bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a Blob object in the bucket with the generated filename
    blob = bucket.blob(file_name)

    # Open the Blob file in binary write mode
    with blob.open("wb") as result_file:
        # Convert HTML to PDF and write to the resulting file
        pisa_status = pisa.CreatePDF(
            source_html,  # HTML to convert
            dest=result_file  # file handler to receive the result
        )

    # Close the output file
    result_file.close()

    # Return the generated filename
    return file_name

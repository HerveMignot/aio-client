import datetime

from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def get_gcs_download_signed_url_v4(bucket_name, blob_name, sa_file=None):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    if sa_file:
      credentials = service_account.Credentials.from_service_account_file(sa_file)
      storage_client = storage.Client(credentials=credentials)
    else:
      storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )
    # f"curl '{url}'
    return url


def get_gcs_upload_signed_url_v4(bucket_name, blob_name, sa_file=None):
    """Generates a v4 signed URL for uploading a blob using HTTP PUT.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    if sa_file:
      credentials = service_account.Credentials.from_service_account_file(sa_file)
      storage_client = storage.Client(credentials=credentials)
    else:
      storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow PUT requests using this URL.
        method="PUT",
        content_type="application/octet-stream",
    )

    #     "curl -X PUT -H 'Content-Type: application/octet-stream' "
    #     "--upload-file my-file '{}'".format(url)
    return url


def upload_file_to_google_drive(file_path, folder_id=None, service_account_file=None):
    """
    Uploads a file to Google Drive using a service account.
    
    :param service_account_file: Path to the service account JSON file.
    :param file_path: Path to the file you want to upload.
    :param folder_id: Optional. The ID of the folder where the file will be uploaded. If None, uploads to the root directory.
    :return: File ID of the uploaded file.

    Example usage:
    upload_to_google_drive('path/to/upload/file.txt', 'folder_id', 'path/to/service_account.json')
    """
    
    # Authenticate using the service account file
    if service_account_file:
      credentials = service_account.Credentials.from_service_account_file(service_account_file)
      service = build('drive', 'v3', credentials=credentials)
    else:
      service = build('drive', 'v3')

    # File metadata
    file_metadata = {'name': file_path.split('/')[-1]}
    
    if folder_id:
        file_metadata['parents'] = [folder_id]

    # Media upload object
    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    #print(f"File ID: {file.get('id')}")
    return file.get('id')


def get_azure_blob_signed_url(storage_account_name, storage_container_name, blob_path, account_access_key, rights="r"):
    """Generates a signed URL for downloading or uploading to Azure Blob storage.

    Note that this method requires a storage account access key, from Azure portal storage account settings.

    :param storage_account_name: Name of the storage account.
    :param storage_container_name: Name of the storage container.
    :param blob_path: Path to the blob.
    :param account_access_key: Access key of the storage account.
    :param rights: Optional. Rights to grant to the signed URL. Defaults to "r". Use "cw" for creating & uploading new blob.
    :return: Signed URL.

    Example usage:
    get_azure_blob_signed_url('my_storage_account','my_container', 'path/to/blob.txt', 'access_key', 'r')
    """

    sas_token = generate_account_sas(
        account_name=storage_account_name,
        account_key=account_access_key,
        resource_types=ResourceTypes(object=True),
        permission=AccountSasPermissions(read=("r" in rights), write=("w" in rights), update=("u" in rights), create=("c" in rights)),
        expiry=datetime.datetime.now() + datetime.timedelta(hours=1)
    )
    return f"https://{storage_account_name}.blob.core.windows.net/{storage_container_name}/{blob_path}?{sas_token}"

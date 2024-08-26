import datetime
import requests
import time

from constants import Storage, Colorspace, CreateMaskType, MimeType
from typing import Self


class AdobeClient(object):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        self._token = None
        self._token_expires = None


    def get_access_token(self) -> str:
        if self._token is None or datetime.datetime.now() >= self._token_expires:
            response = requests.post(f"https://ims-na1.adobelogin.com/ims/token/v3?client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials&scope=openid,AdobeID,firefly_enterprise,firefly_api,ff_apis")
            self._token = response.json()['access_token']
            self._token_expires = datetime.datetime.now() + datetime.timedelta(seconds=response.json()['expires_in'])
        return self._token


    def _infer_storage_type(self, url: str) -> str:
        if "blob.core.windows.net" in url:
            return Storage.AZURE # "azure"
        elif "s3.amazonaws.com" in url:
            return Storage.EXTERNAL # "external"
        elif "storage.googleapis.com" in url:
            return Storage.EXTERNAL # "external"
        elif "dropbox.com" in url:
            return Storage.DROPBOX
        else:
            return Storage.EXTERNAL # "external"


    def _start_job(self, service_url: str, data: dict) -> dict:
        response = requests.post(service_url,
                                 headers = {"Authorization": f"Bearer {self.get_access_token()}",
                                            "x-api-key": self.client_id },
                                 json=data)
        return response.json()


    def remove_background_from_image(self, input_url:str, output_url: str) -> dict:
        _service_url = "https://image.adobe.io/sensei/cutout"
        data = {
            "input": {
                "href": input_url,
                "storage": self._infer_storage_type(input_url)
            },
		    "options": { "optimize": "performance", },
            "output": {
                "href": output_url,
                "storage": self._infer_storage_type(output_url),
                "overwrite": True,
                "color": {
                    "space": Colorspace.RGB
                },
                "mask": {
                    "format": CreateMaskType.SOFT
                    }
            }            
        }
        return self._start_job(_service_url, data)


    def apply_autotone(self, input_url: str, output_url: str) -> dict:
        """Apply autotone processing to an image.

        See: 

        Args:
            input_url (str): input image url
            output_url (str): output image url

        Returns:
            dict: Adobe API job description
        """
        _service_url = "https://image.adobe.io/lrService/autoTone"
        data = {
            "inputs":{
                "href": input_url,
                "storage": self._infer_storage_type(input_url)
            },
            "outputs": [
                {
                    "href": output_url,
                    "storage": self._infer_storage_type(output_url),
                    "type": MimeType.JPEG
                }
            ]
        }
        return self._start_job(_service_url, data)

    
    def pollJob(self, job: dict, max_retries=10) -> dict:
        jobUrl = job["_links"]["self"]["href"]
        status = ""
        trial = 0
        while status != 'succeeded' and status != 'failed':
            response = requests.get(jobUrl, headers = {"Authorization": f"Bearer {self.get_access_token()}",
                                                       "x-api-key": self.client_id })
            json_response = response.json()
            
            if "status" in json_response:
                status = json_response["status"]
            elif "status" in json_response["outputs"][0]:
                status = json_response["outputs"][0]["status"]
            
            if status != 'succeeded' and status != 'failed':
                # TODO: add a max_retries parameter
                time.sleep(3)
                trial += 1
            else:
                return json_response
            
            if trial > max_retries:
                raise Exception("Max retries exceeded")
            

class AdobeJob(object):
    def __init__(self, client: AdobeClient, job: dict):
        self.client = client
        self.job = job
        self.job_id = job["jobID"]
        self.url = job["_links"]["self"]["href"]

        self.status = None
        self.outputs = None
    

    def poll(self) -> Self:
        response = requests.get(self.url, headers = {"Authorization": f"Bearer {self.client.get_access_token()}",
                                                     "x-api-key": self.client.client_id })
        json_response = response.json()
        
        if "status" in json_response:
            self.status = json_response["status"]
        elif "status" in json_response["outputs"][0]:
            self.status = json_response["outputs"][0]["status"]
        
        if "outputs" in json_response:
            self.outputs = json_response["outputs"]
        elif "output" in json_response:
            self.outputs = [json_response["output"]]

        return self


    def is_done(self) -> bool:
        self.poll()
        return self.status == "succeeded" or self.status == "failed"
    

    def poll_until_done(self, max_retries=10) -> Self:
        trial = 0
        while not self.is_done():
            time.sleep(3)
            trial += 1
            
            if trial > max_retries:
                raise Exception("Max retries exceeded")
            
        return self

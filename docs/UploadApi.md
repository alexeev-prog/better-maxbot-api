# max_client.UploadApi

All URIs are relative to *https://botapi.max.ru*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_upload_url**](UploadApi.md#get_upload_url) | **POST** /uploads | Get upload URL


# **get_upload_url**
> UploadEndpoint get_upload_url(type)

Get upload URL

Returns the URL for the subsequent file upload.  For example, you can upload it via curl:  ```curl -i -X POST   -H \"Content-Type: multipart/form-data\"   -F \"data=@movie.mp4\" \"%UPLOAD_URL%\"```  Two types of an upload are supported: - single request upload (multipart request) - and resumable upload.  ##### Multipart upload This type of upload is a simpler one but it is less reliable and agile. If a `Content-Type`: multipart/form-data header is passed in a request our service indicates upload type as a simple single request upload.  This type of an upload has some restrictions:  - Max. file size - 2 Gb - Only one file per request can be uploaded - No possibility to restart stopped / failed upload  ##### Resumable upload If `Content-Type` header value is not equal to `multipart/form-data` our service indicated upload type as a resumable upload. With a `Content-Range` header current file chunk range and complete file size can be passed. If a network error has happened or upload was stopped you can continue to upload a file from the last successfully uploaded file chunk. You can request the last known byte of uploaded file from server and continue to upload a file.  ##### Get upload status To GET an upload status you simply need to perform HTTP-GET request to a file upload URL. Our service will respond with current upload status, complete file size and last known uploaded byte. This data can be used to complete stopped upload if something went wrong. If `REQUESTED_RANGE_NOT_SATISFIABLE` or `INTERNAL_SERVER_ERROR` status was returned it is a good point to try to restart an upload

### Example
```python
from __future__ import print_function
import time
import max_client
from max_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: access_token
configuration = max_client.Configuration()
configuration.api_key['access_token'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['access_token'] = 'Bearer'

# create an instance of the API class
api_instance = max_client.UploadApi(max_client.ApiClient(configuration))
type = max_client.UploadType() # UploadType | Uploaded file type: photo, audio, video, file

try:
    # Get upload URL
    api_response = api_instance.get_upload_url(type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UploadApi->get_upload_url: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | [**UploadType**](.md)| Uploaded file type: photo, audio, video, file | 

### Return type

[**UploadEndpoint**](UploadEndpoint.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


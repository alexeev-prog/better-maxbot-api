# max_client.BotsApi

All URIs are relative to *https://botapi.max.ru*

Method | HTTP request | Description
------------- | ------------- | -------------
[**edit_my_info**](BotsApi.md#edit_my_info) | **PATCH** /me | Edit current bot info
[**get_my_info**](BotsApi.md#get_my_info) | **GET** /me | Get current bot info


# **edit_my_info**
> BotInfo edit_my_info(bot_patch)

Edit current bot info

Edits current bot info. Fill only the fields you want to update. All remaining fields will stay untouched

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
api_instance = max_client.BotsApi(max_client.ApiClient(configuration))
bot_patch = max_client.BotPatch() # BotPatch | 

try:
    # Edit current bot info
    api_response = api_instance.edit_my_info(bot_patch)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BotsApi->edit_my_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bot_patch** | [**BotPatch**](BotPatch.md)|  | 

### Return type

[**BotInfo**](BotInfo.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_my_info**
> BotInfo get_my_info()

Get current bot info

Returns info about current bot. Current bot can be identified by access token. Method returns bot identifier, name and avatar (if any)

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
api_instance = max_client.BotsApi(max_client.ApiClient(configuration))

try:
    # Get current bot info
    api_response = api_instance.get_my_info()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BotsApi->get_my_info: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BotInfo**](BotInfo.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


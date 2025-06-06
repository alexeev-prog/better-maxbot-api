# max_client.ChatsApi

All URIs are relative to *https://botapi.max.ru*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_members**](ChatsApi.md#add_members) | **POST** /chats/{chatId}/members | Add members
[**delete_admins**](ChatsApi.md#delete_admins) | **DELETE** /chats/{chatId}/members/admins/{userId} | Revoke admin rights
[**delete_chat**](ChatsApi.md#delete_chat) | **DELETE** /chats/{chatId} | Delete chat
[**edit_chat**](ChatsApi.md#edit_chat) | **PATCH** /chats/{chatId} | Edit chat info
[**get_admins**](ChatsApi.md#get_admins) | **GET** /chats/{chatId}/members/admins | Get chat admins
[**get_chat**](ChatsApi.md#get_chat) | **GET** /chats/{chatId} | Get chat
[**get_chat_by_link**](ChatsApi.md#get_chat_by_link) | **GET** /chats/{chatLink} | Get chat by link
[**get_chats**](ChatsApi.md#get_chats) | **GET** /chats | Get all chats
[**get_members**](ChatsApi.md#get_members) | **GET** /chats/{chatId}/members | Get members
[**get_membership**](ChatsApi.md#get_membership) | **GET** /chats/{chatId}/members/me | Get chat membership
[**get_pinned_message**](ChatsApi.md#get_pinned_message) | **GET** /chats/{chatId}/pin | Get pinned message
[**leave_chat**](ChatsApi.md#leave_chat) | **DELETE** /chats/{chatId}/members/me | Leave chat
[**pin_message**](ChatsApi.md#pin_message) | **PUT** /chats/{chatId}/pin | Pin message
[**post_admins**](ChatsApi.md#post_admins) | **POST** /chats/{chatId}/members/admins | Set chat admins
[**remove_member**](ChatsApi.md#remove_member) | **DELETE** /chats/{chatId}/members | Remove member
[**send_action**](ChatsApi.md#send_action) | **POST** /chats/{chatId}/actions | Send action
[**unpin_message**](ChatsApi.md#unpin_message) | **DELETE** /chats/{chatId}/pin | Unpin message


# **add_members**
> SimpleQueryResult add_members(chat_id, user_ids_list)

Add members

Adds members to chat. Additional permissions may require.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier
user_ids_list = max_client.UserIdsList() # UserIdsList | 

try:
    # Add members
    api_response = api_instance.add_members(chat_id, user_ids_list)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->add_members: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 
 **user_ids_list** | [**UserIdsList**](UserIdsList.md)|  | 

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_admins**
> SimpleQueryResult delete_admins(chat_id, user_id)

Revoke admin rights

Revokes admin rights from a user in the chat by removing their administrative privileges

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier
user_id = 56 # int | User identifier

try:
    # Revoke admin rights
    api_response = api_instance.delete_admins(chat_id, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->delete_admins: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 
 **user_id** | **int**| User identifier | 

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_chat**
> SimpleQueryResult delete_chat(chat_id)

Delete chat

Deletes chat for all participants.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier

try:
    # Delete chat
    api_response = api_instance.delete_chat(chat_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->delete_chat: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_chat**
> Chat edit_chat(chat_id, chat_patch)

Edit chat info

Edits chat info: title, icon, etc…

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier
chat_patch = max_client.ChatPatch() # ChatPatch | 

try:
    # Edit chat info
    api_response = api_instance.edit_chat(chat_id, chat_patch)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->edit_chat: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 
 **chat_patch** | [**ChatPatch**](ChatPatch.md)|  | 

### Return type

[**Chat**](Chat.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_admins**
> ChatMembersList get_admins(chat_id)

Get chat admins

Returns all chat administrators. Bot must be **administrator** in requested chat.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier

try:
    # Get chat admins
    api_response = api_instance.get_admins(chat_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->get_admins: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 

### Return type

[**ChatMembersList**](ChatMembersList.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_chat**
> Chat get_chat(chat_id)

Get chat

Returns info about chat.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Requested chat identifier

try:
    # Get chat
    api_response = api_instance.get_chat(chat_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->get_chat: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Requested chat identifier | 

### Return type

[**Chat**](Chat.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_chat_by_link**
> Chat get_chat_by_link(chat_link)

Get chat by link

Returns chat/channel information by its public link or dialog with user by username

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_link = 'chat_link_example' # str | Public chat link or username

try:
    # Get chat by link
    api_response = api_instance.get_chat_by_link(chat_link)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->get_chat_by_link: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_link** | **str**| Public chat link or username | 

### Return type

[**Chat**](Chat.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_chats**
> ChatList get_chats(count=count, marker=marker)

Get all chats

Returns information about chats that bot participated in: a result list and marker points to the next page

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
count = 50 # int | Number of chats requested (optional) (default to 50)
marker = 56 # int | Points to next data page. `null` for the first page (optional)

try:
    # Get all chats
    api_response = api_instance.get_chats(count=count, marker=marker)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->get_chats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **count** | **int**| Number of chats requested | [optional] [default to 50]
 **marker** | [**int**](.md)| Points to next data page. &#x60;null&#x60; for the first page | [optional] 

### Return type

[**ChatList**](ChatList.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_members**
> ChatMembersList get_members(chat_id, user_ids=user_ids, marker=marker, count=count)

Get members

Returns users participated in chat.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier
user_ids = [56] # list[int] | *Since* version [0.1.4](#section/About/Changelog).  Comma-separated list of users identifiers to get their membership. When this parameter is passed, both `count` and `marker` are ignored (optional)
marker = 56 # int | Marker (optional)
count = 20 # int | Count (optional) (default to 20)

try:
    # Get members
    api_response = api_instance.get_members(chat_id, user_ids=user_ids, marker=marker, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->get_members: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 
 **user_ids** | [**list[int]**](int.md)| *Since* version [0.1.4](#section/About/Changelog).  Comma-separated list of users identifiers to get their membership. When this parameter is passed, both &#x60;count&#x60; and &#x60;marker&#x60; are ignored | [optional] 
 **marker** | **int**| Marker | [optional] 
 **count** | **int**| Count | [optional] [default to 20]

### Return type

[**ChatMembersList**](ChatMembersList.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_membership**
> ChatMember get_membership(chat_id)

Get chat membership

Returns chat membership info for current bot

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier

try:
    # Get chat membership
    api_response = api_instance.get_membership(chat_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->get_membership: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 

### Return type

[**ChatMember**](ChatMember.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pinned_message**
> GetPinnedMessageResult get_pinned_message(chat_id)

Get pinned message

Get pinned message in chat or channel.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier to get its pinned message

try:
    # Get pinned message
    api_response = api_instance.get_pinned_message(chat_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->get_pinned_message: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier to get its pinned message | 

### Return type

[**GetPinnedMessageResult**](GetPinnedMessageResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **leave_chat**
> SimpleQueryResult leave_chat(chat_id)

Leave chat

Removes bot from chat members.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier

try:
    # Leave chat
    api_response = api_instance.leave_chat(chat_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->leave_chat: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pin_message**
> SimpleQueryResult pin_message(chat_id, pin_message_body)

Pin message

Pins message in chat or channel.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier where message should be pinned
pin_message_body = max_client.PinMessageBody() # PinMessageBody | 

try:
    # Pin message
    api_response = api_instance.pin_message(chat_id, pin_message_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->pin_message: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier where message should be pinned | 
 **pin_message_body** | [**PinMessageBody**](PinMessageBody.md)|  | 

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_admins**
> SimpleQueryResult post_admins(chat_id, chat_admins_list)

Set chat admins

Returns true if all administrators added.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier
chat_admins_list = max_client.ChatAdminsList() # ChatAdminsList | 

try:
    # Set chat admins
    api_response = api_instance.post_admins(chat_id, chat_admins_list)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->post_admins: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 
 **chat_admins_list** | [**ChatAdminsList**](ChatAdminsList.md)|  | 

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_member**
> SimpleQueryResult remove_member(chat_id, user_id, block=block)

Remove member

Removes member from chat. Additional permissions may require.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier
user_id = 56 # int | User id to remove from chat
block = False # bool | Set to `true` if user should be blocked in chat. Applicable only for chats that have public or private link. Ignored otherwise (optional) (default to False)

try:
    # Remove member
    api_response = api_instance.remove_member(chat_id, user_id, block=block)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->remove_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 
 **user_id** | **int**| User id to remove from chat | 
 **block** | **bool**| Set to &#x60;true&#x60; if user should be blocked in chat. Applicable only for chats that have public or private link. Ignored otherwise | [optional] [default to False]

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **send_action**
> SimpleQueryResult send_action(chat_id, action_request_body)

Send action

Send bot action to chat.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier
action_request_body = max_client.ActionRequestBody() # ActionRequestBody | 

try:
    # Send action
    api_response = api_instance.send_action(chat_id, action_request_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->send_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier | 
 **action_request_body** | [**ActionRequestBody**](ActionRequestBody.md)|  | 

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unpin_message**
> SimpleQueryResult unpin_message(chat_id)

Unpin message

Unpins message in chat or channel.

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
api_instance = max_client.ChatsApi(max_client.ApiClient(configuration))
chat_id = 56 # int | Chat identifier to remove pinned message

try:
    # Unpin message
    api_response = api_instance.unpin_message(chat_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChatsApi->unpin_message: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_id** | **int**| Chat identifier to remove pinned message | 

### Return type

[**SimpleQueryResult**](SimpleQueryResult.md)

### Authorization

[access_token](../README.md#access_token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


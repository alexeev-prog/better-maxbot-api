# ChatMember

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**last_access_time** | **int** | User last activity time in chat. Can be outdated for super chats and channels (equals to &#x60;join_time&#x60;) | 
**is_owner** | **bool** |  | 
**is_admin** | **bool** |  | 
**join_time** | **int** |  | 
**permissions** | [**list[ChatAdminPermission]**](ChatAdminPermission.md) | Permissions in chat if member is admin. &#x60;null&#x60; otherwise | 
**alias** | **str** | Alias in chat if member is admin. By default, &#x60;null&#x60; | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



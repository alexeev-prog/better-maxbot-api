# Message

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sender** | [**User**](User.md) | User who sent this message. Can be &#x60;null&#x60; if message has been posted on behalf of a channel | [optional] 
**recipient** | [**Recipient**](Recipient.md) | Message recipient. Could be user or chat | 
**timestamp** | **int** | Unix-time when message was created | 
**link** | [**LinkedMessage**](LinkedMessage.md) | Forwarded or replied message | [optional] 
**body** | [**MessageBody**](MessageBody.md) | Body of created message. Text + attachments. Could be null if message contains only forwarded message | 
**stat** | [**MessageStat**](MessageStat.md) | Message statistics. Available only for channels in [GET:/messages](#operation/getMessages) context | [optional] 
**url** | **str** | Message public URL. Can be &#x60;null&#x60; for dialogs or non-public chats/channels | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



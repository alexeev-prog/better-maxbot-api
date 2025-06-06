# Chat

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**chat_id** | **int** | Chats identifier | 
**type** | [**ChatType**](ChatType.md) | Type of chat. One of: dialog, chat, channel | 
**status** | [**ChatStatus**](ChatStatus.md) | Chat status. One of:  - active: bot is active member of chat  - removed: bot was kicked  - left: bot intentionally left chat  - closed: chat was closed  - suspended: bot was stopped by user. *Only for dialogs* | 
**title** | **str** | Visible title of chat. Can be null for dialogs | 
**icon** | [**Image**](Image.md) | Icon of chat | 
**last_event_time** | **int** | Time of last event occurred in chat | 
**participants_count** | **int** | Number of people in chat. Always 2 for &#x60;dialog&#x60; chat type | 
**owner_id** | **int** | Identifier of chat owner. Visible only for chat admins | [optional] 
**participants** | **dict(str, int)** | Participants in chat with time of last activity. Can be *null* when you request list of chats. Visible for chat admins only | [optional] 
**is_public** | **bool** | Is current chat publicly available. Always &#x60;false&#x60; for dialogs | 
**link** | **str** | Link on chat | [optional] 
**description** | **str** | Chat description | 
**dialog_with_user** | [**UserWithPhoto**](UserWithPhoto.md) | Another user in conversation. For &#x60;dialog&#x60; type chats only | [optional] 
**messages_count** | **int** | Messages count in chat. Only for group chats and channels. **Not available** for dialogs | [optional] 
**chat_message_id** | **str** | Identifier of message that contains &#x60;chat&#x60; button initialized chat | [optional] 
**pinned_message** | [**Message**](Message.md) | Pinned message in chat or channel. Returned only when single chat is requested | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



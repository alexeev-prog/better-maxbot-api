# SubscriptionRequestBody

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | URL of HTTP(S)-endpoint of your bot. Must starts with http(s):// | 
**secret** | **str** | A secret to be sent in a header “X-Max-Bot-Api-Secret” in every webhook request, 5-256 characters. Only characters A-Z, a-z, 0-9, _ and - are allowed. The header is useful to ensure that the request comes from a webhook set by you. | [optional] 
**update_types** | **list[str]** | List of update types your bot want to receive. See &#x60;Update&#x60; object for a complete list of types | [optional] 
**version** | **str** | Version of API. Affects model representation | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



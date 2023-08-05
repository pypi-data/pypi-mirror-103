# UpstreamGroupMappingSpec

The definition of an upstream group mapping
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upstream_issuer** | **str** | the upstream issuer that this mapping pertains to | 
**org_id** | **str** | The org id corresponding to the issuer whose mapping is being updated | 
**group_mappings** | [**list[UpstreamGroupMappingEntry]**](UpstreamGroupMappingEntry.md) | The list of upstream group mappings | [optional] 
**excluded_groups** | [**list[UpstreamGroupExcludedEntry]**](UpstreamGroupExcludedEntry.md) | The list of upstream groups you wish to explicitly exclude from mapping. This is useful for a wildcard mapping  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



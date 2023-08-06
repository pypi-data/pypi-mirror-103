# BillableMetric

A generic metric pertaining to a given billable. A metric contains one or more measurements Provisioned measurements pertain to the set of created billable in the org specified by org_id Active metrics is the set of billables currently deemed active. Each billable has a different algorithm for determining if the billable is active or not. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the billable | [optional] 
**org_id** | **str** | The unique id of the Organisation to which this record applies.  | [optional] 
**provisioned** | [**BillableMeasurement**](BillableMeasurement.md) |  | [optional] 
**active** | [**BillableMeasurement**](BillableMeasurement.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'AlertingActionResponse',
    'AzNsActionGroupResponse',
    'CriteriaResponse',
    'DimensionResponse',
    'LogMetricTriggerResponse',
    'LogToMetricActionResponse',
    'ScheduleResponse',
    'SourceResponse',
    'TriggerConditionResponse',
]

@pulumi.output_type
class AlertingActionResponse(dict):
    """
    Specify action need to be taken when rule type is Alert
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "odataType":
            suggest = "odata_type"
        elif key == "aznsAction":
            suggest = "azns_action"
        elif key == "throttlingInMin":
            suggest = "throttling_in_min"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AlertingActionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AlertingActionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AlertingActionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 odata_type: str,
                 severity: str,
                 trigger: 'outputs.TriggerConditionResponse',
                 azns_action: Optional['outputs.AzNsActionGroupResponse'] = None,
                 throttling_in_min: Optional[int] = None):
        """
        Specify action need to be taken when rule type is Alert
        :param str odata_type: Specifies the action. Supported values - AlertingAction, LogToMetricAction
               Expected value is 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction'.
        :param str severity: Severity of the alert
        :param 'TriggerConditionResponse' trigger: The trigger condition that results in the alert rule being.
        :param 'AzNsActionGroupResponse' azns_action: Azure action group reference.
        :param int throttling_in_min: time (in minutes) for which Alerts should be throttled or suppressed.
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction')
        pulumi.set(__self__, "severity", severity)
        pulumi.set(__self__, "trigger", trigger)
        if azns_action is not None:
            pulumi.set(__self__, "azns_action", azns_action)
        if throttling_in_min is not None:
            pulumi.set(__self__, "throttling_in_min", throttling_in_min)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        Specifies the action. Supported values - AlertingAction, LogToMetricAction
        Expected value is 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter
    def severity(self) -> str:
        """
        Severity of the alert
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter
    def trigger(self) -> 'outputs.TriggerConditionResponse':
        """
        The trigger condition that results in the alert rule being.
        """
        return pulumi.get(self, "trigger")

    @property
    @pulumi.getter(name="aznsAction")
    def azns_action(self) -> Optional['outputs.AzNsActionGroupResponse']:
        """
        Azure action group reference.
        """
        return pulumi.get(self, "azns_action")

    @property
    @pulumi.getter(name="throttlingInMin")
    def throttling_in_min(self) -> Optional[int]:
        """
        time (in minutes) for which Alerts should be throttled or suppressed.
        """
        return pulumi.get(self, "throttling_in_min")


@pulumi.output_type
class AzNsActionGroupResponse(dict):
    """
    Azure action group
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionGroup":
            suggest = "action_group"
        elif key == "customWebhookPayload":
            suggest = "custom_webhook_payload"
        elif key == "emailSubject":
            suggest = "email_subject"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AzNsActionGroupResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AzNsActionGroupResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AzNsActionGroupResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action_group: Optional[Sequence[str]] = None,
                 custom_webhook_payload: Optional[str] = None,
                 email_subject: Optional[str] = None):
        """
        Azure action group
        :param Sequence[str] action_group: Azure Action Group reference.
        :param str custom_webhook_payload: Custom payload to be sent for all webhook URI in Azure action group
        :param str email_subject: Custom subject override for all email ids in Azure action group
        """
        if action_group is not None:
            pulumi.set(__self__, "action_group", action_group)
        if custom_webhook_payload is not None:
            pulumi.set(__self__, "custom_webhook_payload", custom_webhook_payload)
        if email_subject is not None:
            pulumi.set(__self__, "email_subject", email_subject)

    @property
    @pulumi.getter(name="actionGroup")
    def action_group(self) -> Optional[Sequence[str]]:
        """
        Azure Action Group reference.
        """
        return pulumi.get(self, "action_group")

    @property
    @pulumi.getter(name="customWebhookPayload")
    def custom_webhook_payload(self) -> Optional[str]:
        """
        Custom payload to be sent for all webhook URI in Azure action group
        """
        return pulumi.get(self, "custom_webhook_payload")

    @property
    @pulumi.getter(name="emailSubject")
    def email_subject(self) -> Optional[str]:
        """
        Custom subject override for all email ids in Azure action group
        """
        return pulumi.get(self, "email_subject")


@pulumi.output_type
class CriteriaResponse(dict):
    """
    Specifies the criteria for converting log to metric.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricName":
            suggest = "metric_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CriteriaResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CriteriaResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CriteriaResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 metric_name: str,
                 dimensions: Optional[Sequence['outputs.DimensionResponse']] = None):
        """
        Specifies the criteria for converting log to metric.
        :param str metric_name: Name of the metric
        :param Sequence['DimensionResponse'] dimensions: List of Dimensions for creating metric
        """
        pulumi.set(__self__, "metric_name", metric_name)
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        """
        Name of the metric
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.DimensionResponse']]:
        """
        List of Dimensions for creating metric
        """
        return pulumi.get(self, "dimensions")


@pulumi.output_type
class DimensionResponse(dict):
    """
    Specifies the criteria for converting log to metric.
    """
    def __init__(__self__, *,
                 name: str,
                 operator: str,
                 values: Sequence[str]):
        """
        Specifies the criteria for converting log to metric.
        :param str name: Name of the dimension
        :param str operator: Operator for dimension values
        :param Sequence[str] values: List of dimension values
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the dimension
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def operator(self) -> str:
        """
        Operator for dimension values
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        List of dimension values
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class LogMetricTriggerResponse(dict):
    """
    A log metrics trigger descriptor.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricColumn":
            suggest = "metric_column"
        elif key == "metricTriggerType":
            suggest = "metric_trigger_type"
        elif key == "thresholdOperator":
            suggest = "threshold_operator"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LogMetricTriggerResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LogMetricTriggerResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LogMetricTriggerResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 metric_column: Optional[str] = None,
                 metric_trigger_type: Optional[str] = None,
                 threshold: Optional[float] = None,
                 threshold_operator: Optional[str] = None):
        """
        A log metrics trigger descriptor.
        :param str metric_column: Evaluation of metric on a particular column
        :param str metric_trigger_type: Metric Trigger Type - 'Consecutive' or 'Total'
        :param float threshold: The threshold of the metric trigger.
        :param str threshold_operator: Evaluation operation for Metric -'GreaterThan' or 'LessThan' or 'Equal'.
        """
        if metric_column is not None:
            pulumi.set(__self__, "metric_column", metric_column)
        if metric_trigger_type is not None:
            pulumi.set(__self__, "metric_trigger_type", metric_trigger_type)
        if threshold is not None:
            pulumi.set(__self__, "threshold", threshold)
        if threshold_operator is not None:
            pulumi.set(__self__, "threshold_operator", threshold_operator)

    @property
    @pulumi.getter(name="metricColumn")
    def metric_column(self) -> Optional[str]:
        """
        Evaluation of metric on a particular column
        """
        return pulumi.get(self, "metric_column")

    @property
    @pulumi.getter(name="metricTriggerType")
    def metric_trigger_type(self) -> Optional[str]:
        """
        Metric Trigger Type - 'Consecutive' or 'Total'
        """
        return pulumi.get(self, "metric_trigger_type")

    @property
    @pulumi.getter
    def threshold(self) -> Optional[float]:
        """
        The threshold of the metric trigger.
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter(name="thresholdOperator")
    def threshold_operator(self) -> Optional[str]:
        """
        Evaluation operation for Metric -'GreaterThan' or 'LessThan' or 'Equal'.
        """
        return pulumi.get(self, "threshold_operator")


@pulumi.output_type
class LogToMetricActionResponse(dict):
    """
    Specify action need to be taken when rule type is converting log to metric
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "odataType":
            suggest = "odata_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LogToMetricActionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LogToMetricActionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LogToMetricActionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 criteria: Sequence['outputs.CriteriaResponse'],
                 odata_type: str):
        """
        Specify action need to be taken when rule type is converting log to metric
        :param Sequence['CriteriaResponse'] criteria: Criteria of Metric
        :param str odata_type: Specifies the action. Supported values - AlertingAction, LogToMetricAction
               Expected value is 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.LogToMetricAction'.
        """
        pulumi.set(__self__, "criteria", criteria)
        pulumi.set(__self__, "odata_type", 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.LogToMetricAction')

    @property
    @pulumi.getter
    def criteria(self) -> Sequence['outputs.CriteriaResponse']:
        """
        Criteria of Metric
        """
        return pulumi.get(self, "criteria")

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        Specifies the action. Supported values - AlertingAction, LogToMetricAction
        Expected value is 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.LogToMetricAction'.
        """
        return pulumi.get(self, "odata_type")


@pulumi.output_type
class ScheduleResponse(dict):
    """
    Defines how often to run the search and the time interval.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "frequencyInMinutes":
            suggest = "frequency_in_minutes"
        elif key == "timeWindowInMinutes":
            suggest = "time_window_in_minutes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScheduleResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScheduleResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScheduleResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 frequency_in_minutes: int,
                 time_window_in_minutes: int):
        """
        Defines how often to run the search and the time interval.
        :param int frequency_in_minutes: frequency (in minutes) at which rule condition should be evaluated.
        :param int time_window_in_minutes: Time window for which data needs to be fetched for query (should be greater than or equal to frequencyInMinutes).
        """
        pulumi.set(__self__, "frequency_in_minutes", frequency_in_minutes)
        pulumi.set(__self__, "time_window_in_minutes", time_window_in_minutes)

    @property
    @pulumi.getter(name="frequencyInMinutes")
    def frequency_in_minutes(self) -> int:
        """
        frequency (in minutes) at which rule condition should be evaluated.
        """
        return pulumi.get(self, "frequency_in_minutes")

    @property
    @pulumi.getter(name="timeWindowInMinutes")
    def time_window_in_minutes(self) -> int:
        """
        Time window for which data needs to be fetched for query (should be greater than or equal to frequencyInMinutes).
        """
        return pulumi.get(self, "time_window_in_minutes")


@pulumi.output_type
class SourceResponse(dict):
    """
    Specifies the log search query.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dataSourceId":
            suggest = "data_source_id"
        elif key == "authorizedResources":
            suggest = "authorized_resources"
        elif key == "queryType":
            suggest = "query_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 data_source_id: str,
                 authorized_resources: Optional[Sequence[str]] = None,
                 query: Optional[str] = None,
                 query_type: Optional[str] = None):
        """
        Specifies the log search query.
        :param str data_source_id: The resource uri over which log search query is to be run.
        :param Sequence[str] authorized_resources: List of  Resource referred into query
        :param str query: Log search query. Required for action type - AlertingAction
        :param str query_type: Set value to 'ResultCount' .
        """
        pulumi.set(__self__, "data_source_id", data_source_id)
        if authorized_resources is not None:
            pulumi.set(__self__, "authorized_resources", authorized_resources)
        if query is not None:
            pulumi.set(__self__, "query", query)
        if query_type is not None:
            pulumi.set(__self__, "query_type", query_type)

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> str:
        """
        The resource uri over which log search query is to be run.
        """
        return pulumi.get(self, "data_source_id")

    @property
    @pulumi.getter(name="authorizedResources")
    def authorized_resources(self) -> Optional[Sequence[str]]:
        """
        List of  Resource referred into query
        """
        return pulumi.get(self, "authorized_resources")

    @property
    @pulumi.getter
    def query(self) -> Optional[str]:
        """
        Log search query. Required for action type - AlertingAction
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter(name="queryType")
    def query_type(self) -> Optional[str]:
        """
        Set value to 'ResultCount' .
        """
        return pulumi.get(self, "query_type")


@pulumi.output_type
class TriggerConditionResponse(dict):
    """
    The condition that results in the Log Search rule.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "thresholdOperator":
            suggest = "threshold_operator"
        elif key == "metricTrigger":
            suggest = "metric_trigger"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TriggerConditionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TriggerConditionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TriggerConditionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 threshold: float,
                 threshold_operator: str,
                 metric_trigger: Optional['outputs.LogMetricTriggerResponse'] = None):
        """
        The condition that results in the Log Search rule.
        :param float threshold: Result or count threshold based on which rule should be triggered.
        :param str threshold_operator: Evaluation operation for rule - 'GreaterThan' or 'LessThan.
        :param 'LogMetricTriggerResponse' metric_trigger: Trigger condition for metric query rule
        """
        pulumi.set(__self__, "threshold", threshold)
        pulumi.set(__self__, "threshold_operator", threshold_operator)
        if metric_trigger is not None:
            pulumi.set(__self__, "metric_trigger", metric_trigger)

    @property
    @pulumi.getter
    def threshold(self) -> float:
        """
        Result or count threshold based on which rule should be triggered.
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter(name="thresholdOperator")
    def threshold_operator(self) -> str:
        """
        Evaluation operation for rule - 'GreaterThan' or 'LessThan.
        """
        return pulumi.get(self, "threshold_operator")

    @property
    @pulumi.getter(name="metricTrigger")
    def metric_trigger(self) -> Optional['outputs.LogMetricTriggerResponse']:
        """
        Trigger condition for metric query rule
        """
        return pulumi.get(self, "metric_trigger")



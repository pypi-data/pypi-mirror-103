# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'ElasticCloudDeploymentResponse',
    'ElasticCloudUserResponse',
    'ElasticPropertiesResponse',
    'FilteringTagResponse',
    'IdentityPropertiesResponse',
    'LogRulesResponse',
    'MonitorPropertiesResponse',
    'MonitoredResourceResponse',
    'MonitoringTagRulesPropertiesResponse',
    'ResourceSkuResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class ElasticCloudDeploymentResponse(dict):
    """
    Details of the user's elastic deployment associated with the monitor resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "azureSubscriptionId":
            suggest = "azure_subscription_id"
        elif key == "deploymentId":
            suggest = "deployment_id"
        elif key == "elasticsearchRegion":
            suggest = "elasticsearch_region"
        elif key == "elasticsearchServiceUrl":
            suggest = "elasticsearch_service_url"
        elif key == "kibanaServiceUrl":
            suggest = "kibana_service_url"
        elif key == "kibanaSsoUrl":
            suggest = "kibana_sso_url"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ElasticCloudDeploymentResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ElasticCloudDeploymentResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ElasticCloudDeploymentResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 azure_subscription_id: str,
                 deployment_id: str,
                 elasticsearch_region: str,
                 elasticsearch_service_url: str,
                 kibana_service_url: str,
                 kibana_sso_url: str,
                 name: str):
        """
        Details of the user's elastic deployment associated with the monitor resource.
        :param str azure_subscription_id: Associated Azure subscription Id for the elastic deployment.
        :param str deployment_id: Elastic deployment Id
        :param str elasticsearch_region: Region where Deployment at Elastic side took place.
        :param str elasticsearch_service_url: Elasticsearch ingestion endpoint of the Elastic deployment.
        :param str kibana_service_url: Kibana endpoint of the Elastic deployment.
        :param str kibana_sso_url: Kibana dashboard sso URL of the Elastic deployment.
        :param str name: Elastic deployment name
        """
        pulumi.set(__self__, "azure_subscription_id", azure_subscription_id)
        pulumi.set(__self__, "deployment_id", deployment_id)
        pulumi.set(__self__, "elasticsearch_region", elasticsearch_region)
        pulumi.set(__self__, "elasticsearch_service_url", elasticsearch_service_url)
        pulumi.set(__self__, "kibana_service_url", kibana_service_url)
        pulumi.set(__self__, "kibana_sso_url", kibana_sso_url)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="azureSubscriptionId")
    def azure_subscription_id(self) -> str:
        """
        Associated Azure subscription Id for the elastic deployment.
        """
        return pulumi.get(self, "azure_subscription_id")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> str:
        """
        Elastic deployment Id
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter(name="elasticsearchRegion")
    def elasticsearch_region(self) -> str:
        """
        Region where Deployment at Elastic side took place.
        """
        return pulumi.get(self, "elasticsearch_region")

    @property
    @pulumi.getter(name="elasticsearchServiceUrl")
    def elasticsearch_service_url(self) -> str:
        """
        Elasticsearch ingestion endpoint of the Elastic deployment.
        """
        return pulumi.get(self, "elasticsearch_service_url")

    @property
    @pulumi.getter(name="kibanaServiceUrl")
    def kibana_service_url(self) -> str:
        """
        Kibana endpoint of the Elastic deployment.
        """
        return pulumi.get(self, "kibana_service_url")

    @property
    @pulumi.getter(name="kibanaSsoUrl")
    def kibana_sso_url(self) -> str:
        """
        Kibana dashboard sso URL of the Elastic deployment.
        """
        return pulumi.get(self, "kibana_sso_url")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Elastic deployment name
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class ElasticCloudUserResponse(dict):
    """
    Details of the user's elastic account.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "elasticCloudSsoDefaultUrl":
            suggest = "elastic_cloud_sso_default_url"
        elif key == "emailAddress":
            suggest = "email_address"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ElasticCloudUserResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ElasticCloudUserResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ElasticCloudUserResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 elastic_cloud_sso_default_url: str,
                 email_address: str,
                 id: str):
        """
        Details of the user's elastic account.
        :param str elastic_cloud_sso_default_url: Elastic cloud default dashboard sso URL of the Elastic user account.
        :param str email_address: Email of the Elastic User Account.
        :param str id: User Id of the elastic account of the User.
        """
        pulumi.set(__self__, "elastic_cloud_sso_default_url", elastic_cloud_sso_default_url)
        pulumi.set(__self__, "email_address", email_address)
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="elasticCloudSsoDefaultUrl")
    def elastic_cloud_sso_default_url(self) -> str:
        """
        Elastic cloud default dashboard sso URL of the Elastic user account.
        """
        return pulumi.get(self, "elastic_cloud_sso_default_url")

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> str:
        """
        Email of the Elastic User Account.
        """
        return pulumi.get(self, "email_address")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        User Id of the elastic account of the User.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class ElasticPropertiesResponse(dict):
    """
    Elastic Resource Properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "elasticCloudDeployment":
            suggest = "elastic_cloud_deployment"
        elif key == "elasticCloudUser":
            suggest = "elastic_cloud_user"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ElasticPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ElasticPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ElasticPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 elastic_cloud_deployment: Optional['outputs.ElasticCloudDeploymentResponse'] = None,
                 elastic_cloud_user: Optional['outputs.ElasticCloudUserResponse'] = None):
        """
        Elastic Resource Properties.
        :param 'ElasticCloudDeploymentResponse' elastic_cloud_deployment: Details of the elastic cloud deployment.
        :param 'ElasticCloudUserResponse' elastic_cloud_user: Details of the user's elastic account.
        """
        if elastic_cloud_deployment is not None:
            pulumi.set(__self__, "elastic_cloud_deployment", elastic_cloud_deployment)
        if elastic_cloud_user is not None:
            pulumi.set(__self__, "elastic_cloud_user", elastic_cloud_user)

    @property
    @pulumi.getter(name="elasticCloudDeployment")
    def elastic_cloud_deployment(self) -> Optional['outputs.ElasticCloudDeploymentResponse']:
        """
        Details of the elastic cloud deployment.
        """
        return pulumi.get(self, "elastic_cloud_deployment")

    @property
    @pulumi.getter(name="elasticCloudUser")
    def elastic_cloud_user(self) -> Optional['outputs.ElasticCloudUserResponse']:
        """
        Details of the user's elastic account.
        """
        return pulumi.get(self, "elastic_cloud_user")


@pulumi.output_type
class FilteringTagResponse(dict):
    """
    The definition of a filtering tag. Filtering tags are used for capturing resources and include/exclude them from being monitored.
    """
    def __init__(__self__, *,
                 action: Optional[str] = None,
                 name: Optional[str] = None,
                 value: Optional[str] = None):
        """
        The definition of a filtering tag. Filtering tags are used for capturing resources and include/exclude them from being monitored.
        :param str action: Valid actions for a filtering tag.
        :param str name: The name (also known as the key) of the tag.
        :param str value: The value of the tag.
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def action(self) -> Optional[str]:
        """
        Valid actions for a filtering tag.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name (also known as the key) of the tag.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        The value of the tag.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class IdentityPropertiesResponse(dict):
    """
    Identity properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentityPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentityPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentityPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None):
        """
        Identity properties.
        :param str principal_id: The identity ID.
        :param str tenant_id: The tenant ID of resource.
        :param str type: Managed identity type.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The identity ID.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Managed identity type.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class LogRulesResponse(dict):
    """
    Set of rules for sending logs for the Monitor resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "filteringTags":
            suggest = "filtering_tags"
        elif key == "sendAadLogs":
            suggest = "send_aad_logs"
        elif key == "sendActivityLogs":
            suggest = "send_activity_logs"
        elif key == "sendSubscriptionLogs":
            suggest = "send_subscription_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LogRulesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LogRulesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LogRulesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 filtering_tags: Optional[Sequence['outputs.FilteringTagResponse']] = None,
                 send_aad_logs: Optional[bool] = None,
                 send_activity_logs: Optional[bool] = None,
                 send_subscription_logs: Optional[bool] = None):
        """
        Set of rules for sending logs for the Monitor resource.
        :param Sequence['FilteringTagResponse'] filtering_tags: List of filtering tags to be used for capturing logs. This only takes effect if SendActivityLogs flag is enabled. If empty, all resources will be captured. If only Exclude action is specified, the rules will apply to the list of all available resources. If Include actions are specified, the rules will only include resources with the associated tags.
        :param bool send_aad_logs: Flag specifying if AAD logs should be sent for the Monitor resource.
        :param bool send_activity_logs: Flag specifying if activity logs from Azure resources should be sent for the Monitor resource.
        :param bool send_subscription_logs: Flag specifying if subscription logs should be sent for the Monitor resource.
        """
        if filtering_tags is not None:
            pulumi.set(__self__, "filtering_tags", filtering_tags)
        if send_aad_logs is not None:
            pulumi.set(__self__, "send_aad_logs", send_aad_logs)
        if send_activity_logs is not None:
            pulumi.set(__self__, "send_activity_logs", send_activity_logs)
        if send_subscription_logs is not None:
            pulumi.set(__self__, "send_subscription_logs", send_subscription_logs)

    @property
    @pulumi.getter(name="filteringTags")
    def filtering_tags(self) -> Optional[Sequence['outputs.FilteringTagResponse']]:
        """
        List of filtering tags to be used for capturing logs. This only takes effect if SendActivityLogs flag is enabled. If empty, all resources will be captured. If only Exclude action is specified, the rules will apply to the list of all available resources. If Include actions are specified, the rules will only include resources with the associated tags.
        """
        return pulumi.get(self, "filtering_tags")

    @property
    @pulumi.getter(name="sendAadLogs")
    def send_aad_logs(self) -> Optional[bool]:
        """
        Flag specifying if AAD logs should be sent for the Monitor resource.
        """
        return pulumi.get(self, "send_aad_logs")

    @property
    @pulumi.getter(name="sendActivityLogs")
    def send_activity_logs(self) -> Optional[bool]:
        """
        Flag specifying if activity logs from Azure resources should be sent for the Monitor resource.
        """
        return pulumi.get(self, "send_activity_logs")

    @property
    @pulumi.getter(name="sendSubscriptionLogs")
    def send_subscription_logs(self) -> Optional[bool]:
        """
        Flag specifying if subscription logs should be sent for the Monitor resource.
        """
        return pulumi.get(self, "send_subscription_logs")


@pulumi.output_type
class MonitorPropertiesResponse(dict):
    """
    Properties specific to the monitor resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "liftrResourceCategory":
            suggest = "liftr_resource_category"
        elif key == "liftrResourcePreference":
            suggest = "liftr_resource_preference"
        elif key == "elasticProperties":
            suggest = "elastic_properties"
        elif key == "monitoringStatus":
            suggest = "monitoring_status"
        elif key == "provisioningState":
            suggest = "provisioning_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 liftr_resource_category: str,
                 liftr_resource_preference: int,
                 elastic_properties: Optional['outputs.ElasticPropertiesResponse'] = None,
                 monitoring_status: Optional[str] = None,
                 provisioning_state: Optional[str] = None):
        """
        Properties specific to the monitor resource.
        :param int liftr_resource_preference: The priority of the resource.
        :param 'ElasticPropertiesResponse' elastic_properties: Elastic cloud properties.
        :param str monitoring_status: Flag specifying if the resource monitoring is enabled or disabled.
        :param str provisioning_state: Provisioning state of the monitor resource.
        """
        pulumi.set(__self__, "liftr_resource_category", liftr_resource_category)
        pulumi.set(__self__, "liftr_resource_preference", liftr_resource_preference)
        if elastic_properties is not None:
            pulumi.set(__self__, "elastic_properties", elastic_properties)
        if monitoring_status is not None:
            pulumi.set(__self__, "monitoring_status", monitoring_status)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter(name="liftrResourceCategory")
    def liftr_resource_category(self) -> str:
        return pulumi.get(self, "liftr_resource_category")

    @property
    @pulumi.getter(name="liftrResourcePreference")
    def liftr_resource_preference(self) -> int:
        """
        The priority of the resource.
        """
        return pulumi.get(self, "liftr_resource_preference")

    @property
    @pulumi.getter(name="elasticProperties")
    def elastic_properties(self) -> Optional['outputs.ElasticPropertiesResponse']:
        """
        Elastic cloud properties.
        """
        return pulumi.get(self, "elastic_properties")

    @property
    @pulumi.getter(name="monitoringStatus")
    def monitoring_status(self) -> Optional[str]:
        """
        Flag specifying if the resource monitoring is enabled or disabled.
        """
        return pulumi.get(self, "monitoring_status")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning state of the monitor resource.
        """
        return pulumi.get(self, "provisioning_state")


@pulumi.output_type
class MonitoredResourceResponse(dict):
    """
    The properties of a resource currently being monitored by the Elastic monitor resource.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None,
                 reason_for_logs_status: Optional[str] = None,
                 sending_logs: Optional[str] = None):
        """
        The properties of a resource currently being monitored by the Elastic monitor resource.
        :param str id: The ARM id of the resource.
        :param str reason_for_logs_status: Reason for why the resource is sending logs (or why it is not sending).
        :param str sending_logs: Flag indicating the status of the resource for sending logs operation to Elastic.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if reason_for_logs_status is not None:
            pulumi.set(__self__, "reason_for_logs_status", reason_for_logs_status)
        if sending_logs is not None:
            pulumi.set(__self__, "sending_logs", sending_logs)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ARM id of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="reasonForLogsStatus")
    def reason_for_logs_status(self) -> Optional[str]:
        """
        Reason for why the resource is sending logs (or why it is not sending).
        """
        return pulumi.get(self, "reason_for_logs_status")

    @property
    @pulumi.getter(name="sendingLogs")
    def sending_logs(self) -> Optional[str]:
        """
        Flag indicating the status of the resource for sending logs operation to Elastic.
        """
        return pulumi.get(self, "sending_logs")


@pulumi.output_type
class MonitoringTagRulesPropertiesResponse(dict):
    """
    Definition of the properties for a TagRules resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logRules":
            suggest = "log_rules"
        elif key == "provisioningState":
            suggest = "provisioning_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitoringTagRulesPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitoringTagRulesPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitoringTagRulesPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_rules: Optional['outputs.LogRulesResponse'] = None,
                 provisioning_state: Optional[str] = None):
        """
        Definition of the properties for a TagRules resource.
        :param 'LogRulesResponse' log_rules: Rules for sending logs.
        :param str provisioning_state: Provisioning state of the monitoring tag rules.
        """
        if log_rules is not None:
            pulumi.set(__self__, "log_rules", log_rules)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter(name="logRules")
    def log_rules(self) -> Optional['outputs.LogRulesResponse']:
        """
        Rules for sending logs.
        """
        return pulumi.get(self, "log_rules")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning state of the monitoring tag rules.
        """
        return pulumi.get(self, "provisioning_state")


@pulumi.output_type
class ResourceSkuResponse(dict):
    """
    Microsoft.Elastic SKU.
    """
    def __init__(__self__, *,
                 name: str):
        """
        Microsoft.Elastic SKU.
        :param str name: Name of the SKU.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the SKU.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")



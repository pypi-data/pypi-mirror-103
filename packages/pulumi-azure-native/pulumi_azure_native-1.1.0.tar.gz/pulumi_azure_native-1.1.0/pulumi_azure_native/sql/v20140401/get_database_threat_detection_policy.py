# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetDatabaseThreatDetectionPolicyResult',
    'AwaitableGetDatabaseThreatDetectionPolicyResult',
    'get_database_threat_detection_policy',
]

@pulumi.output_type
class GetDatabaseThreatDetectionPolicyResult:
    """
    Contains information about a database Threat Detection policy.
    """
    def __init__(__self__, disabled_alerts=None, email_account_admins=None, email_addresses=None, id=None, kind=None, location=None, name=None, retention_days=None, state=None, storage_endpoint=None, type=None, use_server_default=None):
        if disabled_alerts and not isinstance(disabled_alerts, str):
            raise TypeError("Expected argument 'disabled_alerts' to be a str")
        pulumi.set(__self__, "disabled_alerts", disabled_alerts)
        if email_account_admins and not isinstance(email_account_admins, str):
            raise TypeError("Expected argument 'email_account_admins' to be a str")
        pulumi.set(__self__, "email_account_admins", email_account_admins)
        if email_addresses and not isinstance(email_addresses, str):
            raise TypeError("Expected argument 'email_addresses' to be a str")
        pulumi.set(__self__, "email_addresses", email_addresses)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if retention_days and not isinstance(retention_days, int):
            raise TypeError("Expected argument 'retention_days' to be a int")
        pulumi.set(__self__, "retention_days", retention_days)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if storage_endpoint and not isinstance(storage_endpoint, str):
            raise TypeError("Expected argument 'storage_endpoint' to be a str")
        pulumi.set(__self__, "storage_endpoint", storage_endpoint)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if use_server_default and not isinstance(use_server_default, str):
            raise TypeError("Expected argument 'use_server_default' to be a str")
        pulumi.set(__self__, "use_server_default", use_server_default)

    @property
    @pulumi.getter(name="disabledAlerts")
    def disabled_alerts(self) -> Optional[str]:
        """
        Specifies the semicolon-separated list of alerts that are disabled, or empty string to disable no alerts. Possible values: Sql_Injection; Sql_Injection_Vulnerability; Access_Anomaly; Data_Exfiltration; Unsafe_Action.
        """
        return pulumi.get(self, "disabled_alerts")

    @property
    @pulumi.getter(name="emailAccountAdmins")
    def email_account_admins(self) -> Optional[str]:
        """
        Specifies that the alert is sent to the account administrators.
        """
        return pulumi.get(self, "email_account_admins")

    @property
    @pulumi.getter(name="emailAddresses")
    def email_addresses(self) -> Optional[str]:
        """
        Specifies the semicolon-separated list of e-mail addresses to which the alert is sent.
        """
        return pulumi.get(self, "email_addresses")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Resource kind.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="retentionDays")
    def retention_days(self) -> Optional[int]:
        """
        Specifies the number of days to keep in the Threat Detection audit logs.
        """
        return pulumi.get(self, "retention_days")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Specifies the state of the policy. If state is Enabled, storageEndpoint and storageAccountAccessKey are required.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageEndpoint")
    def storage_endpoint(self) -> Optional[str]:
        """
        Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net). This blob storage will hold all Threat Detection audit logs. If state is Enabled, storageEndpoint is required.
        """
        return pulumi.get(self, "storage_endpoint")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="useServerDefault")
    def use_server_default(self) -> Optional[str]:
        """
        Specifies whether to use the default server policy.
        """
        return pulumi.get(self, "use_server_default")


class AwaitableGetDatabaseThreatDetectionPolicyResult(GetDatabaseThreatDetectionPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatabaseThreatDetectionPolicyResult(
            disabled_alerts=self.disabled_alerts,
            email_account_admins=self.email_account_admins,
            email_addresses=self.email_addresses,
            id=self.id,
            kind=self.kind,
            location=self.location,
            name=self.name,
            retention_days=self.retention_days,
            state=self.state,
            storage_endpoint=self.storage_endpoint,
            type=self.type,
            use_server_default=self.use_server_default)


def get_database_threat_detection_policy(database_name: Optional[str] = None,
                                         resource_group_name: Optional[str] = None,
                                         security_alert_policy_name: Optional[str] = None,
                                         server_name: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDatabaseThreatDetectionPolicyResult:
    """
    Contains information about a database Threat Detection policy.


    :param str database_name: The name of the database for which database Threat Detection policy is defined.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str security_alert_policy_name: The name of the security alert policy.
    :param str server_name: The name of the server.
    """
    __args__ = dict()
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['securityAlertPolicyName'] = security_alert_policy_name
    __args__['serverName'] = server_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:sql/v20140401:getDatabaseThreatDetectionPolicy', __args__, opts=opts, typ=GetDatabaseThreatDetectionPolicyResult).value

    return AwaitableGetDatabaseThreatDetectionPolicyResult(
        disabled_alerts=__ret__.disabled_alerts,
        email_account_admins=__ret__.email_account_admins,
        email_addresses=__ret__.email_addresses,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        retention_days=__ret__.retention_days,
        state=__ret__.state,
        storage_endpoint=__ret__.storage_endpoint,
        type=__ret__.type,
        use_server_default=__ret__.use_server_default)

# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'DatadogOrganizationPropertiesArgs',
    'IdentityPropertiesArgs',
    'MonitorPropertiesArgs',
    'ResourceSkuArgs',
    'UserInfoArgs',
]

@pulumi.input_type
class DatadogOrganizationPropertiesArgs:
    def __init__(__self__, *,
                 api_key: Optional[pulumi.Input[str]] = None,
                 application_key: Optional[pulumi.Input[str]] = None,
                 enterprise_app_id: Optional[pulumi.Input[str]] = None,
                 linking_auth_code: Optional[pulumi.Input[str]] = None,
                 linking_client_id: Optional[pulumi.Input[str]] = None,
                 redirect_uri: Optional[pulumi.Input[str]] = None):
        """
        Datadog organization properties
        :param pulumi.Input[str] api_key: Api key associated to the Datadog organization.
        :param pulumi.Input[str] application_key: Application key associated to the Datadog organization.
        :param pulumi.Input[str] enterprise_app_id: The Id of the Enterprise App used for Single sign on.
        :param pulumi.Input[str] linking_auth_code: The auth code used to linking to an existing datadog organization.
        :param pulumi.Input[str] linking_client_id: The client_id from an existing in exchange for an auth token to link organization.
        :param pulumi.Input[str] redirect_uri: The redirect uri for linking.
        """
        if api_key is not None:
            pulumi.set(__self__, "api_key", api_key)
        if application_key is not None:
            pulumi.set(__self__, "application_key", application_key)
        if enterprise_app_id is not None:
            pulumi.set(__self__, "enterprise_app_id", enterprise_app_id)
        if linking_auth_code is not None:
            pulumi.set(__self__, "linking_auth_code", linking_auth_code)
        if linking_client_id is not None:
            pulumi.set(__self__, "linking_client_id", linking_client_id)
        if redirect_uri is not None:
            pulumi.set(__self__, "redirect_uri", redirect_uri)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> Optional[pulumi.Input[str]]:
        """
        Api key associated to the Datadog organization.
        """
        return pulumi.get(self, "api_key")

    @api_key.setter
    def api_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_key", value)

    @property
    @pulumi.getter(name="applicationKey")
    def application_key(self) -> Optional[pulumi.Input[str]]:
        """
        Application key associated to the Datadog organization.
        """
        return pulumi.get(self, "application_key")

    @application_key.setter
    def application_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_key", value)

    @property
    @pulumi.getter(name="enterpriseAppId")
    def enterprise_app_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of the Enterprise App used for Single sign on.
        """
        return pulumi.get(self, "enterprise_app_id")

    @enterprise_app_id.setter
    def enterprise_app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enterprise_app_id", value)

    @property
    @pulumi.getter(name="linkingAuthCode")
    def linking_auth_code(self) -> Optional[pulumi.Input[str]]:
        """
        The auth code used to linking to an existing datadog organization.
        """
        return pulumi.get(self, "linking_auth_code")

    @linking_auth_code.setter
    def linking_auth_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "linking_auth_code", value)

    @property
    @pulumi.getter(name="linkingClientId")
    def linking_client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The client_id from an existing in exchange for an auth token to link organization.
        """
        return pulumi.get(self, "linking_client_id")

    @linking_client_id.setter
    def linking_client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "linking_client_id", value)

    @property
    @pulumi.getter(name="redirectUri")
    def redirect_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The redirect uri for linking.
        """
        return pulumi.get(self, "redirect_uri")

    @redirect_uri.setter
    def redirect_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "redirect_uri", value)


@pulumi.input_type
class IdentityPropertiesArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input[Union[str, 'ManagedIdentityTypes']]] = None):
        """
        :param pulumi.Input[Union[str, 'ManagedIdentityTypes']] type: Identity type
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ManagedIdentityTypes']]]:
        """
        Identity type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ManagedIdentityTypes']]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class MonitorPropertiesArgs:
    def __init__(__self__, *,
                 datadog_organization_properties: Optional[pulumi.Input['DatadogOrganizationPropertiesArgs']] = None,
                 monitoring_status: Optional[pulumi.Input[Union[str, 'MonitoringStatus']]] = None,
                 user_info: Optional[pulumi.Input['UserInfoArgs']] = None):
        """
        Properties specific to the monitor resource.
        :param pulumi.Input['DatadogOrganizationPropertiesArgs'] datadog_organization_properties: Datadog organization properties
        :param pulumi.Input[Union[str, 'MonitoringStatus']] monitoring_status: Flag specifying if the resource monitoring is enabled or disabled.
        :param pulumi.Input['UserInfoArgs'] user_info: User info
        """
        if datadog_organization_properties is not None:
            pulumi.set(__self__, "datadog_organization_properties", datadog_organization_properties)
        if monitoring_status is not None:
            pulumi.set(__self__, "monitoring_status", monitoring_status)
        if user_info is not None:
            pulumi.set(__self__, "user_info", user_info)

    @property
    @pulumi.getter(name="datadogOrganizationProperties")
    def datadog_organization_properties(self) -> Optional[pulumi.Input['DatadogOrganizationPropertiesArgs']]:
        """
        Datadog organization properties
        """
        return pulumi.get(self, "datadog_organization_properties")

    @datadog_organization_properties.setter
    def datadog_organization_properties(self, value: Optional[pulumi.Input['DatadogOrganizationPropertiesArgs']]):
        pulumi.set(self, "datadog_organization_properties", value)

    @property
    @pulumi.getter(name="monitoringStatus")
    def monitoring_status(self) -> Optional[pulumi.Input[Union[str, 'MonitoringStatus']]]:
        """
        Flag specifying if the resource monitoring is enabled or disabled.
        """
        return pulumi.get(self, "monitoring_status")

    @monitoring_status.setter
    def monitoring_status(self, value: Optional[pulumi.Input[Union[str, 'MonitoringStatus']]]):
        pulumi.set(self, "monitoring_status", value)

    @property
    @pulumi.getter(name="userInfo")
    def user_info(self) -> Optional[pulumi.Input['UserInfoArgs']]:
        """
        User info
        """
        return pulumi.get(self, "user_info")

    @user_info.setter
    def user_info(self, value: Optional[pulumi.Input['UserInfoArgs']]):
        pulumi.set(self, "user_info", value)


@pulumi.input_type
class ResourceSkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: Name of the SKU.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the SKU.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class UserInfoArgs:
    def __init__(__self__, *,
                 email_address: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 phone_number: Optional[pulumi.Input[str]] = None):
        """
        User info
        :param pulumi.Input[str] email_address: Email of the user used by Datadog for contacting them if needed
        :param pulumi.Input[str] name: Name of the user
        :param pulumi.Input[str] phone_number: Phone number of the user used by Datadog for contacting them if needed
        """
        if email_address is not None:
            pulumi.set(__self__, "email_address", email_address)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if phone_number is not None:
            pulumi.set(__self__, "phone_number", phone_number)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> Optional[pulumi.Input[str]]:
        """
        Email of the user used by Datadog for contacting them if needed
        """
        return pulumi.get(self, "email_address")

    @email_address.setter
    def email_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_address", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the user
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="phoneNumber")
    def phone_number(self) -> Optional[pulumi.Input[str]]:
        """
        Phone number of the user used by Datadog for contacting them if needed
        """
        return pulumi.get(self, "phone_number")

    @phone_number.setter
    def phone_number(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "phone_number", value)



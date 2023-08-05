# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['RegistrationDefinitionArgs', 'RegistrationDefinition']

@pulumi.input_type
class RegistrationDefinitionArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 plan: Optional[pulumi.Input['PlanArgs']] = None,
                 properties: Optional[pulumi.Input['RegistrationDefinitionPropertiesArgs']] = None,
                 registration_definition_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RegistrationDefinition resource.
        :param pulumi.Input[str] scope: Scope of the resource.
        :param pulumi.Input['PlanArgs'] plan: Plan details for the managed services.
        :param pulumi.Input['RegistrationDefinitionPropertiesArgs'] properties: Properties of a registration definition.
        :param pulumi.Input[str] registration_definition_id: Guid of the registration definition.
        """
        pulumi.set(__self__, "scope", scope)
        if plan is not None:
            pulumi.set(__self__, "plan", plan)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if registration_definition_id is not None:
            pulumi.set(__self__, "registration_definition_id", registration_definition_id)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        Scope of the resource.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def plan(self) -> Optional[pulumi.Input['PlanArgs']]:
        """
        Plan details for the managed services.
        """
        return pulumi.get(self, "plan")

    @plan.setter
    def plan(self, value: Optional[pulumi.Input['PlanArgs']]):
        pulumi.set(self, "plan", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['RegistrationDefinitionPropertiesArgs']]:
        """
        Properties of a registration definition.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['RegistrationDefinitionPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="registrationDefinitionId")
    def registration_definition_id(self) -> Optional[pulumi.Input[str]]:
        """
        Guid of the registration definition.
        """
        return pulumi.get(self, "registration_definition_id")

    @registration_definition_id.setter
    def registration_definition_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "registration_definition_id", value)


class RegistrationDefinition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 plan: Optional[pulumi.Input[pulumi.InputType['PlanArgs']]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['RegistrationDefinitionPropertiesArgs']]] = None,
                 registration_definition_id: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Registration definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PlanArgs']] plan: Plan details for the managed services.
        :param pulumi.Input[pulumi.InputType['RegistrationDefinitionPropertiesArgs']] properties: Properties of a registration definition.
        :param pulumi.Input[str] registration_definition_id: Guid of the registration definition.
        :param pulumi.Input[str] scope: Scope of the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegistrationDefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Registration definition.

        :param str resource_name: The name of the resource.
        :param RegistrationDefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegistrationDefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 plan: Optional[pulumi.Input[pulumi.InputType['PlanArgs']]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['RegistrationDefinitionPropertiesArgs']]] = None,
                 registration_definition_id: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RegistrationDefinitionArgs.__new__(RegistrationDefinitionArgs)

            __props__.__dict__["plan"] = plan
            __props__.__dict__["properties"] = properties
            __props__.__dict__["registration_definition_id"] = registration_definition_id
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:managedservices/v20190401preview:RegistrationDefinition"), pulumi.Alias(type_="azure-native:managedservices:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices:RegistrationDefinition"), pulumi.Alias(type_="azure-native:managedservices/v20180601preview:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/v20180601preview:RegistrationDefinition"), pulumi.Alias(type_="azure-native:managedservices/v20190601:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/v20190601:RegistrationDefinition"), pulumi.Alias(type_="azure-native:managedservices/v20190901:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/v20190901:RegistrationDefinition"), pulumi.Alias(type_="azure-native:managedservices/v20200201preview:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/v20200201preview:RegistrationDefinition")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(RegistrationDefinition, __self__).__init__(
            'azure-native:managedservices/v20190401preview:RegistrationDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RegistrationDefinition':
        """
        Get an existing RegistrationDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RegistrationDefinitionArgs.__new__(RegistrationDefinitionArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["plan"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return RegistrationDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the registration definition.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def plan(self) -> pulumi.Output[Optional['outputs.PlanResponse']]:
        """
        Plan details for the managed services.
        """
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.RegistrationDefinitionPropertiesResponse']:
        """
        Properties of a registration definition.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource.
        """
        return pulumi.get(self, "type")


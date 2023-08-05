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
from ._inputs import *

__all__ = ['SkusArgs', 'Skus']

@pulumi.input_type
class SkusArgs:
    def __init__(__self__, *,
                 provider_namespace: pulumi.Input[str],
                 resource_type: pulumi.Input[str],
                 sku_settings: pulumi.Input[Sequence[pulumi.Input['SkuSettingArgs']]],
                 sku: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Skus resource.
        :param pulumi.Input[str] provider_namespace: The name of the resource provider hosted within ProviderHub.
        :param pulumi.Input[str] resource_type: The resource type.
        :param pulumi.Input[str] sku: The SKU.
        """
        pulumi.set(__self__, "provider_namespace", provider_namespace)
        pulumi.set(__self__, "resource_type", resource_type)
        pulumi.set(__self__, "sku_settings", sku_settings)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)

    @property
    @pulumi.getter(name="providerNamespace")
    def provider_namespace(self) -> pulumi.Input[str]:
        """
        The name of the resource provider hosted within ProviderHub.
        """
        return pulumi.get(self, "provider_namespace")

    @provider_namespace.setter
    def provider_namespace(self, value: pulumi.Input[str]):
        pulumi.set(self, "provider_namespace", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Input[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter(name="skuSettings")
    def sku_settings(self) -> pulumi.Input[Sequence[pulumi.Input['SkuSettingArgs']]]:
        return pulumi.get(self, "sku_settings")

    @sku_settings.setter
    def sku_settings(self, value: pulumi.Input[Sequence[pulumi.Input['SkuSettingArgs']]]):
        pulumi.set(self, "sku_settings", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input[str]]:
        """
        The SKU.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku", value)


class Skus(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 provider_namespace: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 sku_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SkuSettingArgs']]]]] = None,
                 __props__=None):
        """
        Create a Skus resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] provider_namespace: The name of the resource provider hosted within ProviderHub.
        :param pulumi.Input[str] resource_type: The resource type.
        :param pulumi.Input[str] sku: The SKU.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SkusArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Skus resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param SkusArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SkusArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 provider_namespace: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 sku_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SkuSettingArgs']]]]] = None,
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
            __props__ = SkusArgs.__new__(SkusArgs)

            if provider_namespace is None and not opts.urn:
                raise TypeError("Missing required property 'provider_namespace'")
            __props__.__dict__["provider_namespace"] = provider_namespace
            if resource_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_type'")
            __props__.__dict__["resource_type"] = resource_type
            __props__.__dict__["sku"] = sku
            if sku_settings is None and not opts.urn:
                raise TypeError("Missing required property 'sku_settings'")
            __props__.__dict__["sku_settings"] = sku_settings
            __props__.__dict__["name"] = None
            __props__.__dict__["properties"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:providerhub/v20201120:Skus"), pulumi.Alias(type_="azure-native:providerhub:Skus"), pulumi.Alias(type_="azure-nextgen:providerhub:Skus")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Skus, __self__).__init__(
            'azure-native:providerhub/v20201120:Skus',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Skus':
        """
        Get an existing Skus resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SkusArgs.__new__(SkusArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return Skus(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.SkuResourceResponseProperties']:
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetProductResult',
    'AwaitableGetProductResult',
    'get_product',
]

@pulumi.output_type
class GetProductResult:
    """
    Product information.
    """
    def __init__(__self__, billing_part_number=None, compatibility=None, description=None, display_name=None, gallery_item_identity=None, icon_uris=None, id=None, legal_terms=None, links=None, name=None, offer=None, offer_version=None, payload_length=None, privacy_policy=None, product_kind=None, product_properties=None, publisher_display_name=None, publisher_identifier=None, sku=None, type=None, vm_extension_type=None):
        if billing_part_number and not isinstance(billing_part_number, str):
            raise TypeError("Expected argument 'billing_part_number' to be a str")
        pulumi.set(__self__, "billing_part_number", billing_part_number)
        if compatibility and not isinstance(compatibility, dict):
            raise TypeError("Expected argument 'compatibility' to be a dict")
        pulumi.set(__self__, "compatibility", compatibility)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if gallery_item_identity and not isinstance(gallery_item_identity, str):
            raise TypeError("Expected argument 'gallery_item_identity' to be a str")
        pulumi.set(__self__, "gallery_item_identity", gallery_item_identity)
        if icon_uris and not isinstance(icon_uris, dict):
            raise TypeError("Expected argument 'icon_uris' to be a dict")
        pulumi.set(__self__, "icon_uris", icon_uris)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if legal_terms and not isinstance(legal_terms, str):
            raise TypeError("Expected argument 'legal_terms' to be a str")
        pulumi.set(__self__, "legal_terms", legal_terms)
        if links and not isinstance(links, list):
            raise TypeError("Expected argument 'links' to be a list")
        pulumi.set(__self__, "links", links)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if offer and not isinstance(offer, str):
            raise TypeError("Expected argument 'offer' to be a str")
        pulumi.set(__self__, "offer", offer)
        if offer_version and not isinstance(offer_version, str):
            raise TypeError("Expected argument 'offer_version' to be a str")
        pulumi.set(__self__, "offer_version", offer_version)
        if payload_length and not isinstance(payload_length, float):
            raise TypeError("Expected argument 'payload_length' to be a float")
        pulumi.set(__self__, "payload_length", payload_length)
        if privacy_policy and not isinstance(privacy_policy, str):
            raise TypeError("Expected argument 'privacy_policy' to be a str")
        pulumi.set(__self__, "privacy_policy", privacy_policy)
        if product_kind and not isinstance(product_kind, str):
            raise TypeError("Expected argument 'product_kind' to be a str")
        pulumi.set(__self__, "product_kind", product_kind)
        if product_properties and not isinstance(product_properties, dict):
            raise TypeError("Expected argument 'product_properties' to be a dict")
        pulumi.set(__self__, "product_properties", product_properties)
        if publisher_display_name and not isinstance(publisher_display_name, str):
            raise TypeError("Expected argument 'publisher_display_name' to be a str")
        pulumi.set(__self__, "publisher_display_name", publisher_display_name)
        if publisher_identifier and not isinstance(publisher_identifier, str):
            raise TypeError("Expected argument 'publisher_identifier' to be a str")
        pulumi.set(__self__, "publisher_identifier", publisher_identifier)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vm_extension_type and not isinstance(vm_extension_type, str):
            raise TypeError("Expected argument 'vm_extension_type' to be a str")
        pulumi.set(__self__, "vm_extension_type", vm_extension_type)

    @property
    @pulumi.getter(name="billingPartNumber")
    def billing_part_number(self) -> Optional[str]:
        """
        The part number used for billing purposes.
        """
        return pulumi.get(self, "billing_part_number")

    @property
    @pulumi.getter
    def compatibility(self) -> Optional['outputs.CompatibilityResponse']:
        """
        Product compatibility with current device.
        """
        return pulumi.get(self, "compatibility")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the product.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name of the product.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="galleryItemIdentity")
    def gallery_item_identity(self) -> Optional[str]:
        """
        The identifier of the gallery item corresponding to the product.
        """
        return pulumi.get(self, "gallery_item_identity")

    @property
    @pulumi.getter(name="iconUris")
    def icon_uris(self) -> Optional['outputs.IconUrisResponse']:
        """
        Additional links available for this product.
        """
        return pulumi.get(self, "icon_uris")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="legalTerms")
    def legal_terms(self) -> Optional[str]:
        """
        The legal terms.
        """
        return pulumi.get(self, "legal_terms")

    @property
    @pulumi.getter
    def links(self) -> Optional[Sequence['outputs.ProductLinkResponse']]:
        """
        Additional links available for this product.
        """
        return pulumi.get(self, "links")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def offer(self) -> Optional[str]:
        """
        The offer representing the product.
        """
        return pulumi.get(self, "offer")

    @property
    @pulumi.getter(name="offerVersion")
    def offer_version(self) -> Optional[str]:
        """
        The version of the product offer.
        """
        return pulumi.get(self, "offer_version")

    @property
    @pulumi.getter(name="payloadLength")
    def payload_length(self) -> Optional[float]:
        """
        The length of product content.
        """
        return pulumi.get(self, "payload_length")

    @property
    @pulumi.getter(name="privacyPolicy")
    def privacy_policy(self) -> Optional[str]:
        """
        The privacy policy.
        """
        return pulumi.get(self, "privacy_policy")

    @property
    @pulumi.getter(name="productKind")
    def product_kind(self) -> Optional[str]:
        """
        The kind of the product (virtualMachine or virtualMachineExtension)
        """
        return pulumi.get(self, "product_kind")

    @property
    @pulumi.getter(name="productProperties")
    def product_properties(self) -> Optional['outputs.ProductPropertiesResponse']:
        """
        Additional properties for the product.
        """
        return pulumi.get(self, "product_properties")

    @property
    @pulumi.getter(name="publisherDisplayName")
    def publisher_display_name(self) -> Optional[str]:
        """
        The user-friendly name of the product publisher.
        """
        return pulumi.get(self, "publisher_display_name")

    @property
    @pulumi.getter(name="publisherIdentifier")
    def publisher_identifier(self) -> Optional[str]:
        """
        Publisher identifier.
        """
        return pulumi.get(self, "publisher_identifier")

    @property
    @pulumi.getter
    def sku(self) -> Optional[str]:
        """
        The product SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vmExtensionType")
    def vm_extension_type(self) -> Optional[str]:
        """
        The type of the Virtual Machine Extension.
        """
        return pulumi.get(self, "vm_extension_type")


class AwaitableGetProductResult(GetProductResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProductResult(
            billing_part_number=self.billing_part_number,
            compatibility=self.compatibility,
            description=self.description,
            display_name=self.display_name,
            gallery_item_identity=self.gallery_item_identity,
            icon_uris=self.icon_uris,
            id=self.id,
            legal_terms=self.legal_terms,
            links=self.links,
            name=self.name,
            offer=self.offer,
            offer_version=self.offer_version,
            payload_length=self.payload_length,
            privacy_policy=self.privacy_policy,
            product_kind=self.product_kind,
            product_properties=self.product_properties,
            publisher_display_name=self.publisher_display_name,
            publisher_identifier=self.publisher_identifier,
            sku=self.sku,
            type=self.type,
            vm_extension_type=self.vm_extension_type)


def get_product(product_name: Optional[str] = None,
                registration_name: Optional[str] = None,
                resource_group: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProductResult:
    """
    Product information.


    :param str product_name: Name of the product.
    :param str registration_name: Name of the Azure Stack registration.
    :param str resource_group: Name of the resource group.
    """
    __args__ = dict()
    __args__['productName'] = product_name
    __args__['registrationName'] = registration_name
    __args__['resourceGroup'] = resource_group
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:azurestack/v20160101:getProduct', __args__, opts=opts, typ=GetProductResult).value

    return AwaitableGetProductResult(
        billing_part_number=__ret__.billing_part_number,
        compatibility=__ret__.compatibility,
        description=__ret__.description,
        display_name=__ret__.display_name,
        gallery_item_identity=__ret__.gallery_item_identity,
        icon_uris=__ret__.icon_uris,
        id=__ret__.id,
        legal_terms=__ret__.legal_terms,
        links=__ret__.links,
        name=__ret__.name,
        offer=__ret__.offer,
        offer_version=__ret__.offer_version,
        payload_length=__ret__.payload_length,
        privacy_policy=__ret__.privacy_policy,
        product_kind=__ret__.product_kind,
        product_properties=__ret__.product_properties,
        publisher_display_name=__ret__.publisher_display_name,
        publisher_identifier=__ret__.publisher_identifier,
        sku=__ret__.sku,
        type=__ret__.type,
        vm_extension_type=__ret__.vm_extension_type)

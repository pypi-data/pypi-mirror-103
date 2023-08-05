# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .blob_container import *
from .blob_container_immutability_policy import *
from .blob_service_properties import *
from .file_service_properties import *
from .file_share import *
from .get_blob_container import *
from .get_blob_container_immutability_policy import *
from .get_blob_service_properties import *
from .get_file_service_properties import *
from .get_file_share import *
from .get_management_policy import *
from .get_storage_account import *
from .list_storage_account_keys import *
from .list_storage_account_sas import *
from .list_storage_account_service_sas import *
from .management_policy import *
from .storage_account import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-native:storage/v20190401:BlobContainer":
                return BlobContainer(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:storage/v20190401:BlobContainerImmutabilityPolicy":
                return BlobContainerImmutabilityPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:storage/v20190401:BlobServiceProperties":
                return BlobServiceProperties(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:storage/v20190401:FileServiceProperties":
                return FileServiceProperties(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:storage/v20190401:FileShare":
                return FileShare(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:storage/v20190401:ManagementPolicy":
                return ManagementPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:storage/v20190401:StorageAccount":
                return StorageAccount(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "storage/v20190401", _module_instance)

_register_module()

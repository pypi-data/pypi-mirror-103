# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .app_service_environment import *
from .app_service_plan import *
from .app_service_plan_route_for_vnet import *
from .certificate import *
from .get_app_service_environment import *
from .get_app_service_plan import *
from .get_certificate import *
from .get_web_app import *
from .get_web_app_deployment import *
from .get_web_app_deployment_slot import *
from .get_web_app_diagnostic_logs_configuration import *
from .get_web_app_domain_ownership_identifier import *
from .get_web_app_domain_ownership_identifier_slot import *
from .get_web_app_function import *
from .get_web_app_host_name_binding import *
from .get_web_app_host_name_binding_slot import *
from .get_web_app_hybrid_connection import *
from .get_web_app_hybrid_connection_slot import *
from .get_web_app_instance_function_slot import *
from .get_web_app_premier_add_on import *
from .get_web_app_premier_add_on_slot import *
from .get_web_app_public_certificate import *
from .get_web_app_public_certificate_slot import *
from .get_web_app_relay_service_connection import *
from .get_web_app_relay_service_connection_slot import *
from .get_web_app_site_extension import *
from .get_web_app_site_extension_slot import *
from .get_web_app_slot import *
from .get_web_app_slot_configuration_names import *
from .get_web_app_source_control import *
from .get_web_app_source_control_slot import *
from .get_web_app_swift_virtual_network_connection import *
from .get_web_app_swift_virtual_network_connection_slot import *
from .get_web_app_vnet_connection import *
from .get_web_app_vnet_connection_slot import *
from .list_app_service_plan_hybrid_connection_keys import *
from .list_site_identifiers_assigned_to_host_name import *
from .list_web_app_application_settings import *
from .list_web_app_application_settings_slot import *
from .list_web_app_auth_settings import *
from .list_web_app_auth_settings_slot import *
from .list_web_app_azure_storage_accounts import *
from .list_web_app_azure_storage_accounts_slot import *
from .list_web_app_backup_configuration import *
from .list_web_app_backup_configuration_slot import *
from .list_web_app_backup_status_secrets import *
from .list_web_app_backup_status_secrets_slot import *
from .list_web_app_connection_strings import *
from .list_web_app_connection_strings_slot import *
from .list_web_app_function_keys import *
from .list_web_app_function_keys_slot import *
from .list_web_app_function_secrets import *
from .list_web_app_function_secrets_slot import *
from .list_web_app_host_keys import *
from .list_web_app_host_keys_slot import *
from .list_web_app_hybrid_connection_keys import *
from .list_web_app_hybrid_connection_keys_slot import *
from .list_web_app_metadata import *
from .list_web_app_metadata_slot import *
from .list_web_app_publishing_credentials import *
from .list_web_app_publishing_credentials_slot import *
from .list_web_app_site_push_settings import *
from .list_web_app_site_push_settings_slot import *
from .list_web_app_sync_function_triggers import *
from .list_web_app_sync_function_triggers_slot import *
from .web_app import *
from .web_app_application_settings import *
from .web_app_application_settings_slot import *
from .web_app_auth_settings import *
from .web_app_auth_settings_slot import *
from .web_app_azure_storage_accounts import *
from .web_app_azure_storage_accounts_slot import *
from .web_app_backup_configuration import *
from .web_app_backup_configuration_slot import *
from .web_app_connection_strings import *
from .web_app_connection_strings_slot import *
from .web_app_deployment import *
from .web_app_deployment_slot import *
from .web_app_diagnostic_logs_configuration import *
from .web_app_domain_ownership_identifier import *
from .web_app_domain_ownership_identifier_slot import *
from .web_app_function import *
from .web_app_host_name_binding import *
from .web_app_host_name_binding_slot import *
from .web_app_hybrid_connection import *
from .web_app_hybrid_connection_slot import *
from .web_app_instance_function_slot import *
from .web_app_metadata import *
from .web_app_metadata_slot import *
from .web_app_premier_add_on import *
from .web_app_premier_add_on_slot import *
from .web_app_public_certificate import *
from .web_app_public_certificate_slot import *
from .web_app_relay_service_connection import *
from .web_app_relay_service_connection_slot import *
from .web_app_site_extension import *
from .web_app_site_extension_slot import *
from .web_app_site_push_settings import *
from .web_app_site_push_settings_slot import *
from .web_app_slot import *
from .web_app_slot_configuration_names import *
from .web_app_source_control import *
from .web_app_source_control_slot import *
from .web_app_swift_virtual_network_connection import *
from .web_app_swift_virtual_network_connection_slot import *
from .web_app_vnet_connection import *
from .web_app_vnet_connection_slot import *
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
            if typ == "azure-native:web/v20180201:AppServiceEnvironment":
                return AppServiceEnvironment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:AppServicePlan":
                return AppServicePlan(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:AppServicePlanRouteForVnet":
                return AppServicePlanRouteForVnet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:Certificate":
                return Certificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebApp":
                return WebApp(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppApplicationSettings":
                return WebAppApplicationSettings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppApplicationSettingsSlot":
                return WebAppApplicationSettingsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppAuthSettings":
                return WebAppAuthSettings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppAuthSettingsSlot":
                return WebAppAuthSettingsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppAzureStorageAccounts":
                return WebAppAzureStorageAccounts(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppAzureStorageAccountsSlot":
                return WebAppAzureStorageAccountsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppBackupConfiguration":
                return WebAppBackupConfiguration(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppBackupConfigurationSlot":
                return WebAppBackupConfigurationSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppConnectionStrings":
                return WebAppConnectionStrings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppConnectionStringsSlot":
                return WebAppConnectionStringsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppDeployment":
                return WebAppDeployment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppDeploymentSlot":
                return WebAppDeploymentSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppDiagnosticLogsConfiguration":
                return WebAppDiagnosticLogsConfiguration(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppDomainOwnershipIdentifier":
                return WebAppDomainOwnershipIdentifier(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppDomainOwnershipIdentifierSlot":
                return WebAppDomainOwnershipIdentifierSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppFunction":
                return WebAppFunction(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppHostNameBinding":
                return WebAppHostNameBinding(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppHostNameBindingSlot":
                return WebAppHostNameBindingSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppHybridConnection":
                return WebAppHybridConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppHybridConnectionSlot":
                return WebAppHybridConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppInstanceFunctionSlot":
                return WebAppInstanceFunctionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppMetadata":
                return WebAppMetadata(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppMetadataSlot":
                return WebAppMetadataSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppPremierAddOn":
                return WebAppPremierAddOn(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppPremierAddOnSlot":
                return WebAppPremierAddOnSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppPublicCertificate":
                return WebAppPublicCertificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppPublicCertificateSlot":
                return WebAppPublicCertificateSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppRelayServiceConnection":
                return WebAppRelayServiceConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppRelayServiceConnectionSlot":
                return WebAppRelayServiceConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSiteExtension":
                return WebAppSiteExtension(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSiteExtensionSlot":
                return WebAppSiteExtensionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSitePushSettings":
                return WebAppSitePushSettings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSitePushSettingsSlot":
                return WebAppSitePushSettingsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSlot":
                return WebAppSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSlotConfigurationNames":
                return WebAppSlotConfigurationNames(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSourceControl":
                return WebAppSourceControl(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSourceControlSlot":
                return WebAppSourceControlSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSwiftVirtualNetworkConnection":
                return WebAppSwiftVirtualNetworkConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppSwiftVirtualNetworkConnectionSlot":
                return WebAppSwiftVirtualNetworkConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppVnetConnection":
                return WebAppVnetConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:web/v20180201:WebAppVnetConnectionSlot":
                return WebAppVnetConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "web/v20180201", _module_instance)

_register_module()

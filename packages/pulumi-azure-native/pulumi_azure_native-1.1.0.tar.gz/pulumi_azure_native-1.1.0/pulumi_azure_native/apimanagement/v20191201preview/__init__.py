# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .api import *
from .api_diagnostic import *
from .api_issue import *
from .api_issue_attachment import *
from .api_issue_comment import *
from .api_management_service import *
from .api_operation import *
from .api_operation_policy import *
from .api_policy import *
from .api_release import *
from .api_schema import *
from .api_tag_description import *
from .api_version_set import *
from .authorization_server import *
from .backend import *
from .cache import *
from .certificate import *
from .diagnostic import *
from .email_template import *
from .gateway import *
from .gateway_api_entity_tag import *
from .gateway_hostname_configuration import *
from .get_api import *
from .get_api_diagnostic import *
from .get_api_issue import *
from .get_api_issue_attachment import *
from .get_api_issue_comment import *
from .get_api_management_service import *
from .get_api_management_service_sso_token import *
from .get_api_operation import *
from .get_api_operation_policy import *
from .get_api_policy import *
from .get_api_release import *
from .get_api_schema import *
from .get_api_tag_description import *
from .get_api_version_set import *
from .get_authorization_server import *
from .get_backend import *
from .get_cache import *
from .get_certificate import *
from .get_diagnostic import *
from .get_email_template import *
from .get_gateway import *
from .get_gateway_hostname_configuration import *
from .get_group import *
from .get_identity_provider import *
from .get_logger import *
from .get_named_value import *
from .get_open_id_connect_provider import *
from .get_policy import *
from .get_product import *
from .get_product_policy import *
from .get_subscription import *
from .get_tag import *
from .get_tag_by_api import *
from .get_tag_by_operation import *
from .get_tag_by_product import *
from .get_user import *
from .group import *
from .group_user import *
from .identity_provider import *
from .list_authorization_server_secrets import *
from .list_delegation_setting_secrets import *
from .list_gateway_keys import *
from .list_identity_provider_secrets import *
from .list_named_value import *
from .list_open_id_connect_provider_secrets import *
from .list_subscription_secrets import *
from .list_tenant_access_git_secrets import *
from .list_tenant_access_secrets import *
from .logger import *
from .named_value import *
from .notification_recipient_email import *
from .notification_recipient_user import *
from .open_id_connect_provider import *
from .policy import *
from .product import *
from .product_api import *
from .product_group import *
from .product_policy import *
from .subscription import *
from .tag import *
from .tag_by_api import *
from .tag_by_operation import *
from .tag_by_product import *
from .user import *
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
            if typ == "azure-native:apimanagement/v20191201preview:Api":
                return Api(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiDiagnostic":
                return ApiDiagnostic(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiIssue":
                return ApiIssue(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiIssueAttachment":
                return ApiIssueAttachment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiIssueComment":
                return ApiIssueComment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiManagementService":
                return ApiManagementService(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiOperation":
                return ApiOperation(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiOperationPolicy":
                return ApiOperationPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiPolicy":
                return ApiPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiRelease":
                return ApiRelease(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiSchema":
                return ApiSchema(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiTagDescription":
                return ApiTagDescription(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ApiVersionSet":
                return ApiVersionSet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:AuthorizationServer":
                return AuthorizationServer(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Backend":
                return Backend(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Cache":
                return Cache(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Certificate":
                return Certificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Diagnostic":
                return Diagnostic(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:EmailTemplate":
                return EmailTemplate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Gateway":
                return Gateway(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:GatewayApiEntityTag":
                return GatewayApiEntityTag(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:GatewayHostnameConfiguration":
                return GatewayHostnameConfiguration(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Group":
                return Group(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:GroupUser":
                return GroupUser(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:IdentityProvider":
                return IdentityProvider(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Logger":
                return Logger(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:NamedValue":
                return NamedValue(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:NotificationRecipientEmail":
                return NotificationRecipientEmail(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:NotificationRecipientUser":
                return NotificationRecipientUser(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:OpenIdConnectProvider":
                return OpenIdConnectProvider(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Policy":
                return Policy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Product":
                return Product(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ProductApi":
                return ProductApi(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ProductGroup":
                return ProductGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:ProductPolicy":
                return ProductPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Subscription":
                return Subscription(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:Tag":
                return Tag(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:TagByApi":
                return TagByApi(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:TagByOperation":
                return TagByOperation(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:TagByProduct":
                return TagByProduct(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:apimanagement/v20191201preview:User":
                return User(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "apimanagement/v20191201preview", _module_instance)

_register_module()

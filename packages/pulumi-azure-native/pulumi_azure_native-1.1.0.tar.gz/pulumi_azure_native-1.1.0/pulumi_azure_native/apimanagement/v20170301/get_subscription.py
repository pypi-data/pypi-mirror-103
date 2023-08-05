# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetSubscriptionResult',
    'AwaitableGetSubscriptionResult',
    'get_subscription',
]

@pulumi.output_type
class GetSubscriptionResult:
    """
    Subscription details.
    """
    def __init__(__self__, created_date=None, display_name=None, end_date=None, expiration_date=None, id=None, name=None, notification_date=None, primary_key=None, product_id=None, secondary_key=None, start_date=None, state=None, state_comment=None, type=None, user_id=None):
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if end_date and not isinstance(end_date, str):
            raise TypeError("Expected argument 'end_date' to be a str")
        pulumi.set(__self__, "end_date", end_date)
        if expiration_date and not isinstance(expiration_date, str):
            raise TypeError("Expected argument 'expiration_date' to be a str")
        pulumi.set(__self__, "expiration_date", expiration_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if notification_date and not isinstance(notification_date, str):
            raise TypeError("Expected argument 'notification_date' to be a str")
        pulumi.set(__self__, "notification_date", notification_date)
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, "primary_key", primary_key)
        if product_id and not isinstance(product_id, str):
            raise TypeError("Expected argument 'product_id' to be a str")
        pulumi.set(__self__, "product_id", product_id)
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, "secondary_key", secondary_key)
        if start_date and not isinstance(start_date, str):
            raise TypeError("Expected argument 'start_date' to be a str")
        pulumi.set(__self__, "start_date", start_date)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if state_comment and not isinstance(state_comment, str):
            raise TypeError("Expected argument 'state_comment' to be a str")
        pulumi.set(__self__, "state_comment", state_comment)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_id and not isinstance(user_id, str):
            raise TypeError("Expected argument 'user_id' to be a str")
        pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        Subscription creation date. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The name of the subscription, or null if the subscription has no name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="endDate")
    def end_date(self) -> Optional[str]:
        """
        Date when subscription was cancelled or expired. The setting is for audit purposes only and the subscription is not automatically cancelled. The subscription lifecycle can be managed by using the `state` property. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
        """
        return pulumi.get(self, "end_date")

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> Optional[str]:
        """
        Subscription expiration date. The setting is for audit purposes only and the subscription is not automatically expired. The subscription lifecycle can be managed by using the `state` property. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notificationDate")
    def notification_date(self) -> Optional[str]:
        """
        Upcoming subscription expiration notification date. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
        """
        return pulumi.get(self, "notification_date")

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> str:
        """
        Subscription primary key.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> str:
        """
        The product resource identifier of the subscribed product. The value is a valid relative URL in the format of /products/{productId} where {productId} is a product identifier.
        """
        return pulumi.get(self, "product_id")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> str:
        """
        Subscription secondary key.
        """
        return pulumi.get(self, "secondary_key")

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> Optional[str]:
        """
        Subscription activation date. The setting is for audit purposes only and the subscription is not automatically activated. The subscription lifecycle can be managed by using the `state` property. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
        """
        return pulumi.get(self, "start_date")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Subscription state. Possible states are * active – the subscription is active, * suspended – the subscription is blocked, and the subscriber cannot call any APIs of the product, * submitted – the subscription request has been made by the developer, but has not yet been approved or rejected, * rejected – the subscription request has been denied by an administrator, * cancelled – the subscription has been cancelled by the developer or administrator, * expired – the subscription reached its expiration date and was deactivated.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateComment")
    def state_comment(self) -> Optional[str]:
        """
        Optional subscription comment added by an administrator.
        """
        return pulumi.get(self, "state_comment")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> str:
        """
        The user resource identifier of the subscription owner. The value is a valid relative URL in the format of /users/{uid} where {uid} is a user identifier.
        """
        return pulumi.get(self, "user_id")


class AwaitableGetSubscriptionResult(GetSubscriptionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubscriptionResult(
            created_date=self.created_date,
            display_name=self.display_name,
            end_date=self.end_date,
            expiration_date=self.expiration_date,
            id=self.id,
            name=self.name,
            notification_date=self.notification_date,
            primary_key=self.primary_key,
            product_id=self.product_id,
            secondary_key=self.secondary_key,
            start_date=self.start_date,
            state=self.state,
            state_comment=self.state_comment,
            type=self.type,
            user_id=self.user_id)


def get_subscription(resource_group_name: Optional[str] = None,
                     service_name: Optional[str] = None,
                     sid: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubscriptionResult:
    """
    Subscription details.


    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    :param str sid: Subscription entity Identifier. The entity represents the association between a user and a product in API Management.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    __args__['sid'] = sid
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20170301:getSubscription', __args__, opts=opts, typ=GetSubscriptionResult).value

    return AwaitableGetSubscriptionResult(
        created_date=__ret__.created_date,
        display_name=__ret__.display_name,
        end_date=__ret__.end_date,
        expiration_date=__ret__.expiration_date,
        id=__ret__.id,
        name=__ret__.name,
        notification_date=__ret__.notification_date,
        primary_key=__ret__.primary_key,
        product_id=__ret__.product_id,
        secondary_key=__ret__.secondary_key,
        start_date=__ret__.start_date,
        state=__ret__.state,
        state_comment=__ret__.state_comment,
        type=__ret__.type,
        user_id=__ret__.user_id)

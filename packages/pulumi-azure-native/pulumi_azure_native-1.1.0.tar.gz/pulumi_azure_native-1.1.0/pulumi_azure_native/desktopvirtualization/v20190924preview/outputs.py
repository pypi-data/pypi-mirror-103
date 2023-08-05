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
    'RegistrationInfoResponse',
]

@pulumi.output_type
class RegistrationInfoResponse(dict):
    """
    Represents a RegistrationInfo definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "expirationTime":
            suggest = "expiration_time"
        elif key == "registrationTokenOperation":
            suggest = "registration_token_operation"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RegistrationInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RegistrationInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RegistrationInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 expiration_time: Optional[str] = None,
                 registration_token_operation: Optional[str] = None,
                 token: Optional[str] = None):
        """
        Represents a RegistrationInfo definition.
        :param str expiration_time: Expiration time of registration token.
        :param str registration_token_operation: The type of resetting the token.
        :param str token: The registration token base64 encoded string.
        """
        if expiration_time is not None:
            pulumi.set(__self__, "expiration_time", expiration_time)
        if registration_token_operation is not None:
            pulumi.set(__self__, "registration_token_operation", registration_token_operation)
        if token is not None:
            pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter(name="expirationTime")
    def expiration_time(self) -> Optional[str]:
        """
        Expiration time of registration token.
        """
        return pulumi.get(self, "expiration_time")

    @property
    @pulumi.getter(name="registrationTokenOperation")
    def registration_token_operation(self) -> Optional[str]:
        """
        The type of resetting the token.
        """
        return pulumi.get(self, "registration_token_operation")

    @property
    @pulumi.getter
    def token(self) -> Optional[str]:
        """
        The registration token base64 encoded string.
        """
        return pulumi.get(self, "token")



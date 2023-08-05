# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'IntegrationService',
]

@pulumi.output_type
class IntegrationService(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "serviceKey":
            suggest = "service_key"
        elif key == "serviceName":
            suggest = "service_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationService. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationService.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationService.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 service_key: str,
                 service_name: str):
        pulumi.set(__self__, "service_key", service_key)
        pulumi.set(__self__, "service_name", service_name)

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> str:
        return pulumi.get(self, "service_key")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> str:
        return pulumi.get(self, "service_name")



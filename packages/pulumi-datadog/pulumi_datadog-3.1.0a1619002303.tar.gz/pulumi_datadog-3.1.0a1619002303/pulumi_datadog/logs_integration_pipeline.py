# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['LogsIntegrationPipelineArgs', 'LogsIntegrationPipeline']

@pulumi.input_type
class LogsIntegrationPipelineArgs:
    def __init__(__self__, *,
                 is_enabled: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a LogsIntegrationPipeline resource.
        :param pulumi.Input[bool] is_enabled: Boolean value to enable your pipeline.
        """
        if is_enabled is not None:
            pulumi.set(__self__, "is_enabled", is_enabled)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean value to enable your pipeline.
        """
        return pulumi.get(self, "is_enabled")

    @is_enabled.setter
    def is_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_enabled", value)


@pulumi.input_type
class _LogsIntegrationPipelineState:
    def __init__(__self__, *,
                 is_enabled: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering LogsIntegrationPipeline resources.
        :param pulumi.Input[bool] is_enabled: Boolean value to enable your pipeline.
        """
        if is_enabled is not None:
            pulumi.set(__self__, "is_enabled", is_enabled)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean value to enable your pipeline.
        """
        return pulumi.get(self, "is_enabled")

    @is_enabled.setter
    def is_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_enabled", value)


class LogsIntegrationPipeline(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Provides a Datadog [Logs Pipeline API](https://docs.datadoghq.com/api/v1/logs-pipelines/) resource to manage the [integrations](https://docs.datadoghq.com/logs/log_collection/?tab=tcpussite).

        Integration pipelines are the pipelines that are automatically installed for your organization when sending the logs with specific sources. You don't need to maintain or update these types of pipelines. Keeping them as resources, however, allows you to manage the order of your pipelines by referencing them in your LogsPipelineOrder resource. If you don't need the `pipeline_order` feature, this resource declaration can be omitted.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        python = datadog.LogsIntegrationPipeline("python", is_enabled=True)
        ```

        ## Import

        ```sh
         $ pulumi import datadog:index/logsIntegrationPipeline:LogsIntegrationPipeline name> <pipelineID>`
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] is_enabled: Boolean value to enable your pipeline.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[LogsIntegrationPipelineArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog [Logs Pipeline API](https://docs.datadoghq.com/api/v1/logs-pipelines/) resource to manage the [integrations](https://docs.datadoghq.com/logs/log_collection/?tab=tcpussite).

        Integration pipelines are the pipelines that are automatically installed for your organization when sending the logs with specific sources. You don't need to maintain or update these types of pipelines. Keeping them as resources, however, allows you to manage the order of your pipelines by referencing them in your LogsPipelineOrder resource. If you don't need the `pipeline_order` feature, this resource declaration can be omitted.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        python = datadog.LogsIntegrationPipeline("python", is_enabled=True)
        ```

        ## Import

        ```sh
         $ pulumi import datadog:index/logsIntegrationPipeline:LogsIntegrationPipeline name> <pipelineID>`
        ```

        :param str resource_name: The name of the resource.
        :param LogsIntegrationPipelineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LogsIntegrationPipelineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
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
            __props__ = LogsIntegrationPipelineArgs.__new__(LogsIntegrationPipelineArgs)

            __props__.__dict__["is_enabled"] = is_enabled
        super(LogsIntegrationPipeline, __self__).__init__(
            'datadog:index/logsIntegrationPipeline:LogsIntegrationPipeline',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            is_enabled: Optional[pulumi.Input[bool]] = None) -> 'LogsIntegrationPipeline':
        """
        Get an existing LogsIntegrationPipeline resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] is_enabled: Boolean value to enable your pipeline.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LogsIntegrationPipelineState.__new__(_LogsIntegrationPipelineState)

        __props__.__dict__["is_enabled"] = is_enabled
        return LogsIntegrationPipeline(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean value to enable your pipeline.
        """
        return pulumi.get(self, "is_enabled")


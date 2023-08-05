# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['SecurityMonitoringRuleArgs', 'SecurityMonitoringRule']

@pulumi.input_type
class SecurityMonitoringRuleArgs:
    def __init__(__self__, *,
                 cases: pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleCaseArgs']]],
                 message: pulumi.Input[str],
                 name: pulumi.Input[str],
                 queries: pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleQueryArgs']]],
                 enabled: Optional[pulumi.Input[bool]] = None,
                 options: Optional[pulumi.Input['SecurityMonitoringRuleOptionsArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a SecurityMonitoringRule resource.
        :param pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleCaseArgs']]] cases: Cases for generating signals.
        :param pulumi.Input[str] message: Message for generated signals.
        :param pulumi.Input[str] name: The name of the rule.
        :param pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleQueryArgs']]] queries: Queries for selecting logs which are part of the rule.
        :param pulumi.Input[bool] enabled: Whether the rule is enabled.
        :param pulumi.Input['SecurityMonitoringRuleOptionsArgs'] options: Options on rules.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags for generated signals.
        """
        pulumi.set(__self__, "cases", cases)
        pulumi.set(__self__, "message", message)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "queries", queries)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if options is not None:
            pulumi.set(__self__, "options", options)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def cases(self) -> pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleCaseArgs']]]:
        """
        Cases for generating signals.
        """
        return pulumi.get(self, "cases")

    @cases.setter
    def cases(self, value: pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleCaseArgs']]]):
        pulumi.set(self, "cases", value)

    @property
    @pulumi.getter
    def message(self) -> pulumi.Input[str]:
        """
        Message for generated signals.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: pulumi.Input[str]):
        pulumi.set(self, "message", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def queries(self) -> pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleQueryArgs']]]:
        """
        Queries for selecting logs which are part of the rule.
        """
        return pulumi.get(self, "queries")

    @queries.setter
    def queries(self, value: pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleQueryArgs']]]):
        pulumi.set(self, "queries", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the rule is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input['SecurityMonitoringRuleOptionsArgs']]:
        """
        Options on rules.
        """
        return pulumi.get(self, "options")

    @options.setter
    def options(self, value: Optional[pulumi.Input['SecurityMonitoringRuleOptionsArgs']]):
        pulumi.set(self, "options", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags for generated signals.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _SecurityMonitoringRuleState:
    def __init__(__self__, *,
                 cases: Optional[pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleCaseArgs']]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input['SecurityMonitoringRuleOptionsArgs']] = None,
                 queries: Optional[pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleQueryArgs']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering SecurityMonitoringRule resources.
        :param pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleCaseArgs']]] cases: Cases for generating signals.
        :param pulumi.Input[bool] enabled: Whether the rule is enabled.
        :param pulumi.Input[str] message: Message for generated signals.
        :param pulumi.Input[str] name: The name of the rule.
        :param pulumi.Input['SecurityMonitoringRuleOptionsArgs'] options: Options on rules.
        :param pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleQueryArgs']]] queries: Queries for selecting logs which are part of the rule.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags for generated signals.
        """
        if cases is not None:
            pulumi.set(__self__, "cases", cases)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if options is not None:
            pulumi.set(__self__, "options", options)
        if queries is not None:
            pulumi.set(__self__, "queries", queries)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def cases(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleCaseArgs']]]]:
        """
        Cases for generating signals.
        """
        return pulumi.get(self, "cases")

    @cases.setter
    def cases(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleCaseArgs']]]]):
        pulumi.set(self, "cases", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the rule is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        Message for generated signals.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input['SecurityMonitoringRuleOptionsArgs']]:
        """
        Options on rules.
        """
        return pulumi.get(self, "options")

    @options.setter
    def options(self, value: Optional[pulumi.Input['SecurityMonitoringRuleOptionsArgs']]):
        pulumi.set(self, "options", value)

    @property
    @pulumi.getter
    def queries(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleQueryArgs']]]]:
        """
        Queries for selecting logs which are part of the rule.
        """
        return pulumi.get(self, "queries")

    @queries.setter
    def queries(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SecurityMonitoringRuleQueryArgs']]]]):
        pulumi.set(self, "queries", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags for generated signals.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class SecurityMonitoringRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleCaseArgs']]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleOptionsArgs']]] = None,
                 queries: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleQueryArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Datadog [Security Monitoring Rule API](https://docs.datadoghq.com/api/v2/security-monitoring/) resource. This can be used to create and manage Datadog security monitoring rules. To change settings for a default rule use [datadog_security_default_rule](https://www.terraform.io/resources/security_monitoring_default_rule) instead.

        ## Example Usage

        Create a simple security monitoring rule.

        ```python
        import pulumi
        import pulumi_datadog as datadog

        myrule = datadog.SecurityMonitoringRule("myrule",
            cases=[datadog.SecurityMonitoringRuleCaseArgs(
                condition="errors > 3 && warnings > 10",
                notifications=["@user"],
                status="high",
            )],
            enabled=True,
            message="The rule has triggered.",
            name="My rule",
            options=datadog.SecurityMonitoringRuleOptionsArgs(
                evaluation_window=300,
                keep_alive=600,
                max_signal_duration=900,
            ),
            queries=[
                datadog.SecurityMonitoringRuleQueryArgs(
                    aggregation="count",
                    group_by_fields=["host"],
                    name="errors",
                    query="status:error",
                ),
                datadog.SecurityMonitoringRuleQueryArgs(
                    aggregation="count",
                    group_by_fields=["host"],
                    name="warnings",
                    query="status:warning",
                ),
            ],
            tags=["type:dos"])
        ```

        ## Import

        Security monitoring rules can be imported using ID, e.g. console

        ```sh
         $ pulumi import datadog:index/securityMonitoringRule:SecurityMonitoringRule my_monitor m0o-hto-lkb
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleCaseArgs']]]] cases: Cases for generating signals.
        :param pulumi.Input[bool] enabled: Whether the rule is enabled.
        :param pulumi.Input[str] message: Message for generated signals.
        :param pulumi.Input[str] name: The name of the rule.
        :param pulumi.Input[pulumi.InputType['SecurityMonitoringRuleOptionsArgs']] options: Options on rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleQueryArgs']]]] queries: Queries for selecting logs which are part of the rule.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags for generated signals.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SecurityMonitoringRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog [Security Monitoring Rule API](https://docs.datadoghq.com/api/v2/security-monitoring/) resource. This can be used to create and manage Datadog security monitoring rules. To change settings for a default rule use [datadog_security_default_rule](https://www.terraform.io/resources/security_monitoring_default_rule) instead.

        ## Example Usage

        Create a simple security monitoring rule.

        ```python
        import pulumi
        import pulumi_datadog as datadog

        myrule = datadog.SecurityMonitoringRule("myrule",
            cases=[datadog.SecurityMonitoringRuleCaseArgs(
                condition="errors > 3 && warnings > 10",
                notifications=["@user"],
                status="high",
            )],
            enabled=True,
            message="The rule has triggered.",
            name="My rule",
            options=datadog.SecurityMonitoringRuleOptionsArgs(
                evaluation_window=300,
                keep_alive=600,
                max_signal_duration=900,
            ),
            queries=[
                datadog.SecurityMonitoringRuleQueryArgs(
                    aggregation="count",
                    group_by_fields=["host"],
                    name="errors",
                    query="status:error",
                ),
                datadog.SecurityMonitoringRuleQueryArgs(
                    aggregation="count",
                    group_by_fields=["host"],
                    name="warnings",
                    query="status:warning",
                ),
            ],
            tags=["type:dos"])
        ```

        ## Import

        Security monitoring rules can be imported using ID, e.g. console

        ```sh
         $ pulumi import datadog:index/securityMonitoringRule:SecurityMonitoringRule my_monitor m0o-hto-lkb
        ```

        :param str resource_name: The name of the resource.
        :param SecurityMonitoringRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecurityMonitoringRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleCaseArgs']]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleOptionsArgs']]] = None,
                 queries: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleQueryArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
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
            __props__ = SecurityMonitoringRuleArgs.__new__(SecurityMonitoringRuleArgs)

            if cases is None and not opts.urn:
                raise TypeError("Missing required property 'cases'")
            __props__.__dict__["cases"] = cases
            __props__.__dict__["enabled"] = enabled
            if message is None and not opts.urn:
                raise TypeError("Missing required property 'message'")
            __props__.__dict__["message"] = message
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["options"] = options
            if queries is None and not opts.urn:
                raise TypeError("Missing required property 'queries'")
            __props__.__dict__["queries"] = queries
            __props__.__dict__["tags"] = tags
        super(SecurityMonitoringRule, __self__).__init__(
            'datadog:index/securityMonitoringRule:SecurityMonitoringRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleCaseArgs']]]]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            message: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            options: Optional[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleOptionsArgs']]] = None,
            queries: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleQueryArgs']]]]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'SecurityMonitoringRule':
        """
        Get an existing SecurityMonitoringRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleCaseArgs']]]] cases: Cases for generating signals.
        :param pulumi.Input[bool] enabled: Whether the rule is enabled.
        :param pulumi.Input[str] message: Message for generated signals.
        :param pulumi.Input[str] name: The name of the rule.
        :param pulumi.Input[pulumi.InputType['SecurityMonitoringRuleOptionsArgs']] options: Options on rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SecurityMonitoringRuleQueryArgs']]]] queries: Queries for selecting logs which are part of the rule.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags for generated signals.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SecurityMonitoringRuleState.__new__(_SecurityMonitoringRuleState)

        __props__.__dict__["cases"] = cases
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["message"] = message
        __props__.__dict__["name"] = name
        __props__.__dict__["options"] = options
        __props__.__dict__["queries"] = queries
        __props__.__dict__["tags"] = tags
        return SecurityMonitoringRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cases(self) -> pulumi.Output[Sequence['outputs.SecurityMonitoringRuleCase']]:
        """
        Cases for generating signals.
        """
        return pulumi.get(self, "cases")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the rule is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def message(self) -> pulumi.Output[str]:
        """
        Message for generated signals.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def options(self) -> pulumi.Output[Optional['outputs.SecurityMonitoringRuleOptions']]:
        """
        Options on rules.
        """
        return pulumi.get(self, "options")

    @property
    @pulumi.getter
    def queries(self) -> pulumi.Output[Sequence['outputs.SecurityMonitoringRuleQuery']]:
        """
        Queries for selecting logs which are part of the rule.
        """
        return pulumi.get(self, "queries")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Tags for generated signals.
        """
        return pulumi.get(self, "tags")


# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['UserArgs', 'User']

@pulumi.input_type
class UserArgs:
    def __init__(__self__, *,
                 email: pulumi.Input[str],
                 access_role: Optional[pulumi.Input[str]] = None,
                 disabled: Optional[pulumi.Input[bool]] = None,
                 handle: Optional[pulumi.Input[str]] = None,
                 is_admin: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 send_user_invitation: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a User resource.
        :param pulumi.Input[str] email: Email address for user.
        :param pulumi.Input[str] access_role: Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`.
               `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        :param pulumi.Input[bool] disabled: Whether the user is disabled.
        :param pulumi.Input[str] handle: The user handle, must be a valid email.
        :param pulumi.Input[bool] is_admin: Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the
               argument would always trigger an execution plan.
        :param pulumi.Input[str] name: Name for user.
        :param pulumi.Input[str] role: Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument
               would always trigger an execution plan.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] roles: A list a role IDs to assign to the user.
        :param pulumi.Input[bool] send_user_invitation: Whether an invitation email should be sent when the user is created.
        """
        pulumi.set(__self__, "email", email)
        if access_role is not None:
            warnings.warn("""This parameter is replaced by `roles` and will be removed from the next Major version""", DeprecationWarning)
            pulumi.log.warn("""access_role is deprecated: This parameter is replaced by `roles` and will be removed from the next Major version""")
        if access_role is not None:
            pulumi.set(__self__, "access_role", access_role)
        if disabled is not None:
            pulumi.set(__self__, "disabled", disabled)
        if handle is not None:
            warnings.warn("""This parameter is deprecated and will be removed from the next Major version""", DeprecationWarning)
            pulumi.log.warn("""handle is deprecated: This parameter is deprecated and will be removed from the next Major version""")
        if handle is not None:
            pulumi.set(__self__, "handle", handle)
        if is_admin is not None:
            warnings.warn("""This parameter is replaced by `roles` and will be removed from the next Major version""", DeprecationWarning)
            pulumi.log.warn("""is_admin is deprecated: This parameter is replaced by `roles` and will be removed from the next Major version""")
        if is_admin is not None:
            pulumi.set(__self__, "is_admin", is_admin)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if role is not None:
            warnings.warn("""This parameter was removed from the API and has no effect""", DeprecationWarning)
            pulumi.log.warn("""role is deprecated: This parameter was removed from the API and has no effect""")
        if role is not None:
            pulumi.set(__self__, "role", role)
        if roles is not None:
            pulumi.set(__self__, "roles", roles)
        if send_user_invitation is not None:
            pulumi.set(__self__, "send_user_invitation", send_user_invitation)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Input[str]:
        """
        Email address for user.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: pulumi.Input[str]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="accessRole")
    def access_role(self) -> Optional[pulumi.Input[str]]:
        """
        Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`.
        `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        """
        return pulumi.get(self, "access_role")

    @access_role.setter
    def access_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_role", value)

    @property
    @pulumi.getter
    def disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the user is disabled.
        """
        return pulumi.get(self, "disabled")

    @disabled.setter
    def disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disabled", value)

    @property
    @pulumi.getter
    def handle(self) -> Optional[pulumi.Input[str]]:
        """
        The user handle, must be a valid email.
        """
        return pulumi.get(self, "handle")

    @handle.setter
    def handle(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "handle", value)

    @property
    @pulumi.getter(name="isAdmin")
    def is_admin(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the
        argument would always trigger an execution plan.
        """
        return pulumi.get(self, "is_admin")

    @is_admin.setter
    def is_admin(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_admin", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name for user.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument
        would always trigger an execution plan.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list a role IDs to assign to the user.
        """
        return pulumi.get(self, "roles")

    @roles.setter
    def roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "roles", value)

    @property
    @pulumi.getter(name="sendUserInvitation")
    def send_user_invitation(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether an invitation email should be sent when the user is created.
        """
        return pulumi.get(self, "send_user_invitation")

    @send_user_invitation.setter
    def send_user_invitation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_user_invitation", value)


@pulumi.input_type
class _UserState:
    def __init__(__self__, *,
                 access_role: Optional[pulumi.Input[str]] = None,
                 disabled: Optional[pulumi.Input[bool]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 handle: Optional[pulumi.Input[str]] = None,
                 is_admin: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 send_user_invitation: Optional[pulumi.Input[bool]] = None,
                 user_invitation_id: Optional[pulumi.Input[str]] = None,
                 verified: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering User resources.
        :param pulumi.Input[str] access_role: Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`.
               `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        :param pulumi.Input[bool] disabled: Whether the user is disabled.
        :param pulumi.Input[str] email: Email address for user.
        :param pulumi.Input[str] handle: The user handle, must be a valid email.
        :param pulumi.Input[bool] is_admin: Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the
               argument would always trigger an execution plan.
        :param pulumi.Input[str] name: Name for user.
        :param pulumi.Input[str] role: Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument
               would always trigger an execution plan.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] roles: A list a role IDs to assign to the user.
        :param pulumi.Input[bool] send_user_invitation: Whether an invitation email should be sent when the user is created.
        :param pulumi.Input[str] user_invitation_id: The ID of the user invitation that was sent when creating the user.
        :param pulumi.Input[bool] verified: Returns true if Datadog user is verified.
        """
        if access_role is not None:
            warnings.warn("""This parameter is replaced by `roles` and will be removed from the next Major version""", DeprecationWarning)
            pulumi.log.warn("""access_role is deprecated: This parameter is replaced by `roles` and will be removed from the next Major version""")
        if access_role is not None:
            pulumi.set(__self__, "access_role", access_role)
        if disabled is not None:
            pulumi.set(__self__, "disabled", disabled)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if handle is not None:
            warnings.warn("""This parameter is deprecated and will be removed from the next Major version""", DeprecationWarning)
            pulumi.log.warn("""handle is deprecated: This parameter is deprecated and will be removed from the next Major version""")
        if handle is not None:
            pulumi.set(__self__, "handle", handle)
        if is_admin is not None:
            warnings.warn("""This parameter is replaced by `roles` and will be removed from the next Major version""", DeprecationWarning)
            pulumi.log.warn("""is_admin is deprecated: This parameter is replaced by `roles` and will be removed from the next Major version""")
        if is_admin is not None:
            pulumi.set(__self__, "is_admin", is_admin)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if role is not None:
            warnings.warn("""This parameter was removed from the API and has no effect""", DeprecationWarning)
            pulumi.log.warn("""role is deprecated: This parameter was removed from the API and has no effect""")
        if role is not None:
            pulumi.set(__self__, "role", role)
        if roles is not None:
            pulumi.set(__self__, "roles", roles)
        if send_user_invitation is not None:
            pulumi.set(__self__, "send_user_invitation", send_user_invitation)
        if user_invitation_id is not None:
            pulumi.set(__self__, "user_invitation_id", user_invitation_id)
        if verified is not None:
            pulumi.set(__self__, "verified", verified)

    @property
    @pulumi.getter(name="accessRole")
    def access_role(self) -> Optional[pulumi.Input[str]]:
        """
        Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`.
        `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        """
        return pulumi.get(self, "access_role")

    @access_role.setter
    def access_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_role", value)

    @property
    @pulumi.getter
    def disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the user is disabled.
        """
        return pulumi.get(self, "disabled")

    @disabled.setter
    def disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disabled", value)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        Email address for user.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter
    def handle(self) -> Optional[pulumi.Input[str]]:
        """
        The user handle, must be a valid email.
        """
        return pulumi.get(self, "handle")

    @handle.setter
    def handle(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "handle", value)

    @property
    @pulumi.getter(name="isAdmin")
    def is_admin(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the
        argument would always trigger an execution plan.
        """
        return pulumi.get(self, "is_admin")

    @is_admin.setter
    def is_admin(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_admin", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name for user.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument
        would always trigger an execution plan.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list a role IDs to assign to the user.
        """
        return pulumi.get(self, "roles")

    @roles.setter
    def roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "roles", value)

    @property
    @pulumi.getter(name="sendUserInvitation")
    def send_user_invitation(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether an invitation email should be sent when the user is created.
        """
        return pulumi.get(self, "send_user_invitation")

    @send_user_invitation.setter
    def send_user_invitation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_user_invitation", value)

    @property
    @pulumi.getter(name="userInvitationId")
    def user_invitation_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the user invitation that was sent when creating the user.
        """
        return pulumi.get(self, "user_invitation_id")

    @user_invitation_id.setter
    def user_invitation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_invitation_id", value)

    @property
    @pulumi.getter
    def verified(self) -> Optional[pulumi.Input[bool]]:
        """
        Returns true if Datadog user is verified.
        """
        return pulumi.get(self, "verified")

    @verified.setter
    def verified(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "verified", value)


class User(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_role: Optional[pulumi.Input[str]] = None,
                 disabled: Optional[pulumi.Input[bool]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 handle: Optional[pulumi.Input[str]] = None,
                 is_admin: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 send_user_invitation: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Provides a Datadog user resource. This can be used to create and manage Datadog users.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        ro_role = datadog.get_role(filter="Datadog Read Only Role")
        # Create a new Datadog user
        foo = datadog.User("foo",
            email="new@example.com",
            roles=[ro_role.id])
        ```
        ## Schema

        ### Required

        - **email** (String) Email address for user.

        ### Optional

        - **access_role** (String, Deprecated) Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`. `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        - **disabled** (Boolean) Whether the user is disabled.
        - **handle** (String, Deprecated) The user handle, must be a valid email.
        - **id** (String) The ID of this resource.
        - **is_admin** (Boolean, Deprecated) Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument would always trigger an execution plan.
        - **name** (String) Name for user.
        - **role** (String, Deprecated) Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument would always trigger an execution plan.
        - **roles** (Set of String) A list a role IDs to assign to the user.
        - **send_user_invitation** (Boolean) Whether an invitation email should be sent when the user is created.

        ### Read-only

        - **user_invitation_id** (String) The ID of the user invitation that was sent when creating the user.
        - **verified** (Boolean) Returns true if Datadog user is verified.

        ## Import

        Import is supported using the following syntax

        ```sh
         $ pulumi import datadog:index/user:User example_user 6f1b44c0-30b2-11eb-86bc-279f7c1ebaa4
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_role: Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`.
               `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        :param pulumi.Input[bool] disabled: Whether the user is disabled.
        :param pulumi.Input[str] email: Email address for user.
        :param pulumi.Input[str] handle: The user handle, must be a valid email.
        :param pulumi.Input[bool] is_admin: Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the
               argument would always trigger an execution plan.
        :param pulumi.Input[str] name: Name for user.
        :param pulumi.Input[str] role: Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument
               would always trigger an execution plan.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] roles: A list a role IDs to assign to the user.
        :param pulumi.Input[bool] send_user_invitation: Whether an invitation email should be sent when the user is created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog user resource. This can be used to create and manage Datadog users.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        ro_role = datadog.get_role(filter="Datadog Read Only Role")
        # Create a new Datadog user
        foo = datadog.User("foo",
            email="new@example.com",
            roles=[ro_role.id])
        ```
        ## Schema

        ### Required

        - **email** (String) Email address for user.

        ### Optional

        - **access_role** (String, Deprecated) Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`. `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        - **disabled** (Boolean) Whether the user is disabled.
        - **handle** (String, Deprecated) The user handle, must be a valid email.
        - **id** (String) The ID of this resource.
        - **is_admin** (Boolean, Deprecated) Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument would always trigger an execution plan.
        - **name** (String) Name for user.
        - **role** (String, Deprecated) Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument would always trigger an execution plan.
        - **roles** (Set of String) A list a role IDs to assign to the user.
        - **send_user_invitation** (Boolean) Whether an invitation email should be sent when the user is created.

        ### Read-only

        - **user_invitation_id** (String) The ID of the user invitation that was sent when creating the user.
        - **verified** (Boolean) Returns true if Datadog user is verified.

        ## Import

        Import is supported using the following syntax

        ```sh
         $ pulumi import datadog:index/user:User example_user 6f1b44c0-30b2-11eb-86bc-279f7c1ebaa4
        ```

        :param str resource_name: The name of the resource.
        :param UserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_role: Optional[pulumi.Input[str]] = None,
                 disabled: Optional[pulumi.Input[bool]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 handle: Optional[pulumi.Input[str]] = None,
                 is_admin: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 send_user_invitation: Optional[pulumi.Input[bool]] = None,
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
            __props__ = UserArgs.__new__(UserArgs)

            if access_role is not None and not opts.urn:
                warnings.warn("""This parameter is replaced by `roles` and will be removed from the next Major version""", DeprecationWarning)
                pulumi.log.warn("""access_role is deprecated: This parameter is replaced by `roles` and will be removed from the next Major version""")
            __props__.__dict__["access_role"] = access_role
            __props__.__dict__["disabled"] = disabled
            if email is None and not opts.urn:
                raise TypeError("Missing required property 'email'")
            __props__.__dict__["email"] = email
            if handle is not None and not opts.urn:
                warnings.warn("""This parameter is deprecated and will be removed from the next Major version""", DeprecationWarning)
                pulumi.log.warn("""handle is deprecated: This parameter is deprecated and will be removed from the next Major version""")
            __props__.__dict__["handle"] = handle
            if is_admin is not None and not opts.urn:
                warnings.warn("""This parameter is replaced by `roles` and will be removed from the next Major version""", DeprecationWarning)
                pulumi.log.warn("""is_admin is deprecated: This parameter is replaced by `roles` and will be removed from the next Major version""")
            __props__.__dict__["is_admin"] = is_admin
            __props__.__dict__["name"] = name
            if role is not None and not opts.urn:
                warnings.warn("""This parameter was removed from the API and has no effect""", DeprecationWarning)
                pulumi.log.warn("""role is deprecated: This parameter was removed from the API and has no effect""")
            __props__.__dict__["role"] = role
            __props__.__dict__["roles"] = roles
            __props__.__dict__["send_user_invitation"] = send_user_invitation
            __props__.__dict__["user_invitation_id"] = None
            __props__.__dict__["verified"] = None
        super(User, __self__).__init__(
            'datadog:index/user:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_role: Optional[pulumi.Input[str]] = None,
            disabled: Optional[pulumi.Input[bool]] = None,
            email: Optional[pulumi.Input[str]] = None,
            handle: Optional[pulumi.Input[str]] = None,
            is_admin: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None,
            roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            send_user_invitation: Optional[pulumi.Input[bool]] = None,
            user_invitation_id: Optional[pulumi.Input[str]] = None,
            verified: Optional[pulumi.Input[bool]] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_role: Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`.
               `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        :param pulumi.Input[bool] disabled: Whether the user is disabled.
        :param pulumi.Input[str] email: Email address for user.
        :param pulumi.Input[str] handle: The user handle, must be a valid email.
        :param pulumi.Input[bool] is_admin: Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the
               argument would always trigger an execution plan.
        :param pulumi.Input[str] name: Name for user.
        :param pulumi.Input[str] role: Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument
               would always trigger an execution plan.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] roles: A list a role IDs to assign to the user.
        :param pulumi.Input[bool] send_user_invitation: Whether an invitation email should be sent when the user is created.
        :param pulumi.Input[str] user_invitation_id: The ID of the user invitation that was sent when creating the user.
        :param pulumi.Input[bool] verified: Returns true if Datadog user is verified.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserState.__new__(_UserState)

        __props__.__dict__["access_role"] = access_role
        __props__.__dict__["disabled"] = disabled
        __props__.__dict__["email"] = email
        __props__.__dict__["handle"] = handle
        __props__.__dict__["is_admin"] = is_admin
        __props__.__dict__["name"] = name
        __props__.__dict__["role"] = role
        __props__.__dict__["roles"] = roles
        __props__.__dict__["send_user_invitation"] = send_user_invitation
        __props__.__dict__["user_invitation_id"] = user_invitation_id
        __props__.__dict__["verified"] = verified
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessRole")
    def access_role(self) -> pulumi.Output[Optional[str]]:
        """
        Role description for user. Can be `st` (standard user), `adm` (admin user) or `ro` (read-only user). Default is `st`.
        `access_role` is ignored for new users created with this resource. New users have to use the `roles` attribute.
        """
        return pulumi.get(self, "access_role")

    @property
    @pulumi.getter
    def disabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the user is disabled.
        """
        return pulumi.get(self, "disabled")

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[str]:
        """
        Email address for user.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def handle(self) -> pulumi.Output[Optional[str]]:
        """
        The user handle, must be a valid email.
        """
        return pulumi.get(self, "handle")

    @property
    @pulumi.getter(name="isAdmin")
    def is_admin(self) -> pulumi.Output[bool]:
        """
        Whether the user is an administrator. Warning: the corresponding query parameter is ignored by the Datadog API, thus the
        argument would always trigger an execution plan.
        """
        return pulumi.get(self, "is_admin")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Name for user.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[Optional[str]]:
        """
        Role description for user. Warning: the corresponding query parameter is ignored by the Datadog API, thus the argument
        would always trigger an execution plan.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def roles(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list a role IDs to assign to the user.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter(name="sendUserInvitation")
    def send_user_invitation(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether an invitation email should be sent when the user is created.
        """
        return pulumi.get(self, "send_user_invitation")

    @property
    @pulumi.getter(name="userInvitationId")
    def user_invitation_id(self) -> pulumi.Output[str]:
        """
        The ID of the user invitation that was sent when creating the user.
        """
        return pulumi.get(self, "user_invitation_id")

    @property
    @pulumi.getter
    def verified(self) -> pulumi.Output[bool]:
        """
        Returns true if Datadog user is verified.
        """
        return pulumi.get(self, "verified")


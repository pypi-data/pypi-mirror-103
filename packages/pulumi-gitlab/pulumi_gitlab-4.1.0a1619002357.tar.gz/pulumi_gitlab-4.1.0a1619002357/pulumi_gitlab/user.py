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
                 username: pulumi.Input[str],
                 can_create_group: Optional[pulumi.Input[bool]] = None,
                 is_admin: Optional[pulumi.Input[bool]] = None,
                 is_external: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 projects_limit: Optional[pulumi.Input[int]] = None,
                 reset_password: Optional[pulumi.Input[bool]] = None,
                 skip_confirmation: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a User resource.
        :param pulumi.Input[str] email: The e-mail address of the user.
        :param pulumi.Input[str] username: The username of the user.
        :param pulumi.Input[bool] can_create_group: Boolean, defaults to false. Whether to allow the user to create groups.
        :param pulumi.Input[bool] is_admin: Boolean, defaults to false.  Whether to enable administrative priviledges
               for the user.
        :param pulumi.Input[bool] is_external: Boolean, defaults to false. Whether a user has access only to some internal or private projects. External users can only access projects to which they are explicitly granted access.
        :param pulumi.Input[str] name: The name of the user.
        :param pulumi.Input[str] note: The note associated to the user.
        :param pulumi.Input[str] password: The password of the user.
        :param pulumi.Input[int] projects_limit: Integer, defaults to 0.  Number of projects user can create.
        :param pulumi.Input[bool] reset_password: Boolean, defaults to false. Send user password reset link.
        :param pulumi.Input[bool] skip_confirmation: Boolean, defaults to true. Whether to skip confirmation.
        """
        pulumi.set(__self__, "email", email)
        pulumi.set(__self__, "username", username)
        if can_create_group is not None:
            pulumi.set(__self__, "can_create_group", can_create_group)
        if is_admin is not None:
            pulumi.set(__self__, "is_admin", is_admin)
        if is_external is not None:
            pulumi.set(__self__, "is_external", is_external)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if note is not None:
            pulumi.set(__self__, "note", note)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if projects_limit is not None:
            pulumi.set(__self__, "projects_limit", projects_limit)
        if reset_password is not None:
            pulumi.set(__self__, "reset_password", reset_password)
        if skip_confirmation is not None:
            pulumi.set(__self__, "skip_confirmation", skip_confirmation)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Input[str]:
        """
        The e-mail address of the user.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: pulumi.Input[str]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The username of the user.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter(name="canCreateGroup")
    def can_create_group(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to false. Whether to allow the user to create groups.
        """
        return pulumi.get(self, "can_create_group")

    @can_create_group.setter
    def can_create_group(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "can_create_group", value)

    @property
    @pulumi.getter(name="isAdmin")
    def is_admin(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to false.  Whether to enable administrative priviledges
        for the user.
        """
        return pulumi.get(self, "is_admin")

    @is_admin.setter
    def is_admin(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_admin", value)

    @property
    @pulumi.getter(name="isExternal")
    def is_external(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to false. Whether a user has access only to some internal or private projects. External users can only access projects to which they are explicitly granted access.
        """
        return pulumi.get(self, "is_external")

    @is_external.setter
    def is_external(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_external", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def note(self) -> Optional[pulumi.Input[str]]:
        """
        The note associated to the user.
        """
        return pulumi.get(self, "note")

    @note.setter
    def note(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "note", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the user.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="projectsLimit")
    def projects_limit(self) -> Optional[pulumi.Input[int]]:
        """
        Integer, defaults to 0.  Number of projects user can create.
        """
        return pulumi.get(self, "projects_limit")

    @projects_limit.setter
    def projects_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "projects_limit", value)

    @property
    @pulumi.getter(name="resetPassword")
    def reset_password(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to false. Send user password reset link.
        """
        return pulumi.get(self, "reset_password")

    @reset_password.setter
    def reset_password(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reset_password", value)

    @property
    @pulumi.getter(name="skipConfirmation")
    def skip_confirmation(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to true. Whether to skip confirmation.
        """
        return pulumi.get(self, "skip_confirmation")

    @skip_confirmation.setter
    def skip_confirmation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_confirmation", value)


@pulumi.input_type
class _UserState:
    def __init__(__self__, *,
                 can_create_group: Optional[pulumi.Input[bool]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 is_admin: Optional[pulumi.Input[bool]] = None,
                 is_external: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 projects_limit: Optional[pulumi.Input[int]] = None,
                 reset_password: Optional[pulumi.Input[bool]] = None,
                 skip_confirmation: Optional[pulumi.Input[bool]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering User resources.
        :param pulumi.Input[bool] can_create_group: Boolean, defaults to false. Whether to allow the user to create groups.
        :param pulumi.Input[str] email: The e-mail address of the user.
        :param pulumi.Input[bool] is_admin: Boolean, defaults to false.  Whether to enable administrative priviledges
               for the user.
        :param pulumi.Input[bool] is_external: Boolean, defaults to false. Whether a user has access only to some internal or private projects. External users can only access projects to which they are explicitly granted access.
        :param pulumi.Input[str] name: The name of the user.
        :param pulumi.Input[str] note: The note associated to the user.
        :param pulumi.Input[str] password: The password of the user.
        :param pulumi.Input[int] projects_limit: Integer, defaults to 0.  Number of projects user can create.
        :param pulumi.Input[bool] reset_password: Boolean, defaults to false. Send user password reset link.
        :param pulumi.Input[bool] skip_confirmation: Boolean, defaults to true. Whether to skip confirmation.
        :param pulumi.Input[str] username: The username of the user.
        """
        if can_create_group is not None:
            pulumi.set(__self__, "can_create_group", can_create_group)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if is_admin is not None:
            pulumi.set(__self__, "is_admin", is_admin)
        if is_external is not None:
            pulumi.set(__self__, "is_external", is_external)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if note is not None:
            pulumi.set(__self__, "note", note)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if projects_limit is not None:
            pulumi.set(__self__, "projects_limit", projects_limit)
        if reset_password is not None:
            pulumi.set(__self__, "reset_password", reset_password)
        if skip_confirmation is not None:
            pulumi.set(__self__, "skip_confirmation", skip_confirmation)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="canCreateGroup")
    def can_create_group(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to false. Whether to allow the user to create groups.
        """
        return pulumi.get(self, "can_create_group")

    @can_create_group.setter
    def can_create_group(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "can_create_group", value)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        The e-mail address of the user.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="isAdmin")
    def is_admin(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to false.  Whether to enable administrative priviledges
        for the user.
        """
        return pulumi.get(self, "is_admin")

    @is_admin.setter
    def is_admin(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_admin", value)

    @property
    @pulumi.getter(name="isExternal")
    def is_external(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to false. Whether a user has access only to some internal or private projects. External users can only access projects to which they are explicitly granted access.
        """
        return pulumi.get(self, "is_external")

    @is_external.setter
    def is_external(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_external", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def note(self) -> Optional[pulumi.Input[str]]:
        """
        The note associated to the user.
        """
        return pulumi.get(self, "note")

    @note.setter
    def note(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "note", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the user.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="projectsLimit")
    def projects_limit(self) -> Optional[pulumi.Input[int]]:
        """
        Integer, defaults to 0.  Number of projects user can create.
        """
        return pulumi.get(self, "projects_limit")

    @projects_limit.setter
    def projects_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "projects_limit", value)

    @property
    @pulumi.getter(name="resetPassword")
    def reset_password(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to false. Send user password reset link.
        """
        return pulumi.get(self, "reset_password")

    @reset_password.setter
    def reset_password(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reset_password", value)

    @property
    @pulumi.getter(name="skipConfirmation")
    def skip_confirmation(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean, defaults to true. Whether to skip confirmation.
        """
        return pulumi.get(self, "skip_confirmation")

    @skip_confirmation.setter
    def skip_confirmation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_confirmation", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The username of the user.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class User(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 can_create_group: Optional[pulumi.Input[bool]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 is_admin: Optional[pulumi.Input[bool]] = None,
                 is_external: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 projects_limit: Optional[pulumi.Input[int]] = None,
                 reset_password: Optional[pulumi.Input[bool]] = None,
                 skip_confirmation: Optional[pulumi.Input[bool]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a User resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] can_create_group: Boolean, defaults to false. Whether to allow the user to create groups.
        :param pulumi.Input[str] email: The e-mail address of the user.
        :param pulumi.Input[bool] is_admin: Boolean, defaults to false.  Whether to enable administrative priviledges
               for the user.
        :param pulumi.Input[bool] is_external: Boolean, defaults to false. Whether a user has access only to some internal or private projects. External users can only access projects to which they are explicitly granted access.
        :param pulumi.Input[str] name: The name of the user.
        :param pulumi.Input[str] note: The note associated to the user.
        :param pulumi.Input[str] password: The password of the user.
        :param pulumi.Input[int] projects_limit: Integer, defaults to 0.  Number of projects user can create.
        :param pulumi.Input[bool] reset_password: Boolean, defaults to false. Send user password reset link.
        :param pulumi.Input[bool] skip_confirmation: Boolean, defaults to true. Whether to skip confirmation.
        :param pulumi.Input[str] username: The username of the user.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a User resource with the given unique name, props, and options.
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
                 can_create_group: Optional[pulumi.Input[bool]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 is_admin: Optional[pulumi.Input[bool]] = None,
                 is_external: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 projects_limit: Optional[pulumi.Input[int]] = None,
                 reset_password: Optional[pulumi.Input[bool]] = None,
                 skip_confirmation: Optional[pulumi.Input[bool]] = None,
                 username: Optional[pulumi.Input[str]] = None,
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

            __props__.__dict__["can_create_group"] = can_create_group
            if email is None and not opts.urn:
                raise TypeError("Missing required property 'email'")
            __props__.__dict__["email"] = email
            __props__.__dict__["is_admin"] = is_admin
            __props__.__dict__["is_external"] = is_external
            __props__.__dict__["name"] = name
            __props__.__dict__["note"] = note
            __props__.__dict__["password"] = password
            __props__.__dict__["projects_limit"] = projects_limit
            __props__.__dict__["reset_password"] = reset_password
            __props__.__dict__["skip_confirmation"] = skip_confirmation
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
        super(User, __self__).__init__(
            'gitlab:index/user:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            can_create_group: Optional[pulumi.Input[bool]] = None,
            email: Optional[pulumi.Input[str]] = None,
            is_admin: Optional[pulumi.Input[bool]] = None,
            is_external: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            note: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            projects_limit: Optional[pulumi.Input[int]] = None,
            reset_password: Optional[pulumi.Input[bool]] = None,
            skip_confirmation: Optional[pulumi.Input[bool]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] can_create_group: Boolean, defaults to false. Whether to allow the user to create groups.
        :param pulumi.Input[str] email: The e-mail address of the user.
        :param pulumi.Input[bool] is_admin: Boolean, defaults to false.  Whether to enable administrative priviledges
               for the user.
        :param pulumi.Input[bool] is_external: Boolean, defaults to false. Whether a user has access only to some internal or private projects. External users can only access projects to which they are explicitly granted access.
        :param pulumi.Input[str] name: The name of the user.
        :param pulumi.Input[str] note: The note associated to the user.
        :param pulumi.Input[str] password: The password of the user.
        :param pulumi.Input[int] projects_limit: Integer, defaults to 0.  Number of projects user can create.
        :param pulumi.Input[bool] reset_password: Boolean, defaults to false. Send user password reset link.
        :param pulumi.Input[bool] skip_confirmation: Boolean, defaults to true. Whether to skip confirmation.
        :param pulumi.Input[str] username: The username of the user.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserState.__new__(_UserState)

        __props__.__dict__["can_create_group"] = can_create_group
        __props__.__dict__["email"] = email
        __props__.__dict__["is_admin"] = is_admin
        __props__.__dict__["is_external"] = is_external
        __props__.__dict__["name"] = name
        __props__.__dict__["note"] = note
        __props__.__dict__["password"] = password
        __props__.__dict__["projects_limit"] = projects_limit
        __props__.__dict__["reset_password"] = reset_password
        __props__.__dict__["skip_confirmation"] = skip_confirmation
        __props__.__dict__["username"] = username
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="canCreateGroup")
    def can_create_group(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean, defaults to false. Whether to allow the user to create groups.
        """
        return pulumi.get(self, "can_create_group")

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[str]:
        """
        The e-mail address of the user.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="isAdmin")
    def is_admin(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean, defaults to false.  Whether to enable administrative priviledges
        for the user.
        """
        return pulumi.get(self, "is_admin")

    @property
    @pulumi.getter(name="isExternal")
    def is_external(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean, defaults to false. Whether a user has access only to some internal or private projects. External users can only access projects to which they are explicitly granted access.
        """
        return pulumi.get(self, "is_external")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the user.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def note(self) -> pulumi.Output[Optional[str]]:
        """
        The note associated to the user.
        """
        return pulumi.get(self, "note")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The password of the user.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="projectsLimit")
    def projects_limit(self) -> pulumi.Output[Optional[int]]:
        """
        Integer, defaults to 0.  Number of projects user can create.
        """
        return pulumi.get(self, "projects_limit")

    @property
    @pulumi.getter(name="resetPassword")
    def reset_password(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean, defaults to false. Send user password reset link.
        """
        return pulumi.get(self, "reset_password")

    @property
    @pulumi.getter(name="skipConfirmation")
    def skip_confirmation(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean, defaults to true. Whether to skip confirmation.
        """
        return pulumi.get(self, "skip_confirmation")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        The username of the user.
        """
        return pulumi.get(self, "username")


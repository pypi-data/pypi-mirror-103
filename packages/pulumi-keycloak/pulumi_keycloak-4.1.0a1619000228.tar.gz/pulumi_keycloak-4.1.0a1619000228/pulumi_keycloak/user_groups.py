# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['UserGroupsArgs', 'UserGroups']

@pulumi.input_type
class UserGroupsArgs:
    def __init__(__self__, *,
                 group_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 realm_id: pulumi.Input[str],
                 user_id: pulumi.Input[str],
                 exhaustive: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a UserGroups resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_ids: A list of group IDs that the user is member of.
        :param pulumi.Input[str] realm_id: The realm this group exists in.
        :param pulumi.Input[str] user_id: The ID of the user this resource should manage groups for.
        :param pulumi.Input[bool] exhaustive: Indicates if the list of the user's groups is exhaustive. In this case, groups that are manually added to the user will be removed. Defaults to `true`.
        """
        pulumi.set(__self__, "group_ids", group_ids)
        pulumi.set(__self__, "realm_id", realm_id)
        pulumi.set(__self__, "user_id", user_id)
        if exhaustive is not None:
            pulumi.set(__self__, "exhaustive", exhaustive)

    @property
    @pulumi.getter(name="groupIds")
    def group_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of group IDs that the user is member of.
        """
        return pulumi.get(self, "group_ids")

    @group_ids.setter
    def group_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "group_ids", value)

    @property
    @pulumi.getter(name="realmId")
    def realm_id(self) -> pulumi.Input[str]:
        """
        The realm this group exists in.
        """
        return pulumi.get(self, "realm_id")

    @realm_id.setter
    def realm_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "realm_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        The ID of the user this resource should manage groups for.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter
    def exhaustive(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if the list of the user's groups is exhaustive. In this case, groups that are manually added to the user will be removed. Defaults to `true`.
        """
        return pulumi.get(self, "exhaustive")

    @exhaustive.setter
    def exhaustive(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exhaustive", value)


@pulumi.input_type
class _UserGroupsState:
    def __init__(__self__, *,
                 exhaustive: Optional[pulumi.Input[bool]] = None,
                 group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 realm_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserGroups resources.
        :param pulumi.Input[bool] exhaustive: Indicates if the list of the user's groups is exhaustive. In this case, groups that are manually added to the user will be removed. Defaults to `true`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_ids: A list of group IDs that the user is member of.
        :param pulumi.Input[str] realm_id: The realm this group exists in.
        :param pulumi.Input[str] user_id: The ID of the user this resource should manage groups for.
        """
        if exhaustive is not None:
            pulumi.set(__self__, "exhaustive", exhaustive)
        if group_ids is not None:
            pulumi.set(__self__, "group_ids", group_ids)
        if realm_id is not None:
            pulumi.set(__self__, "realm_id", realm_id)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter
    def exhaustive(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if the list of the user's groups is exhaustive. In this case, groups that are manually added to the user will be removed. Defaults to `true`.
        """
        return pulumi.get(self, "exhaustive")

    @exhaustive.setter
    def exhaustive(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exhaustive", value)

    @property
    @pulumi.getter(name="groupIds")
    def group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of group IDs that the user is member of.
        """
        return pulumi.get(self, "group_ids")

    @group_ids.setter
    def group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "group_ids", value)

    @property
    @pulumi.getter(name="realmId")
    def realm_id(self) -> Optional[pulumi.Input[str]]:
        """
        The realm this group exists in.
        """
        return pulumi.get(self, "realm_id")

    @realm_id.setter
    def realm_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "realm_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the user this resource should manage groups for.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)


class UserGroups(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 exhaustive: Optional[pulumi.Input[bool]] = None,
                 group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 realm_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        This resource does not support import. Instead of importing, feel free to create this resource as if it did not already exist on the server.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] exhaustive: Indicates if the list of the user's groups is exhaustive. In this case, groups that are manually added to the user will be removed. Defaults to `true`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_ids: A list of group IDs that the user is member of.
        :param pulumi.Input[str] realm_id: The realm this group exists in.
        :param pulumi.Input[str] user_id: The ID of the user this resource should manage groups for.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserGroupsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        This resource does not support import. Instead of importing, feel free to create this resource as if it did not already exist on the server.

        :param str resource_name: The name of the resource.
        :param UserGroupsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserGroupsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 exhaustive: Optional[pulumi.Input[bool]] = None,
                 group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 realm_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = UserGroupsArgs.__new__(UserGroupsArgs)

            __props__.__dict__["exhaustive"] = exhaustive
            if group_ids is None and not opts.urn:
                raise TypeError("Missing required property 'group_ids'")
            __props__.__dict__["group_ids"] = group_ids
            if realm_id is None and not opts.urn:
                raise TypeError("Missing required property 'realm_id'")
            __props__.__dict__["realm_id"] = realm_id
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__.__dict__["user_id"] = user_id
        super(UserGroups, __self__).__init__(
            'keycloak:index/userGroups:UserGroups',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            exhaustive: Optional[pulumi.Input[bool]] = None,
            group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            realm_id: Optional[pulumi.Input[str]] = None,
            user_id: Optional[pulumi.Input[str]] = None) -> 'UserGroups':
        """
        Get an existing UserGroups resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] exhaustive: Indicates if the list of the user's groups is exhaustive. In this case, groups that are manually added to the user will be removed. Defaults to `true`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_ids: A list of group IDs that the user is member of.
        :param pulumi.Input[str] realm_id: The realm this group exists in.
        :param pulumi.Input[str] user_id: The ID of the user this resource should manage groups for.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserGroupsState.__new__(_UserGroupsState)

        __props__.__dict__["exhaustive"] = exhaustive
        __props__.__dict__["group_ids"] = group_ids
        __props__.__dict__["realm_id"] = realm_id
        __props__.__dict__["user_id"] = user_id
        return UserGroups(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def exhaustive(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates if the list of the user's groups is exhaustive. In this case, groups that are manually added to the user will be removed. Defaults to `true`.
        """
        return pulumi.get(self, "exhaustive")

    @property
    @pulumi.getter(name="groupIds")
    def group_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of group IDs that the user is member of.
        """
        return pulumi.get(self, "group_ids")

    @property
    @pulumi.getter(name="realmId")
    def realm_id(self) -> pulumi.Output[str]:
        """
        The realm this group exists in.
        """
        return pulumi.get(self, "realm_id")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        The ID of the user this resource should manage groups for.
        """
        return pulumi.get(self, "user_id")


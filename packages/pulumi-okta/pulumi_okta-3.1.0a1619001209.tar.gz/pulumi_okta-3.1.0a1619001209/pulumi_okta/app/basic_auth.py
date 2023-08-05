# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['BasicAuthArgs', 'BasicAuth']

@pulumi.input_type
class BasicAuthArgs:
    def __init__(__self__, *,
                 auth_url: pulumi.Input[str],
                 label: pulumi.Input[str],
                 url: pulumi.Input[str],
                 auto_submit_toolbar: Optional[pulumi.Input[bool]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 hide_ios: Optional[pulumi.Input[bool]] = None,
                 hide_web: Optional[pulumi.Input[bool]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input['BasicAuthUserArgs']]]] = None):
        """
        The set of arguments for constructing a BasicAuth resource.
        :param pulumi.Input[str] auth_url: The URL of the authenticating site for this app.
        :param pulumi.Input[str] label: The Application's display name.
        :param pulumi.Input[str] url: The URL of the sign-in page for this app.
        :param pulumi.Input[bool] auto_submit_toolbar: Display auto submit toolbar.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: Groups associated with the application.
        :param pulumi.Input[bool] hide_ios: Do not display application icon on mobile app.
        :param pulumi.Input[bool] hide_web: Do not display application icon to users.
        :param pulumi.Input[str] status: Status of application. (`"ACTIVE"` or `"INACTIVE"`).
        :param pulumi.Input[Sequence[pulumi.Input['BasicAuthUserArgs']]] users: Users associated with the application.
        """
        pulumi.set(__self__, "auth_url", auth_url)
        pulumi.set(__self__, "label", label)
        pulumi.set(__self__, "url", url)
        if auto_submit_toolbar is not None:
            pulumi.set(__self__, "auto_submit_toolbar", auto_submit_toolbar)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if hide_ios is not None:
            pulumi.set(__self__, "hide_ios", hide_ios)
        if hide_web is not None:
            pulumi.set(__self__, "hide_web", hide_web)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="authUrl")
    def auth_url(self) -> pulumi.Input[str]:
        """
        The URL of the authenticating site for this app.
        """
        return pulumi.get(self, "auth_url")

    @auth_url.setter
    def auth_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "auth_url", value)

    @property
    @pulumi.getter
    def label(self) -> pulumi.Input[str]:
        """
        The Application's display name.
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: pulumi.Input[str]):
        pulumi.set(self, "label", value)

    @property
    @pulumi.getter
    def url(self) -> pulumi.Input[str]:
        """
        The URL of the sign-in page for this app.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: pulumi.Input[str]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter(name="autoSubmitToolbar")
    def auto_submit_toolbar(self) -> Optional[pulumi.Input[bool]]:
        """
        Display auto submit toolbar.
        """
        return pulumi.get(self, "auto_submit_toolbar")

    @auto_submit_toolbar.setter
    def auto_submit_toolbar(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_submit_toolbar", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Groups associated with the application.
        """
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter(name="hideIos")
    def hide_ios(self) -> Optional[pulumi.Input[bool]]:
        """
        Do not display application icon on mobile app.
        """
        return pulumi.get(self, "hide_ios")

    @hide_ios.setter
    def hide_ios(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hide_ios", value)

    @property
    @pulumi.getter(name="hideWeb")
    def hide_web(self) -> Optional[pulumi.Input[bool]]:
        """
        Do not display application icon to users.
        """
        return pulumi.get(self, "hide_web")

    @hide_web.setter
    def hide_web(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hide_web", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of application. (`"ACTIVE"` or `"INACTIVE"`).
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BasicAuthUserArgs']]]]:
        """
        Users associated with the application.
        """
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BasicAuthUserArgs']]]]):
        pulumi.set(self, "users", value)


@pulumi.input_type
class _BasicAuthState:
    def __init__(__self__, *,
                 auth_url: Optional[pulumi.Input[str]] = None,
                 auto_submit_toolbar: Optional[pulumi.Input[bool]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 hide_ios: Optional[pulumi.Input[bool]] = None,
                 hide_web: Optional[pulumi.Input[bool]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sign_on_mode: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input['BasicAuthUserArgs']]]] = None):
        """
        Input properties used for looking up and filtering BasicAuth resources.
        :param pulumi.Input[str] auth_url: The URL of the authenticating site for this app.
        :param pulumi.Input[bool] auto_submit_toolbar: Display auto submit toolbar.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: Groups associated with the application.
        :param pulumi.Input[bool] hide_ios: Do not display application icon on mobile app.
        :param pulumi.Input[bool] hide_web: Do not display application icon to users.
        :param pulumi.Input[str] label: The Application's display name.
        :param pulumi.Input[str] name: name of app.
        :param pulumi.Input[str] sign_on_mode: Sign on mode of application.
        :param pulumi.Input[str] status: Status of application. (`"ACTIVE"` or `"INACTIVE"`).
        :param pulumi.Input[str] url: The URL of the sign-in page for this app.
        :param pulumi.Input[Sequence[pulumi.Input['BasicAuthUserArgs']]] users: Users associated with the application.
        """
        if auth_url is not None:
            pulumi.set(__self__, "auth_url", auth_url)
        if auto_submit_toolbar is not None:
            pulumi.set(__self__, "auto_submit_toolbar", auto_submit_toolbar)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if hide_ios is not None:
            pulumi.set(__self__, "hide_ios", hide_ios)
        if hide_web is not None:
            pulumi.set(__self__, "hide_web", hide_web)
        if label is not None:
            pulumi.set(__self__, "label", label)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if sign_on_mode is not None:
            pulumi.set(__self__, "sign_on_mode", sign_on_mode)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="authUrl")
    def auth_url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the authenticating site for this app.
        """
        return pulumi.get(self, "auth_url")

    @auth_url.setter
    def auth_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auth_url", value)

    @property
    @pulumi.getter(name="autoSubmitToolbar")
    def auto_submit_toolbar(self) -> Optional[pulumi.Input[bool]]:
        """
        Display auto submit toolbar.
        """
        return pulumi.get(self, "auto_submit_toolbar")

    @auto_submit_toolbar.setter
    def auto_submit_toolbar(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_submit_toolbar", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Groups associated with the application.
        """
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter(name="hideIos")
    def hide_ios(self) -> Optional[pulumi.Input[bool]]:
        """
        Do not display application icon on mobile app.
        """
        return pulumi.get(self, "hide_ios")

    @hide_ios.setter
    def hide_ios(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hide_ios", value)

    @property
    @pulumi.getter(name="hideWeb")
    def hide_web(self) -> Optional[pulumi.Input[bool]]:
        """
        Do not display application icon to users.
        """
        return pulumi.get(self, "hide_web")

    @hide_web.setter
    def hide_web(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hide_web", value)

    @property
    @pulumi.getter
    def label(self) -> Optional[pulumi.Input[str]]:
        """
        The Application's display name.
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "label", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        name of app.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="signOnMode")
    def sign_on_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Sign on mode of application.
        """
        return pulumi.get(self, "sign_on_mode")

    @sign_on_mode.setter
    def sign_on_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sign_on_mode", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of application. (`"ACTIVE"` or `"INACTIVE"`).
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the sign-in page for this app.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BasicAuthUserArgs']]]]:
        """
        Users associated with the application.
        """
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BasicAuthUserArgs']]]]):
        pulumi.set(self, "users", value)


class BasicAuth(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auth_url: Optional[pulumi.Input[str]] = None,
                 auto_submit_toolbar: Optional[pulumi.Input[bool]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 hide_ios: Optional[pulumi.Input[bool]] = None,
                 hide_web: Optional[pulumi.Input[bool]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BasicAuthUserArgs']]]]] = None,
                 __props__=None):
        """
        Creates a Basic Auth Application.

        This resource allows you to create and configure a Basic Auth Application.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.app.BasicAuth("example",
            auth_url="https://example.com/auth.html",
            label="Example",
            url="https://example.com/login.html")
        ```

        ## Import

        A Basic Auth App can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:app/basicAuth:BasicAuth example <app id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auth_url: The URL of the authenticating site for this app.
        :param pulumi.Input[bool] auto_submit_toolbar: Display auto submit toolbar.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: Groups associated with the application.
        :param pulumi.Input[bool] hide_ios: Do not display application icon on mobile app.
        :param pulumi.Input[bool] hide_web: Do not display application icon to users.
        :param pulumi.Input[str] label: The Application's display name.
        :param pulumi.Input[str] status: Status of application. (`"ACTIVE"` or `"INACTIVE"`).
        :param pulumi.Input[str] url: The URL of the sign-in page for this app.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BasicAuthUserArgs']]]] users: Users associated with the application.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BasicAuthArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a Basic Auth Application.

        This resource allows you to create and configure a Basic Auth Application.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.app.BasicAuth("example",
            auth_url="https://example.com/auth.html",
            label="Example",
            url="https://example.com/login.html")
        ```

        ## Import

        A Basic Auth App can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:app/basicAuth:BasicAuth example <app id>
        ```

        :param str resource_name: The name of the resource.
        :param BasicAuthArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BasicAuthArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auth_url: Optional[pulumi.Input[str]] = None,
                 auto_submit_toolbar: Optional[pulumi.Input[bool]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 hide_ios: Optional[pulumi.Input[bool]] = None,
                 hide_web: Optional[pulumi.Input[bool]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BasicAuthUserArgs']]]]] = None,
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
            __props__ = BasicAuthArgs.__new__(BasicAuthArgs)

            if auth_url is None and not opts.urn:
                raise TypeError("Missing required property 'auth_url'")
            __props__.__dict__["auth_url"] = auth_url
            __props__.__dict__["auto_submit_toolbar"] = auto_submit_toolbar
            __props__.__dict__["groups"] = groups
            __props__.__dict__["hide_ios"] = hide_ios
            __props__.__dict__["hide_web"] = hide_web
            if label is None and not opts.urn:
                raise TypeError("Missing required property 'label'")
            __props__.__dict__["label"] = label
            __props__.__dict__["status"] = status
            if url is None and not opts.urn:
                raise TypeError("Missing required property 'url'")
            __props__.__dict__["url"] = url
            __props__.__dict__["users"] = users
            __props__.__dict__["name"] = None
            __props__.__dict__["sign_on_mode"] = None
        super(BasicAuth, __self__).__init__(
            'okta:app/basicAuth:BasicAuth',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            auth_url: Optional[pulumi.Input[str]] = None,
            auto_submit_toolbar: Optional[pulumi.Input[bool]] = None,
            groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            hide_ios: Optional[pulumi.Input[bool]] = None,
            hide_web: Optional[pulumi.Input[bool]] = None,
            label: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            sign_on_mode: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            url: Optional[pulumi.Input[str]] = None,
            users: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BasicAuthUserArgs']]]]] = None) -> 'BasicAuth':
        """
        Get an existing BasicAuth resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auth_url: The URL of the authenticating site for this app.
        :param pulumi.Input[bool] auto_submit_toolbar: Display auto submit toolbar.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: Groups associated with the application.
        :param pulumi.Input[bool] hide_ios: Do not display application icon on mobile app.
        :param pulumi.Input[bool] hide_web: Do not display application icon to users.
        :param pulumi.Input[str] label: The Application's display name.
        :param pulumi.Input[str] name: name of app.
        :param pulumi.Input[str] sign_on_mode: Sign on mode of application.
        :param pulumi.Input[str] status: Status of application. (`"ACTIVE"` or `"INACTIVE"`).
        :param pulumi.Input[str] url: The URL of the sign-in page for this app.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BasicAuthUserArgs']]]] users: Users associated with the application.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BasicAuthState.__new__(_BasicAuthState)

        __props__.__dict__["auth_url"] = auth_url
        __props__.__dict__["auto_submit_toolbar"] = auto_submit_toolbar
        __props__.__dict__["groups"] = groups
        __props__.__dict__["hide_ios"] = hide_ios
        __props__.__dict__["hide_web"] = hide_web
        __props__.__dict__["label"] = label
        __props__.__dict__["name"] = name
        __props__.__dict__["sign_on_mode"] = sign_on_mode
        __props__.__dict__["status"] = status
        __props__.__dict__["url"] = url
        __props__.__dict__["users"] = users
        return BasicAuth(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authUrl")
    def auth_url(self) -> pulumi.Output[str]:
        """
        The URL of the authenticating site for this app.
        """
        return pulumi.get(self, "auth_url")

    @property
    @pulumi.getter(name="autoSubmitToolbar")
    def auto_submit_toolbar(self) -> pulumi.Output[Optional[bool]]:
        """
        Display auto submit toolbar.
        """
        return pulumi.get(self, "auto_submit_toolbar")

    @property
    @pulumi.getter
    def groups(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Groups associated with the application.
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter(name="hideIos")
    def hide_ios(self) -> pulumi.Output[Optional[bool]]:
        """
        Do not display application icon on mobile app.
        """
        return pulumi.get(self, "hide_ios")

    @property
    @pulumi.getter(name="hideWeb")
    def hide_web(self) -> pulumi.Output[Optional[bool]]:
        """
        Do not display application icon to users.
        """
        return pulumi.get(self, "hide_web")

    @property
    @pulumi.getter
    def label(self) -> pulumi.Output[str]:
        """
        The Application's display name.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        name of app.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="signOnMode")
    def sign_on_mode(self) -> pulumi.Output[str]:
        """
        Sign on mode of application.
        """
        return pulumi.get(self, "sign_on_mode")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Status of application. (`"ACTIVE"` or `"INACTIVE"`).
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        The URL of the sign-in page for this app.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter
    def users(self) -> pulumi.Output[Optional[Sequence['outputs.BasicAuthUser']]]:
        """
        Users associated with the application.
        """
        return pulumi.get(self, "users")


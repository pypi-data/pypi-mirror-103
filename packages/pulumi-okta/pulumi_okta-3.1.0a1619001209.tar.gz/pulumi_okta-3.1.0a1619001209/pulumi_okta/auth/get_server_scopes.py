# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetServerScopesResult',
    'AwaitableGetServerScopesResult',
    'get_server_scopes',
]

@pulumi.output_type
class GetServerScopesResult:
    """
    A collection of values returned by getServerScopes.
    """
    def __init__(__self__, auth_server_id=None, id=None, scopes=None):
        if auth_server_id and not isinstance(auth_server_id, str):
            raise TypeError("Expected argument 'auth_server_id' to be a str")
        pulumi.set(__self__, "auth_server_id", auth_server_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if scopes and not isinstance(scopes, list):
            raise TypeError("Expected argument 'scopes' to be a list")
        pulumi.set(__self__, "scopes", scopes)

    @property
    @pulumi.getter(name="authServerId")
    def auth_server_id(self) -> str:
        return pulumi.get(self, "auth_server_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def scopes(self) -> Sequence['outputs.GetServerScopesScopeResult']:
        """
        collection of authorization server scopes retrieved from Okta with the following properties.
        """
        return pulumi.get(self, "scopes")


class AwaitableGetServerScopesResult(GetServerScopesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerScopesResult(
            auth_server_id=self.auth_server_id,
            id=self.id,
            scopes=self.scopes)


def get_server_scopes(auth_server_id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerScopesResult:
    """
    Use this data source to retrieve a list of authorization server scopes from Okta.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_okta as okta

    test = okta.auth.get_server_scopes(auth_server_id="default")
    ```


    :param str auth_server_id: Auth server ID.
    """
    __args__ = dict()
    __args__['authServerId'] = auth_server_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('okta:auth/getServerScopes:getServerScopes', __args__, opts=opts, typ=GetServerScopesResult).value

    return AwaitableGetServerScopesResult(
        auth_server_id=__ret__.auth_server_id,
        id=__ret__.id,
        scopes=__ret__.scopes)

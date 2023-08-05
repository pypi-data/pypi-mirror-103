# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetClusterDriverResult',
    'AwaitableGetClusterDriverResult',
    'get_cluster_driver',
]

@pulumi.output_type
class GetClusterDriverResult:
    """
    A collection of values returned by getClusterDriver.
    """
    def __init__(__self__, active=None, actual_url=None, annotations=None, builtin=None, checksum=None, id=None, labels=None, name=None, ui_url=None, url=None, whitelist_domains=None):
        if active and not isinstance(active, bool):
            raise TypeError("Expected argument 'active' to be a bool")
        pulumi.set(__self__, "active", active)
        if actual_url and not isinstance(actual_url, str):
            raise TypeError("Expected argument 'actual_url' to be a str")
        pulumi.set(__self__, "actual_url", actual_url)
        if annotations and not isinstance(annotations, dict):
            raise TypeError("Expected argument 'annotations' to be a dict")
        pulumi.set(__self__, "annotations", annotations)
        if builtin and not isinstance(builtin, bool):
            raise TypeError("Expected argument 'builtin' to be a bool")
        pulumi.set(__self__, "builtin", builtin)
        if checksum and not isinstance(checksum, str):
            raise TypeError("Expected argument 'checksum' to be a str")
        pulumi.set(__self__, "checksum", checksum)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if ui_url and not isinstance(ui_url, str):
            raise TypeError("Expected argument 'ui_url' to be a str")
        pulumi.set(__self__, "ui_url", ui_url)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)
        if whitelist_domains and not isinstance(whitelist_domains, list):
            raise TypeError("Expected argument 'whitelist_domains' to be a list")
        pulumi.set(__self__, "whitelist_domains", whitelist_domains)

    @property
    @pulumi.getter
    def active(self) -> bool:
        """
        (Computed) Specify if the cluster driver state (bool)
        """
        return pulumi.get(self, "active")

    @property
    @pulumi.getter(name="actualUrl")
    def actual_url(self) -> str:
        """
        (Computed) Actual url of the cluster driver (string)
        """
        return pulumi.get(self, "actual_url")

    @property
    @pulumi.getter
    def annotations(self) -> Mapping[str, Any]:
        """
        (Computed) Annotations of the resource (map)
        """
        return pulumi.get(self, "annotations")

    @property
    @pulumi.getter
    def builtin(self) -> bool:
        """
        (Computed) Specify whether the cluster driver is an internal cluster driver or not (bool)
        """
        return pulumi.get(self, "builtin")

    @property
    @pulumi.getter
    def checksum(self) -> str:
        """
        (Computed) Verify that the downloaded driver matches the expected checksum (string)
        """
        return pulumi.get(self, "checksum")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, Any]:
        """
        (Computed) Labels of the resource (map)
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="uiUrl")
    def ui_url(self) -> str:
        """
        (Computed) The URL to load for customized Add Clusters screen for this driver (string)
        """
        return pulumi.get(self, "ui_url")

    @property
    @pulumi.getter
    def url(self) -> str:
        return pulumi.get(self, "url")

    @property
    @pulumi.getter(name="whitelistDomains")
    def whitelist_domains(self) -> Sequence[str]:
        """
        (Computed) Domains to whitelist for the ui (list)
        """
        return pulumi.get(self, "whitelist_domains")


class AwaitableGetClusterDriverResult(GetClusterDriverResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterDriverResult(
            active=self.active,
            actual_url=self.actual_url,
            annotations=self.annotations,
            builtin=self.builtin,
            checksum=self.checksum,
            id=self.id,
            labels=self.labels,
            name=self.name,
            ui_url=self.ui_url,
            url=self.url,
            whitelist_domains=self.whitelist_domains)


def get_cluster_driver(name: Optional[str] = None,
                       url: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterDriverResult:
    """
    Use this data source to retrieve information about a Rancher v2 Cluster Driver resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_rancher2 as rancher2

    foo = rancher2.get_cluster_driver(name="foo")
    ```


    :param str name: Name of the cluster driver (string)
    :param str url: The URL to download the machine driver binary for 64-bit Linux (string)
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['url'] = url
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('rancher2:index/getClusterDriver:getClusterDriver', __args__, opts=opts, typ=GetClusterDriverResult).value

    return AwaitableGetClusterDriverResult(
        active=__ret__.active,
        actual_url=__ret__.actual_url,
        annotations=__ret__.annotations,
        builtin=__ret__.builtin,
        checksum=__ret__.checksum,
        id=__ret__.id,
        labels=__ret__.labels,
        name=__ret__.name,
        ui_url=__ret__.ui_url,
        url=__ret__.url,
        whitelist_domains=__ret__.whitelist_domains)

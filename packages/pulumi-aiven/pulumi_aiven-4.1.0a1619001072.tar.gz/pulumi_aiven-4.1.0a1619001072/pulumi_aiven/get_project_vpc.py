# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetProjectVpcResult',
    'AwaitableGetProjectVpcResult',
    'get_project_vpc',
]

@pulumi.output_type
class GetProjectVpcResult:
    """
    A collection of values returned by getProjectVpc.
    """
    def __init__(__self__, cloud_name=None, id=None, network_cidr=None, project=None, state=None):
        if cloud_name and not isinstance(cloud_name, str):
            raise TypeError("Expected argument 'cloud_name' to be a str")
        pulumi.set(__self__, "cloud_name", cloud_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if network_cidr and not isinstance(network_cidr, str):
            raise TypeError("Expected argument 'network_cidr' to be a str")
        pulumi.set(__self__, "network_cidr", network_cidr)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="cloudName")
    def cloud_name(self) -> str:
        return pulumi.get(self, "cloud_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="networkCidr")
    def network_cidr(self) -> Optional[str]:
        """
        defines the network CIDR of the VPC.
        """
        return pulumi.get(self, "network_cidr")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        ia a computed property that tells the current state of the VPC. This property cannot be
        set, only read.
        """
        return pulumi.get(self, "state")


class AwaitableGetProjectVpcResult(GetProjectVpcResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectVpcResult(
            cloud_name=self.cloud_name,
            id=self.id,
            network_cidr=self.network_cidr,
            project=self.project,
            state=self.state)


def get_project_vpc(cloud_name: Optional[str] = None,
                    network_cidr: Optional[str] = None,
                    project: Optional[str] = None,
                    state: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectVpcResult:
    """
    ## # Project VPC Data Source

    The Project VPC data source provides information about the existing Aiven Project VPC.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aiven as aiven

    myvpc = aiven.get_project_vpc(cloud_name="google-europe-west1",
        project=aiven_project["myproject"]["project"])
    ```


    :param str cloud_name: defines where the cloud provider and region where the service is hosted
           in. See the Service resource for additional information.
    :param str network_cidr: defines the network CIDR of the VPC.
    :param str project: defines the project the VPC belongs to.
    :param str state: ia a computed property that tells the current state of the VPC. This property cannot be
           set, only read.
    """
    __args__ = dict()
    __args__['cloudName'] = cloud_name
    __args__['networkCidr'] = network_cidr
    __args__['project'] = project
    __args__['state'] = state
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aiven:index/getProjectVpc:getProjectVpc', __args__, opts=opts, typ=GetProjectVpcResult).value

    return AwaitableGetProjectVpcResult(
        cloud_name=__ret__.cloud_name,
        id=__ret__.id,
        network_cidr=__ret__.network_cidr,
        project=__ret__.project,
        state=__ret__.state)

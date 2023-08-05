# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ProviderArgs', 'Provider']

@pulumi.input_type
class ProviderArgs:
    def __init__(__self__, *,
                 address: Optional[pulumi.Input[str]] = None,
                 ca_file: Optional[pulumi.Input[str]] = None,
                 ca_path: Optional[pulumi.Input[str]] = None,
                 ca_pem: Optional[pulumi.Input[str]] = None,
                 cert_file: Optional[pulumi.Input[str]] = None,
                 cert_pem: Optional[pulumi.Input[str]] = None,
                 datacenter: Optional[pulumi.Input[str]] = None,
                 http_auth: Optional[pulumi.Input[str]] = None,
                 insecure_https: Optional[pulumi.Input[bool]] = None,
                 key_file: Optional[pulumi.Input[str]] = None,
                 key_pem: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 scheme: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Provider resource.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if ca_file is not None:
            pulumi.set(__self__, "ca_file", ca_file)
        if ca_path is not None:
            pulumi.set(__self__, "ca_path", ca_path)
        if ca_pem is not None:
            pulumi.set(__self__, "ca_pem", ca_pem)
        if cert_file is not None:
            pulumi.set(__self__, "cert_file", cert_file)
        if cert_pem is not None:
            pulumi.set(__self__, "cert_pem", cert_pem)
        if datacenter is not None:
            pulumi.set(__self__, "datacenter", datacenter)
        if http_auth is not None:
            pulumi.set(__self__, "http_auth", http_auth)
        if insecure_https is not None:
            pulumi.set(__self__, "insecure_https", insecure_https)
        if key_file is not None:
            pulumi.set(__self__, "key_file", key_file)
        if key_pem is not None:
            pulumi.set(__self__, "key_pem", key_pem)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if scheme is not None:
            pulumi.set(__self__, "scheme", scheme)
        if token is not None:
            pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="caFile")
    def ca_file(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "ca_file")

    @ca_file.setter
    def ca_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ca_file", value)

    @property
    @pulumi.getter(name="caPath")
    def ca_path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "ca_path")

    @ca_path.setter
    def ca_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ca_path", value)

    @property
    @pulumi.getter(name="caPem")
    def ca_pem(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "ca_pem")

    @ca_pem.setter
    def ca_pem(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ca_pem", value)

    @property
    @pulumi.getter(name="certFile")
    def cert_file(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cert_file")

    @cert_file.setter
    def cert_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cert_file", value)

    @property
    @pulumi.getter(name="certPem")
    def cert_pem(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cert_pem")

    @cert_pem.setter
    def cert_pem(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cert_pem", value)

    @property
    @pulumi.getter
    def datacenter(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "datacenter")

    @datacenter.setter
    def datacenter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "datacenter", value)

    @property
    @pulumi.getter(name="httpAuth")
    def http_auth(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "http_auth")

    @http_auth.setter
    def http_auth(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_auth", value)

    @property
    @pulumi.getter(name="insecureHttps")
    def insecure_https(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "insecure_https")

    @insecure_https.setter
    def insecure_https(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "insecure_https", value)

    @property
    @pulumi.getter(name="keyFile")
    def key_file(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "key_file")

    @key_file.setter
    def key_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_file", value)

    @property
    @pulumi.getter(name="keyPem")
    def key_pem(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "key_pem")

    @key_pem.setter
    def key_pem(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_pem", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter
    def scheme(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "scheme")

    @scheme.setter
    def scheme(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scheme", value)

    @property
    @pulumi.getter
    def token(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "token")

    @token.setter
    def token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token", value)


class Provider(pulumi.ProviderResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 ca_file: Optional[pulumi.Input[str]] = None,
                 ca_path: Optional[pulumi.Input[str]] = None,
                 ca_pem: Optional[pulumi.Input[str]] = None,
                 cert_file: Optional[pulumi.Input[str]] = None,
                 cert_pem: Optional[pulumi.Input[str]] = None,
                 datacenter: Optional[pulumi.Input[str]] = None,
                 http_auth: Optional[pulumi.Input[str]] = None,
                 insecure_https: Optional[pulumi.Input[bool]] = None,
                 key_file: Optional[pulumi.Input[str]] = None,
                 key_pem: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 scheme: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The provider type for the consul package. By default, resources use package-wide configuration
        settings, however an explicit `Provider` instance may be created and passed during resource
        construction to achieve fine-grained programmatic control over provider settings. See the
        [documentation](https://www.pulumi.com/docs/reference/programming-model/#providers) for more information.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ProviderArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The provider type for the consul package. By default, resources use package-wide configuration
        settings, however an explicit `Provider` instance may be created and passed during resource
        construction to achieve fine-grained programmatic control over provider settings. See the
        [documentation](https://www.pulumi.com/docs/reference/programming-model/#providers) for more information.

        :param str resource_name: The name of the resource.
        :param ProviderArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProviderArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 ca_file: Optional[pulumi.Input[str]] = None,
                 ca_path: Optional[pulumi.Input[str]] = None,
                 ca_pem: Optional[pulumi.Input[str]] = None,
                 cert_file: Optional[pulumi.Input[str]] = None,
                 cert_pem: Optional[pulumi.Input[str]] = None,
                 datacenter: Optional[pulumi.Input[str]] = None,
                 http_auth: Optional[pulumi.Input[str]] = None,
                 insecure_https: Optional[pulumi.Input[bool]] = None,
                 key_file: Optional[pulumi.Input[str]] = None,
                 key_pem: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 scheme: Optional[pulumi.Input[str]] = None,
                 token: Optional[pulumi.Input[str]] = None,
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
            __props__ = ProviderArgs.__new__(ProviderArgs)

            __props__.__dict__["address"] = address
            __props__.__dict__["ca_file"] = ca_file
            __props__.__dict__["ca_path"] = ca_path
            __props__.__dict__["ca_pem"] = ca_pem
            __props__.__dict__["cert_file"] = cert_file
            __props__.__dict__["cert_pem"] = cert_pem
            __props__.__dict__["datacenter"] = datacenter
            __props__.__dict__["http_auth"] = http_auth
            __props__.__dict__["insecure_https"] = pulumi.Output.from_input(insecure_https).apply(pulumi.runtime.to_json) if insecure_https is not None else None
            __props__.__dict__["key_file"] = key_file
            __props__.__dict__["key_pem"] = key_pem
            __props__.__dict__["namespace"] = namespace
            __props__.__dict__["scheme"] = scheme
            __props__.__dict__["token"] = token
        super(Provider, __self__).__init__(
            'consul',
            resource_name,
            __props__,
            opts)


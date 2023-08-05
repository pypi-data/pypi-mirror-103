# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'RouteDestinationArgs',
    'RouteSourceArgs',
    'UpstreamHealthchecksArgs',
    'UpstreamHealthchecksActiveArgs',
    'UpstreamHealthchecksActiveHealthyArgs',
    'UpstreamHealthchecksActiveUnhealthyArgs',
    'UpstreamHealthchecksPassiveArgs',
    'UpstreamHealthchecksPassiveHealthyArgs',
    'UpstreamHealthchecksPassiveUnhealthyArgs',
]

@pulumi.input_type
class RouteDestinationArgs:
    def __init__(__self__, *,
                 ip: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None):
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def ip(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "ip")

    @ip.setter
    def ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)


@pulumi.input_type
class RouteSourceArgs:
    def __init__(__self__, *,
                 ip: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None):
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def ip(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "ip")

    @ip.setter
    def ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)


@pulumi.input_type
class UpstreamHealthchecksArgs:
    def __init__(__self__, *,
                 active: Optional[pulumi.Input['UpstreamHealthchecksActiveArgs']] = None,
                 passive: Optional[pulumi.Input['UpstreamHealthchecksPassiveArgs']] = None):
        if active is not None:
            pulumi.set(__self__, "active", active)
        if passive is not None:
            pulumi.set(__self__, "passive", passive)

    @property
    @pulumi.getter
    def active(self) -> Optional[pulumi.Input['UpstreamHealthchecksActiveArgs']]:
        return pulumi.get(self, "active")

    @active.setter
    def active(self, value: Optional[pulumi.Input['UpstreamHealthchecksActiveArgs']]):
        pulumi.set(self, "active", value)

    @property
    @pulumi.getter
    def passive(self) -> Optional[pulumi.Input['UpstreamHealthchecksPassiveArgs']]:
        return pulumi.get(self, "passive")

    @passive.setter
    def passive(self, value: Optional[pulumi.Input['UpstreamHealthchecksPassiveArgs']]):
        pulumi.set(self, "passive", value)


@pulumi.input_type
class UpstreamHealthchecksActiveArgs:
    def __init__(__self__, *,
                 concurrency: Optional[pulumi.Input[int]] = None,
                 healthy: Optional[pulumi.Input['UpstreamHealthchecksActiveHealthyArgs']] = None,
                 http_path: Optional[pulumi.Input[str]] = None,
                 https_sni: Optional[pulumi.Input[str]] = None,
                 https_verify_certificate: Optional[pulumi.Input[bool]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 unhealthy: Optional[pulumi.Input['UpstreamHealthchecksActiveUnhealthyArgs']] = None):
        if concurrency is not None:
            pulumi.set(__self__, "concurrency", concurrency)
        if healthy is not None:
            pulumi.set(__self__, "healthy", healthy)
        if http_path is not None:
            pulumi.set(__self__, "http_path", http_path)
        if https_sni is not None:
            pulumi.set(__self__, "https_sni", https_sni)
        if https_verify_certificate is not None:
            pulumi.set(__self__, "https_verify_certificate", https_verify_certificate)
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if unhealthy is not None:
            pulumi.set(__self__, "unhealthy", unhealthy)

    @property
    @pulumi.getter
    def concurrency(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "concurrency")

    @concurrency.setter
    def concurrency(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "concurrency", value)

    @property
    @pulumi.getter
    def healthy(self) -> Optional[pulumi.Input['UpstreamHealthchecksActiveHealthyArgs']]:
        return pulumi.get(self, "healthy")

    @healthy.setter
    def healthy(self, value: Optional[pulumi.Input['UpstreamHealthchecksActiveHealthyArgs']]):
        pulumi.set(self, "healthy", value)

    @property
    @pulumi.getter(name="httpPath")
    def http_path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "http_path")

    @http_path.setter
    def http_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_path", value)

    @property
    @pulumi.getter(name="httpsSni")
    def https_sni(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "https_sni")

    @https_sni.setter
    def https_sni(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "https_sni", value)

    @property
    @pulumi.getter(name="httpsVerifyCertificate")
    def https_verify_certificate(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "https_verify_certificate")

    @https_verify_certificate.setter
    def https_verify_certificate(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "https_verify_certificate", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def unhealthy(self) -> Optional[pulumi.Input['UpstreamHealthchecksActiveUnhealthyArgs']]:
        return pulumi.get(self, "unhealthy")

    @unhealthy.setter
    def unhealthy(self, value: Optional[pulumi.Input['UpstreamHealthchecksActiveUnhealthyArgs']]):
        pulumi.set(self, "unhealthy", value)


@pulumi.input_type
class UpstreamHealthchecksActiveHealthyArgs:
    def __init__(__self__, *,
                 http_statuses: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 successes: Optional[pulumi.Input[int]] = None):
        if http_statuses is not None:
            pulumi.set(__self__, "http_statuses", http_statuses)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if successes is not None:
            pulumi.set(__self__, "successes", successes)

    @property
    @pulumi.getter(name="httpStatuses")
    def http_statuses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        return pulumi.get(self, "http_statuses")

    @http_statuses.setter
    def http_statuses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "http_statuses", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter
    def successes(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "successes")

    @successes.setter
    def successes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "successes", value)


@pulumi.input_type
class UpstreamHealthchecksActiveUnhealthyArgs:
    def __init__(__self__, *,
                 http_failures: Optional[pulumi.Input[int]] = None,
                 http_statuses: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 tcp_failures: Optional[pulumi.Input[int]] = None,
                 timeouts: Optional[pulumi.Input[int]] = None):
        if http_failures is not None:
            pulumi.set(__self__, "http_failures", http_failures)
        if http_statuses is not None:
            pulumi.set(__self__, "http_statuses", http_statuses)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if tcp_failures is not None:
            pulumi.set(__self__, "tcp_failures", tcp_failures)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="httpFailures")
    def http_failures(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "http_failures")

    @http_failures.setter
    def http_failures(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "http_failures", value)

    @property
    @pulumi.getter(name="httpStatuses")
    def http_statuses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        return pulumi.get(self, "http_statuses")

    @http_statuses.setter
    def http_statuses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "http_statuses", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="tcpFailures")
    def tcp_failures(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "tcp_failures")

    @tcp_failures.setter
    def tcp_failures(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "tcp_failures", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeouts", value)


@pulumi.input_type
class UpstreamHealthchecksPassiveArgs:
    def __init__(__self__, *,
                 healthy: Optional[pulumi.Input['UpstreamHealthchecksPassiveHealthyArgs']] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 unhealthy: Optional[pulumi.Input['UpstreamHealthchecksPassiveUnhealthyArgs']] = None):
        if healthy is not None:
            pulumi.set(__self__, "healthy", healthy)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if unhealthy is not None:
            pulumi.set(__self__, "unhealthy", unhealthy)

    @property
    @pulumi.getter
    def healthy(self) -> Optional[pulumi.Input['UpstreamHealthchecksPassiveHealthyArgs']]:
        return pulumi.get(self, "healthy")

    @healthy.setter
    def healthy(self, value: Optional[pulumi.Input['UpstreamHealthchecksPassiveHealthyArgs']]):
        pulumi.set(self, "healthy", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def unhealthy(self) -> Optional[pulumi.Input['UpstreamHealthchecksPassiveUnhealthyArgs']]:
        return pulumi.get(self, "unhealthy")

    @unhealthy.setter
    def unhealthy(self, value: Optional[pulumi.Input['UpstreamHealthchecksPassiveUnhealthyArgs']]):
        pulumi.set(self, "unhealthy", value)


@pulumi.input_type
class UpstreamHealthchecksPassiveHealthyArgs:
    def __init__(__self__, *,
                 http_statuses: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 successes: Optional[pulumi.Input[int]] = None):
        if http_statuses is not None:
            pulumi.set(__self__, "http_statuses", http_statuses)
        if successes is not None:
            pulumi.set(__self__, "successes", successes)

    @property
    @pulumi.getter(name="httpStatuses")
    def http_statuses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        return pulumi.get(self, "http_statuses")

    @http_statuses.setter
    def http_statuses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "http_statuses", value)

    @property
    @pulumi.getter
    def successes(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "successes")

    @successes.setter
    def successes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "successes", value)


@pulumi.input_type
class UpstreamHealthchecksPassiveUnhealthyArgs:
    def __init__(__self__, *,
                 http_failures: Optional[pulumi.Input[int]] = None,
                 http_statuses: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 tcp_failures: Optional[pulumi.Input[int]] = None,
                 timeouts: Optional[pulumi.Input[int]] = None):
        if http_failures is not None:
            pulumi.set(__self__, "http_failures", http_failures)
        if http_statuses is not None:
            pulumi.set(__self__, "http_statuses", http_statuses)
        if tcp_failures is not None:
            pulumi.set(__self__, "tcp_failures", tcp_failures)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="httpFailures")
    def http_failures(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "http_failures")

    @http_failures.setter
    def http_failures(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "http_failures", value)

    @property
    @pulumi.getter(name="httpStatuses")
    def http_statuses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        return pulumi.get(self, "http_statuses")

    @http_statuses.setter
    def http_statuses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "http_statuses", value)

    @property
    @pulumi.getter(name="tcpFailures")
    def tcp_failures(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "tcp_failures")

    @tcp_failures.setter
    def tcp_failures(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "tcp_failures", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeouts", value)



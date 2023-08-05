# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'authentication_plugin',
    'endpoint',
    'max_conn_lifetime_sec',
    'max_open_conns',
    'password',
    'proxy',
    'tls',
    'username',
]

__config__ = pulumi.Config('mysql')

authentication_plugin = __config__.get('authenticationPlugin')

endpoint = __config__.get('endpoint')

max_conn_lifetime_sec = __config__.get('maxConnLifetimeSec')

max_open_conns = __config__.get('maxOpenConns')

password = __config__.get('password')

proxy = __config__.get('proxy') or _utilities.get_env('ALL_PROXY', 'all_proxy')

tls = __config__.get('tls') or (_utilities.get_env('MYSQL_TLS_CONFIG') or 'false')

username = __config__.get('username')


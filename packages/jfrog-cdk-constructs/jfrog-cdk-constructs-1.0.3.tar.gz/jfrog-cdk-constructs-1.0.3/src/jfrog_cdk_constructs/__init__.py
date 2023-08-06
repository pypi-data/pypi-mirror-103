'''
[![NPM version](https://badge.fury.io/js/jfrog-cdk-constructs.svg)](https://badge.fury.io/js/jfrog-cdk-constructs)
![Release](https://github.com/anshrma/jfrog-cdk-constructs/workflows/Release/badge.svg)

# jfrog-cdk-constructs

AWS CDK construct library that allows you to Quickly start with JFrog Platform on Amazon EKS

# Sample
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_eks
import aws_cdk.aws_rds
import aws_cdk.core


class JFrogEks(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="jfrog-cdk-constructs.JFrogEks",
):
    '''
    :summary: The JFrogEks class.
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        eks_props: aws_cdk.aws_eks.ClusterProps,
        rds_props: "RdsDatabaseProps",
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param eks_props: 
        :param rds_props: 

        :access: public
        :since: 0.1.0
        :summary: Constructs a new instance of the JFrogEks class.
        '''
        props = JFrogEksProps(eks_props=eks_props, rds_props=rds_props)

        jsii.create(JFrogEks, self, [scope, id, props])


@jsii.data_type(
    jsii_type="jfrog-cdk-constructs.JFrogEksProps",
    jsii_struct_bases=[],
    name_mapping={"eks_props": "eksProps", "rds_props": "rdsProps"},
)
class JFrogEksProps:
    def __init__(
        self,
        *,
        eks_props: aws_cdk.aws_eks.ClusterProps,
        rds_props: "RdsDatabaseProps",
    ) -> None:
        '''
        :param eks_props: 
        :param rds_props: 

        :summary: The properties for the JFrogEks class.
        '''
        if isinstance(eks_props, dict):
            eks_props = aws_cdk.aws_eks.ClusterProps(**eks_props)
        if isinstance(rds_props, dict):
            rds_props = RdsDatabaseProps(**rds_props)
        self._values: typing.Dict[str, typing.Any] = {
            "eks_props": eks_props,
            "rds_props": rds_props,
        }

    @builtins.property
    def eks_props(self) -> aws_cdk.aws_eks.ClusterProps:
        result = self._values.get("eks_props")
        assert result is not None, "Required property 'eks_props' is missing"
        return typing.cast(aws_cdk.aws_eks.ClusterProps, result)

    @builtins.property
    def rds_props(self) -> "RdsDatabaseProps":
        result = self._values.get("rds_props")
        assert result is not None, "Required property 'rds_props' is missing"
        return typing.cast("RdsDatabaseProps", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JFrogEksProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="jfrog-cdk-constructs.RdsDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "databasename": "databasename",
        "postgresversion": "postgresversion",
        "username": "username",
    },
)
class RdsDatabaseProps:
    def __init__(
        self,
        *,
        databasename: builtins.str,
        postgresversion: aws_cdk.aws_rds.PostgresEngineVersion,
        username: builtins.str,
    ) -> None:
        '''
        :param databasename: 
        :param postgresversion: 
        :param username: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "databasename": databasename,
            "postgresversion": postgresversion,
            "username": username,
        }

    @builtins.property
    def databasename(self) -> builtins.str:
        result = self._values.get("databasename")
        assert result is not None, "Required property 'databasename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresversion(self) -> aws_cdk.aws_rds.PostgresEngineVersion:
        result = self._values.get("postgresversion")
        assert result is not None, "Required property 'postgresversion' is missing"
        return typing.cast(aws_cdk.aws_rds.PostgresEngineVersion, result)

    @builtins.property
    def username(self) -> builtins.str:
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "JFrogEks",
    "JFrogEksProps",
    "RdsDatabaseProps",
]

publication.publish()

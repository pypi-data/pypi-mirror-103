'''
# jfrog-cdk-constructs

[![NPM version](https://badge.fury.io/js/jfrog-cdk-constructs.svg)](https://badge.fury.io/js/jfrog-cdk-constructs)
[![PyPI version](https://badge.fury.io/py/jfrog-cdk-constructs.svg)](https://badge.fury.io/py/jfrog-cdk-constructs)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/jfrog-cdk-constructs?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/jfrog-cdk-constructs?label=pypi&color=blue)

Use this JFrog CDK Construct Library to deploy JFrog Platform on Amazon EKS .

This CDK library automatically creates and configures recommended architecture on AWS by:

* Use of Amazon S3 for persistance
* Amazon RDS for database tier
* User Configurable EKS cluter and EKS nodes

## npm Package Installation:

```
yarn add --dev jfrog-cdk-constructs
# or
npm install jfrog-cdk-constructs --save-dev
```

## PyPI Package Installation:

```
pip install jfrog-cdk-constructs
```

# Sample

Try out https://github.com/anshrma/sample-jfrog-eks for the complete sample application and instructions.

## Resources to learn about CDK

* [CDK TypeScript Workshop](https://cdkworkshop.com/20-typescript.html)
* [Video Introducing CDK by AWS with Demo](https://youtu.be/ZWCvNFUN-sU)
* [CDK Concepts](https://youtu.be/9As_ZIjUGmY)
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
        eks_cluster_props: aws_cdk.aws_eks.ClusterProps,
        eks_nodes_props: aws_cdk.aws_eks.AutoScalingGroupCapacityOptions,
        rds_props: "RdsDatabaseProps",
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param eks_cluster_props: 
        :param eks_nodes_props: 
        :param rds_props: 

        :access: public
        :since: 0.1.0
        :summary: Constructs a new instance of the JFrogEks class.
        '''
        props = JFrogEksProps(
            eks_cluster_props=eks_cluster_props,
            eks_nodes_props=eks_nodes_props,
            rds_props=rds_props,
        )

        jsii.create(JFrogEks, self, [scope, id, props])


@jsii.data_type(
    jsii_type="jfrog-cdk-constructs.JFrogEksProps",
    jsii_struct_bases=[],
    name_mapping={
        "eks_cluster_props": "eksClusterProps",
        "eks_nodes_props": "eksNodesProps",
        "rds_props": "rdsProps",
    },
)
class JFrogEksProps:
    def __init__(
        self,
        *,
        eks_cluster_props: aws_cdk.aws_eks.ClusterProps,
        eks_nodes_props: aws_cdk.aws_eks.AutoScalingGroupCapacityOptions,
        rds_props: "RdsDatabaseProps",
    ) -> None:
        '''
        :param eks_cluster_props: 
        :param eks_nodes_props: 
        :param rds_props: 

        :summary: The properties for the JFrogEks class.
        '''
        if isinstance(eks_cluster_props, dict):
            eks_cluster_props = aws_cdk.aws_eks.ClusterProps(**eks_cluster_props)
        if isinstance(eks_nodes_props, dict):
            eks_nodes_props = aws_cdk.aws_eks.AutoScalingGroupCapacityOptions(**eks_nodes_props)
        if isinstance(rds_props, dict):
            rds_props = RdsDatabaseProps(**rds_props)
        self._values: typing.Dict[str, typing.Any] = {
            "eks_cluster_props": eks_cluster_props,
            "eks_nodes_props": eks_nodes_props,
            "rds_props": rds_props,
        }

    @builtins.property
    def eks_cluster_props(self) -> aws_cdk.aws_eks.ClusterProps:
        '''
        :see: https://docs.aws.amazon.com/cdk/api/latest/docs/
        :aws-cdk_aws-eks: .ClusterProps.html
        :summary: EKS Cluster properties
        '''
        result = self._values.get("eks_cluster_props")
        assert result is not None, "Required property 'eks_cluster_props' is missing"
        return typing.cast(aws_cdk.aws_eks.ClusterProps, result)

    @builtins.property
    def eks_nodes_props(self) -> aws_cdk.aws_eks.AutoScalingGroupCapacityOptions:
        '''
        :see: https://docs.aws.amazon.com/cdk/api/latest/docs/
        :aws-cdk_aws-eks: .AutoScalingGroupCapacityOptions.html
        :summary: EKS Nodes properties
        '''
        result = self._values.get("eks_nodes_props")
        assert result is not None, "Required property 'eks_nodes_props' is missing"
        return typing.cast(aws_cdk.aws_eks.AutoScalingGroupCapacityOptions, result)

    @builtins.property
    def rds_props(self) -> "RdsDatabaseProps":
        '''
        :summary: RDS Database properties
        '''
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
        '''
        :summary: Database name to be used for Artifactory
        '''
        result = self._values.get("databasename")
        assert result is not None, "Required property 'databasename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresversion(self) -> aws_cdk.aws_rds.PostgresEngineVersion:
        '''
        :see: https://docs.aws.amazon.com/cdk/api/latest/docs/
        :aws-cdk_aws-rds: .PostgresEngineVersion.html
        :summary: RDS PostGres Engine Version
        '''
        result = self._values.get("postgresversion")
        assert result is not None, "Required property 'postgresversion' is missing"
        return typing.cast(aws_cdk.aws_rds.PostgresEngineVersion, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''
        :summary: Master username to be used for RDS
        '''
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

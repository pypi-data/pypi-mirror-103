'''
[![NPM version](https://badge.fury.io/js/jfrog-cdk-constructs.svg)](https://badge.fury.io/js/jfrog-cdk-constructs)
[![PyPI version](https://badge.fury.io/py/jfrog-cdk-constructs.svg)](https://badge.fury.io/py/jfrog-cdk-constructs)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/jfrog-cdk-constructs?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/jfrog-cdk-constructs?label=pypi&color=blue)

# jfrog-cdk-constructs

AWS CDK construct library that allows you to quickly start with JFrog Platform on Amazon EKS

# Sample

Try out https://github.com/anshrma/sample-jfrog-eks for the complete sample application and instructions.
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

import aws_cdk.aws_ec2
import aws_cdk.aws_eks
import aws_cdk.aws_rds
import aws_cdk.core


@jsii.data_type(
    jsii_type="jfrog-cdk-constructs.EksNodes",
    jsii_struct_bases=[],
    name_mapping={
        "instanceclass": "instanceclass",
        "instancesize": "instancesize",
        "numberofnodes": "numberofnodes",
    },
)
class EksNodes:
    def __init__(
        self,
        *,
        instanceclass: aws_cdk.aws_ec2.InstanceClass,
        instancesize: aws_cdk.aws_ec2.InstanceSize,
        numberofnodes: jsii.Number,
    ) -> None:
        '''
        :param instanceclass: 
        :param instancesize: 
        :param numberofnodes: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "instanceclass": instanceclass,
            "instancesize": instancesize,
            "numberofnodes": numberofnodes,
        }

    @builtins.property
    def instanceclass(self) -> aws_cdk.aws_ec2.InstanceClass:
        result = self._values.get("instanceclass")
        assert result is not None, "Required property 'instanceclass' is missing"
        return typing.cast(aws_cdk.aws_ec2.InstanceClass, result)

    @builtins.property
    def instancesize(self) -> aws_cdk.aws_ec2.InstanceSize:
        result = self._values.get("instancesize")
        assert result is not None, "Required property 'instancesize' is missing"
        return typing.cast(aws_cdk.aws_ec2.InstanceSize, result)

    @builtins.property
    def numberofnodes(self) -> jsii.Number:
        result = self._values.get("numberofnodes")
        assert result is not None, "Required property 'numberofnodes' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksNodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


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
        eks_non_bottle_rocket_nodes: EksNodes,
        eks_props: aws_cdk.aws_eks.ClusterProps,
        rds_props: "RdsDatabaseProps",
        create_bottle_rocket_nodes: typing.Optional[EksNodes] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param eks_non_bottle_rocket_nodes: 
        :param eks_props: 
        :param rds_props: 
        :param create_bottle_rocket_nodes: 

        :access: public
        :since: 0.1.0
        :summary: Constructs a new instance of the JFrogEks class.
        '''
        props = JFrogEksProps(
            eks_non_bottle_rocket_nodes=eks_non_bottle_rocket_nodes,
            eks_props=eks_props,
            rds_props=rds_props,
            create_bottle_rocket_nodes=create_bottle_rocket_nodes,
        )

        jsii.create(JFrogEks, self, [scope, id, props])


@jsii.data_type(
    jsii_type="jfrog-cdk-constructs.JFrogEksProps",
    jsii_struct_bases=[],
    name_mapping={
        "eks_non_bottle_rocket_nodes": "eksNonBottleRocketNodes",
        "eks_props": "eksProps",
        "rds_props": "rdsProps",
        "create_bottle_rocket_nodes": "createBottleRocketNodes",
    },
)
class JFrogEksProps:
    def __init__(
        self,
        *,
        eks_non_bottle_rocket_nodes: EksNodes,
        eks_props: aws_cdk.aws_eks.ClusterProps,
        rds_props: "RdsDatabaseProps",
        create_bottle_rocket_nodes: typing.Optional[EksNodes] = None,
    ) -> None:
        '''
        :param eks_non_bottle_rocket_nodes: 
        :param eks_props: 
        :param rds_props: 
        :param create_bottle_rocket_nodes: 

        :summary: The properties for the JFrogEks class.
        '''
        if isinstance(eks_non_bottle_rocket_nodes, dict):
            eks_non_bottle_rocket_nodes = EksNodes(**eks_non_bottle_rocket_nodes)
        if isinstance(eks_props, dict):
            eks_props = aws_cdk.aws_eks.ClusterProps(**eks_props)
        if isinstance(rds_props, dict):
            rds_props = RdsDatabaseProps(**rds_props)
        if isinstance(create_bottle_rocket_nodes, dict):
            create_bottle_rocket_nodes = EksNodes(**create_bottle_rocket_nodes)
        self._values: typing.Dict[str, typing.Any] = {
            "eks_non_bottle_rocket_nodes": eks_non_bottle_rocket_nodes,
            "eks_props": eks_props,
            "rds_props": rds_props,
        }
        if create_bottle_rocket_nodes is not None:
            self._values["create_bottle_rocket_nodes"] = create_bottle_rocket_nodes

    @builtins.property
    def eks_non_bottle_rocket_nodes(self) -> EksNodes:
        result = self._values.get("eks_non_bottle_rocket_nodes")
        assert result is not None, "Required property 'eks_non_bottle_rocket_nodes' is missing"
        return typing.cast(EksNodes, result)

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

    @builtins.property
    def create_bottle_rocket_nodes(self) -> typing.Optional[EksNodes]:
        result = self._values.get("create_bottle_rocket_nodes")
        return typing.cast(typing.Optional[EksNodes], result)

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
    "EksNodes",
    "JFrogEks",
    "JFrogEksProps",
    "RdsDatabaseProps",
]

publication.publish()

# from decimal import Decimal
# from io import BytesIO
# import json
# import os
# import requests
# import boto3
import logging
from pprint import pprint
from zipfile import ZipFile
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# from question import Question

from classes.structure_tables.Pokemons import Pokemons
from classes.structure_tables.Abilities import Abilities

logger = logging.getLogger(__name__)


class Dynamo:
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists. Otherwise, it is set by 'create_table'.
        self.table = None

    def set_table(self, table_name):
        table = self.dyn_resource.Table(table_name)
        self.table = table

    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.

        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        else:
            self.table = table
        return exists

    def create_table(
        self, table_name, key_schema, attribute_definitions, provisioned_throughput
    ):
        """
        Creates an Amazon DynamoDB table.

        :param table_name: The name of the table to create.
        :return: The newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput=provisioned_throughput,
            )
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return self.table

    def list_tables(self):
        """
        Lists the Amazon DynamoDB tables for the current account.

        :return: The list of tables.
        """
        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                print(table.name)
                tables.append(table)
        except ClientError as err:
            logger.error(
                "Couldn't list tables. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return tables

    def add_item(self, key, value, data):
        """
        Adds a movie to the table.

        :param key: Clave de la tabla
        :param value: value to add
        """
        try:
            self.table.put_item(Item={key: value, "data": data})
        except ClientError as err:
            logger.error(
                "Couldn't add item %s to table %s. Here's why: %s: %s",
                key,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def get_item(self, table_name, key, value):
        """
        Gets movie data from the table for a specific movie.

        :param table_name: Nombre de la tabla donde se guardarán los datos
        :param key: Clave de la tabla pokemon_name | ability_name
        :param value: Los Datos en json van aquí
        """
        try:
            exists = self.exists(table_name)
            if not exists:
                # 2 - Crear la tabla si no existe
                if table_name == Pokemons.TableName:
                    _class = Pokemons
                elif table_name == Abilities.TableName:
                    _class = Abilities

                self.create_table(
                    table_name,
                    _class.KeySchema,
                    _class.AttributeDefinitions,
                    _class.ProvisionedThroughput,
                )

            if self.table == None:
                self.set_table(table_name)

            response = self.table.get_item(Key={key: value})
            hasKey = "Item" in response
            if hasKey:
                item = response["Item"]
                response = {"exists": True, "data": item}
            else:
                response = {"exists": False, "data": None}
        except ClientError as err:
            print("Error aquí")

            logger.error(
                "Couldn't get item %s from table %s. Here's why: %s: %s",
                key,
                table_name,  # self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            response = {"exists": False, "data": None}
            # return response
            raise
        else:
            return response

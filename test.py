import boto3
import requests
from main import get_response
from classes.Dynamo import Dynamo
from classes.structure_tables.Pokemons import Pokemons
from classes.structure_tables.Abilities import Abilities

AWS_APPLICATION = "dynamodb"
ENDPOINT_URL = "http://localhost:8000"
REGION_NAME = "dummy"
AWS_ACCESS_KEY_ID = "dummy"
AWS_SECRET_ACCESS_KEY = "dummy"

# 1 - crear cliente
clientdb = boto3.client(
    AWS_APPLICATION,
    endpoint_url=ENDPOINT_URL,
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

resourcedb = boto3.resource(
    AWS_APPLICATION,
    endpoint_url=ENDPOINT_URL,
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

dynamo = Dynamo(resourcedb)

base_url = "https://pokeapi.co/api/v2/"


def get_item_pokemon(pokemon_name):
    pokemon_name = pokemon_name.lower()
    table_name = Pokemons.TableName
    attribute_key = Pokemons.AtttributeKey
    # consultar localmente el pokemon
    response = dynamo.get_item(table_name, attribute_key, pokemon_name)

    # si se encuentra => devolverlo, sino => registrarlo y devolverlo
    if response["exists"]:
        item = response["data"]["data"]  # sólo retornar el json original guardado
    else:
        url = f"{base_url}pokemon/{pokemon_name}"
        item = get_response(url, attribute_key, pokemon_name)

        if item["exists"]:
            # registrar el item en nuestro dynamodb si existe, si no => imprimir sólo el resultado dado
            item = item["data"]
            put_item(table_name, attribute_key, pokemon_name, item)

    return item


def get_item_ability(ability_name):
    ability_name = ability_name.lower()
    table_name = Abilities.TableName
    attribute_key = Abilities.AtttributeKey
    # consultar localmente el pokemon
    response = dynamo.get_item(table_name, attribute_key, ability_name)

    # si se encuentra => devolverlo, sino => registrarlo y devolverlo
    if response["exists"]:
        item = response["data"]["data"]  # sólo retornar el json original guardado
    else:
        url = f"{base_url}ability/{ability_name}"
        item = get_response(url, attribute_key, ability_name)

        if item["exists"]:
            # registrar el item en nuestro dynamodb si existe, si no => imprimir sólo el resultado dado
            item = item["data"]
            put_item(table_name, attribute_key, ability_name, item)

    return item


def put_item(table_name, key, value, data):
    # key = key.lower()

    table = get_table(table_name)

    # preparar el item a insertar
    input = {key: value, "data": data}

    # Insertar Datos
    table.put_item(Item=input)
    print("Successfully put item")


def get_table(tableName):
    table = resourcedb.Table(tableName)
    return table


# equivalente a un SELECT * FROM tableName de prueba
def get_all_items(tableName, tabledb, key):
    scanResponse = tabledb.scan(TableName=tableName)
    items = scanResponse["Items"]
    for item in items:
        print(item[key])


# equivalente a un SELECT * FROM tableName WHERE key = value_key de prueba
def get_item(tabledb, key, value_key):
    response = tabledb
    print(response)
    result = {"exists": True, "item": response}
    return result


# put_item_pokemon("pikachus")

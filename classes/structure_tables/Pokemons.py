class Pokemons:
    AtttributeKey = "pokemon_name"
    # -------------------------------
    TableName = "Pokemons"
    AttributeDefinitions = [{"AttributeName": AtttributeKey, "AttributeType": "S"}]
    KeySchema = [{"AttributeName": AtttributeKey, "KeyType": "HASH"}]
    ProvisionedThroughput = {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10}

class Abilities:
    AtttributeKey = "ability_name"
    # -------------------------------
    TableName = "Abilities"
    AttributeDefinitions = [{"AttributeName": AtttributeKey, "AttributeType": "S"}]
    KeySchema = [{"AttributeName": AtttributeKey, "KeyType": "HASH"}]
    ProvisionedThroughput = {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10}

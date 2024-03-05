import requests
from fastapi import (
    FastAPI,
)  # para invocar el framework FastAPI | funcionando con uvicorn, con el comando: uvicorn main:app --reload
import test  # funciones base
import uvicorn

app = FastAPI()


# creación de rutas
@app.get("/")  # registra la ruta principal con la siguiente función
def index():
    return {"message": f"Documentación y test de la API http://127.0.0.1:8001/docs"}


@app.get("/pokemon/{name}")
def get_pokemon_by_name(name):
    # Corresponde para API de LAMBDA
    response = test.get_item_pokemon(name)  # existe en nuestro dynamodb?
    return response


@app.get("/pokemon/ability/{ability}")
def get_pokemon_by_ability(ability):
    # Corresponde para API de LAMBDA
    response = test.get_item_ability(ability)  # existe en nuestro dynamodb?
    return response


@app.get("/{item}")
def get_item(item: str, name: str = None, ability: str = None):
    """
    Esta Endpoint utiliza otros endpoint como referencia para reciclar el código, sin embargo, lo que hace hasta este punto
    es poder utilizar los parámetros y valores de manera convencional, ejemplo:
    http://127.0.0.1:8001/pokemon?name=pikachu
    http://127.0.0.1:8001/pokemon?ability=static

    Adquiriendo esta estructura
    http://host:port/item?parameter=value

    :param item: palabra clave
    :param name: (parameter) nombre del pokemón
    :param ability: (parameter) cualquier habilidad pokemón
    """

    result = {"message": f"Item {item} Not found"}
    if item == "pokemon":
        if name != None:
            result = get_pokemon_by_name(name)
        elif ability != None:
            result = get_pokemon_by_ability(ability)
        else:
            result = {"message": "Param not found"}
    return result


def get_response(url, type, value_type):
    response = requests.get(url)
    if response.ok:
        payload = response.json()
        return {"exists": True, "data": payload}
    else:
        return {
            "exists": False,
            "message": f"{type.replace('_', ' ').title()} '{value_type}' Not found",
        }


# se utiliza uvicorn con debugueo
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

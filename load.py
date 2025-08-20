from pydantic import ValidationError
import json
import httpx
import tramitacao.camara.models as cm
import time

CAMARA_BASE_URL = "https://dadosabertos.camara.leg.br/api/v2/"


def get_with_pagination(url: str):
    current_url = url
    items = []
    while True:
        response = httpx.get(current_url)
        response.raise_for_status()
        data = response.json()
        items.extend(data.get("dados", []))
        links = data.get("links", [])
        for link in links:
            if link.get('rel', '') == 'next':
                current_url = link['href']
                print(current_url)
                break
        else:
            break
    return items


with open("./data/camara/proposicoes_2020_2025.json") as f:
    house_props = cm.Proposicoes.model_validate_json(f.read())

with open("checked.json", "r") as f:
    checked = set(json.load(f))

n_props = len(house_props.items)
for i, prop in enumerate(house_props.items):
    print(f"{i + 1}/{n_props}", end="\r")
    if prop.id in checked:
        continue
    max_retries = 3
    for retry in range(max_retries):
        try:
            author_data = get_with_pagination(f"{CAMARA_BASE_URL}proposicoes/{prop.id}/autores")
            break
        except Exception as e:
            print(f"\nGot exception: {e}. Retrying.")
            time.sleep(1)
    else:
        print("Max retries.")
        break
    try:
        authors = [cm.Autor.model_validate(item) for item in author_data]
    except ValidationError as e:
        print(e)
        raise
    prop.autores[:] = authors
    checked.add(prop.id)
    with open("checked.json", "w") as f:
        json.dump(list(checked), f)

    if i % 1000 == 0:
        print("\nSaving.")
        with open("./data/camara/proposicoes_2020_2025.json", "w") as f:
            f.write(house_props.model_dump_json(indent=2))

if i % 1000 == 0:
    print("\nSaving.")
    with open("./data/camara/proposicoes_2020_2025.json", "w") as f:
        f.write(house_props.model_dump_json(indent=2))
import requests

def buscar_endereco_por_cep(cep: str):
    cep = cep.replace('-', '').strip()
    if len(cep) != 8 or not cep.isdigit():
        return None

    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'erro' in data:
            return None
        return data
    except requests.RequestException:
        return None

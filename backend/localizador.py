import requests


def obter_dados_localizacao():
    """
    Identifica o país, a moeda e o idioma do utilizador
    através do endereço IP de forma automática.
    """
    try:
        # Faz uma consulta a uma API de geolocalização por IP segura
        resposta = requests.get("https://ipapi.co", timeout=5)

        if resposta.status_code == 200:
            dados = resposta.json()

            # Organiza as informações essenciais para o PreçoRoot
            informacao_local = {
                "pais_codigo": dados.get("country_code"),  # Ex: PT, BR, US
                "pais_nome": dados.get("country_name"),  # Ex: Portugal, Brazil
                "moeda": dados.get("currency"),  # Ex: EUR, BRL
                "cidade": dados.get("city")  # Ex: Lisboa, São Paulo
            }
            return informacao_local
        else:
            # Caso a API falhe temporariamente, define um padrão de segurança
            return {"pais_codigo": "PT", "pais_nome": "Portugal", "moeda": "EUR", "cidade": "Desconhecida"}

    except Exception:
        # Se o utilizador estiver offline ou der erro de rede
        return {"pais_codigo": "PT", "pais_nome": "Portugal", "moeda": "EUR", "cidade": "Desconhecida"}


# --- ÁREA DE TESTE RÁPIDO ---
if __name__ == "__main__":
    print("Testando detecção de localização do PreçoRoot...")
    print(obter_dados_localizacao())

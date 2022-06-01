# Preparar o ambiente
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ pip freeze > requirements.txt --> for new imports

# Configurações necessárias
    # No arquivo .env, é necessário adicionar o valor do Google API Key na chave GOOGLE_MAP_API_KEY

# Como rodar o data_collector via terminal
    # O comando segue o template: python <caminho_arquivo_google_api_client> <cidade> <linguagem>. Exemplo:
        $ python WebApp/data_collector/google_api_client.py Campinas pt
    # Será gerado arquivos de places e reviews no formato csv no caminho: WebApp/data_collector/datas/places e WebApp/data_collector/datas/reviews

# Referenciais:
    # https://googlemaps.github.io/libraries.html
    # https://github.com/googlemaps/google-maps-services-python
    # https://developers.google.com/maps/documentation/geocoding/requests-geocoding
    # https://googlemaps.github.io/google-maps-services-python/docs/index.html
    # https://developers.google.com/maps/documentation/places/web-service/search-find-place
    # https://developers.google.com/maps/documentation/geocoding/overview
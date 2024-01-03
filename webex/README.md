# Código de Integração com Webex

Este código é um exemplo de integração com as APIs  Webex para obter dados e interagir com os Service Apps e Integrations. Ele inclui funcionalidades para obter tokens de acesso, obter dados do xAPI e obter dados de outros endpoints da API do Webex.

## Dependências 
- requests 
- urllib3 
- xmltodict 
- logging 
- base64

## Configuração

No caso de utilizar o Webex Integration, você precisa configurar as seguintes variáveis de ambiente:
- WEBEX_INTEGRATION_CLIENT_ID: Client ID da integração com o Webex
- WEBEX_INTEGRATION_CLIENT_SECRET:  Client Secret da integração com o Webex
- WEBEX_INTEGRATION_REDIRECT_URI: URI de redirecionamento da integração com o Webex

No caso de utilizar o Webex Service Apps, você precisa configurar as seguintes variáveis de ambiente:
- WEBEX_SERVICE_ACCESS_TOKEN: token de acesso para o serviço do Webex 
- WEBEX_SERVICE_REFRESH_TOKEN: token de atualização para o serviço do Webex

### Classe webexIntegration
 Esta classe é responsável por lidar com a integração com o Webex e inclui os seguintes métodos:

#### init(client_id, client_secret, redirect_uri, code) Construtor da classe webexIntegration. 
Recebe os seguintes parâmetros: 
- client_id: Client ID da integração com o Webex 
- client_secret: Client Secret da integração com o Webex 
- redirect_uri: URI de redirecionamento da integração com o Webex 
- code: código de autorização da integração com o Webex

#### get_token() 
Obtém o Access e Refresh token da integração com o Webex.

#### refresh_token() 
Atualiza o Access e Refresh token  da integração com o Webex.

#### get_data_xapi(id, metric_name)
Obtém dados do xAPI do Webex. Recebe os seguintes parâmetros: 
- id: ID do dispositivo (ou IP)
- metric_name: nome da métrica

#### get_data(endpoint, **kwargs)
 Obtém dados de um endpoint específico da API do Webex. Recebe os seguintes parâmetros: 
 - endpoint: endpoint da API do Webex 
 - **kwargs: argumentos adicionais para a requisição

### Classe webexService
 Esta classe é responsável por lidar com o serviço do Webex e inclui os mesmos métodos da classe webexIntegration.

## Observações 
- Antes de utilizar este código, certifique-se de configurar as variáveis de ambiente corretamente. 
- Este código é um exemplo e pode ser personalizado de acordo com suas necessidades. 
- Certifique-se de ter as dependências instaladas antes de executar este código.
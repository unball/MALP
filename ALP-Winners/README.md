## Dependências
- Vá para a pasta `src/client/protobuf` e execute o `protobuf.sh`
- Volte para a raíz do projeto e execute `pip3 install -r requirements.txt`

## Execução
Para executar o sistema sem o VSSReferee rode `python3 src/main.py --port 5001`

# Docker
O sistema pode ser executado com docker. 

Para gerar a imagem docker basta fazer:

`docker build . -f Dockerfile -t alp-winners`

Para criar e rodar um container:

`docker run -it --net=host --name='alp-winners-container' alp-winners /bin/bash`

Para remover o container depois de usado:

`docker container rm alp-winners-container -f`

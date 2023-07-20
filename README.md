# MALP

MALP é o sistema da equipe utilizado na LARC 2022 que realiza a integração entre o ALP-Winners (sistema utilizado na LARC 2021 remota) e MainSystem (sistema utilizado na LARC 2019 presencial). O MainSystem fornece a interface gráfica para configuração dos paramêtros da visão e o ALP-Winners, a estratégia, controle e comunicação.

A visão do MainSystem se comunica com o ALP-Winners utilizando sockets. ALP-GUI é uma interface criada para auxiliar no desenvolvimento do ALP-Winners, para executar o MALP não é necessário executar ALP-GUI.

## Como executar MALP

1. Instale as dependências necessárias para os dois sistemas utilizando o pip na pasta raiz
```
pip install -r requirements.txt
```

2. Digital no termianl 

`./run.sh`

Isso irá executar o sistema com a configuração padrão de porta `5001`. Caso haja algum problema com essa porta, é possível executar o MALP com o comando

`./run.sh 5002`

Ou com qualquer outra porta que desejar. 

> ### Importante!!
>
> - A interface gráfica do MainSystem não é finalizada quando o bash run.sh é finalizado no terminal
> - Caso queira fazer debug usando prints, é recomendado colocar no print o nome do sistema proveniente ou executar os sistemas manualmente em terminais separados
> - Caso queira usar outros argumentos antes de executar, basta alterar o arquivo run.sh na linha 10

## Comunicação MALP com robô

A comunicação do MALP com o robô é feita por meio de sinal de rádio nrf24l01.

Para isso, conectamos um módulo ESP32 + rádio nrf24l01. O firmware para a ESP32 pode ser encontrado neste repositório: [Communication](https://github.com/unball/communication). As informações do MALP são enviadas por sinal serial a esse conjunto ESP32 + radio nrf24l01.

As informações enviadas pelo ESP32 + radio nrf24l01 são recebidas por um nrf24l01 presente no robô. O firmware responsável por esse rádio pode ser encontrado no repositório [Firmware](https://github.com/unball/Firmware).


> ### Atenção!
>
> Erros na comunicação são comuns. Segue uma lista de problemas e possíveis soluções:
>
> - O robô está ligado, esperando pela comunicação com o conjunto ESP32 + nrf24l01, fazendo movimentação senoidal (apenas andando para frente e para trás). O conjunto está conectado no computador e está ligado mas nada muda. Nesse caso, basta desconectar o cabo USB da ESP32 e conectar novamente. Se o rádio da ESP32 conseguir efetivar a comunicação, o movimento senoidal é interrompido e nesse caso, a comunicação está acontecendo de fato.
> - Pode acontecer da porta serial não ser autorizada pelo computador. Para resolver esse problema, basta digitar no terminal o comando abaixo. P.S.: ```ttyUSB0``` é a porta por onde o rádio tenta conectar com o computador.
>
> ```
> sudo chmod a+rw /dev/ttyUSB0
> ```

## Configuração da camera

No Linux, a camera pode ser configurada usando uma interface gráfica do v4l, ```camset```, disponibilizada nesse [repositório do Github](https://github.com/azeam/camset). Basta seguir as instruções do repositório para conseguir usar. Lembrar de configurar o PATH caso queira usar o comando ```camset```.
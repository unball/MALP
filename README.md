# MALP

MALP é o sistema da equipe utilizado na LARC 2022 que realiza a integração entre o ALP-Winners (sistema utilizado na LARC 2021 remota) e MainSystem (sistema utilizado na LARC 2019 presencial). O MainSystem fornece a interface gráfica para configuração dos paramêtros da visão e o ALP-Winners, a estratégia, controle e comunicação.

A visão do MainSystem se comunica com o ALP-Winners utilizando sockets. O ALP-GUI é uma interface criada para auxiliar no desenvolvimento do ALP-Winners, para executar o MALP não é necessário executar ALP-GUI.

# Como executar MALP

1.  **Depois de instalar os requisitos do sistema ALP-Winners no seu diretório**, executar no terminal, dentro do MainSystem:

        ./main.py --port 5001 --n_robots 3

2.  **Depois de instalar os requisitos do sistema ALP-Winners no seu diretório**, executar no terminal, dentro do ALP-Winners:

        python3 src/main.py --team-color blue --team-side left --immediate-start --port 5001 --n_robots 3

> ### Importante!!
>
> - Executar os comandos do MainSystem antes de executar os do ALP-Winners para estabelecer a comunicação entre os sistemas
> - Observar se a porta 5001 está sendo utilizada por outra aplicação. Caso esteja em uso, basta trocar para 5002, 5003, e assim por diante. O conflito dessas portas costuma ocorrer quando houve algum erro no MALP

## Comunicação MALP com robô

A comunicação do MALP com o robô é feita por meio de sinal de rádio nrf24l01.

Para isso, conectamos um módulo ESP32 + rádio nrf24l01. O firmware para a ESP32 pode ser encontrado neste repositório: [Communication](https://github.com/unball/communication). As informações do MALP são enviadas por sinal serial a esse conjunto ESP32 + radio nrf24l01.

As informações enviadas pelo ESP32 + radio nrf24l01 são recebidas por um nrf24l01 presente no robô. O firmware responsável por esse rádio pode ser encontrado no repositório [Firmware](https://github.com/unball/Firmware).

> ### Atenção!
>
> Erros na comunicação são comuns. Segue o mais frequente e como lidar nessa situação:
>
> - O robô está ligado, esperando pela comunicação com o conjunto ESP32 + nrf24l01, fazendo movimentação senoidal (apenas andando para frente e para trás). O conjunto está conectado no computador e está ligado mas nada muda. Nesse caso, basta desconectar o cabo USB da ESP32 e conectar novamente. Se o rádio da ESP32 conseguir efetivar a comunicação, o movimento senoidal é interrompido e nesse caso, a comunicação está acontecendo de fato.

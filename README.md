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

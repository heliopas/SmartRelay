# SmartRelay
Python script that can read values from meters WT210 and HP34401A. This script can also control relay box.

Tabela de conteúdos
=================
<!--ts-->
   * [Sobre](#Sobre)
   * [Funções disponíveis](#Features)

<!--te-->

## Sobre
Programa para controle de acionamento de relés e leitura de multimetros modelos:
*WT210 e HP34401A

## Funções disponíveis
- [x] Open serial port
- [x] Send and receive data from multimeter
- [x] Disable beep HP34401A
- [x] Relay box control

## Features

- 27/11/2024 - Commit manuais operação
- 27/11/2024 - Adicionado camada de conexão com banco de dados oracle alterado código main
- 28/11/2024 - Adicionado query de consulta BD por LanI
- 06/12/2024 - Adicionado controle on/off por recebimento de ultimo pacote via CC
- 20/12/2024 - Alterado a logica para gerar outage somente após todas CPUS enviarem algum pacote no CC
- 06/01/2025 - Corrigido lógica que verifica recebimento dos pacotes enviados pela CPU
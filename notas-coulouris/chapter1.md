# Characterization of Distributed Systems

## Introduction

o livro objetiva explicar as características de computadores ligados a rede, que impactam os desenvolvedores de sistemas, e também para apresentar conceitos que foram criada para auxiliar na criação de sistemas baseados na rede

>**what is a distributed system?** hardware and software components located at networked computers coordinate their actions **only** by passing messages

esta definição, que independe da localidade dos dispositivos, implica nas seguitnes consequências:

- concorrencia (compartilhamento de recursos)

- sem relógio global (programas precisam cooperar na ordenação das ações, a qual depende da ideia de tempo, porem não há um relógio global para todos dispositivos)

- falhas independentes (já existem falhas individuais, imagina com varias dispositivos conectados, dependendo um do outro para executar programas - pode ocorrer problemas de hardware, de rede e de SO... muita coisa pode dar errado)

## Examples of distributed systems
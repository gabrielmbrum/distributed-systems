# Biased Local SGD para Classificação de Imagens Médicas em Sistemas com GPUs Heterogêneas

> Rascunho de proposta de tema — Disciplina de Sistemas Distribuídos (Pós-Graduação)
> Status: **em investigação** — escopo final a definir conforme viabilidade experimental

## Contexto e motivação

Métodos clássicos de treinamento distribuído (data-parallel SGD síncrono) assumem que todos os workers têm capacidade computacional semelhante. Na prática, é comum ter acesso a hardware heterogêneo — GPUs de gerações e capacidades diferentes — e essa suposição de homogeneidade gera **overhead de sincronização**: workers rápidos ficam ociosos esperando os mais lentos em cada etapa de agregação.

O ponto de partida deste trabalho é o framework de **Local SGD enviesado (biased local SGD)** proposto por Lim et al. (2025) [[1]](#referências), que ataca esse problema por dois mecanismos:

1. **Local SGD desbalanceado** — cada worker realiza um número de updates locais proporcional à sua velocidade (`τ_F` para o rápido, `τ_S = γ·τ_F` para o lento, onde `γ` é a razão de desempenho medida empiricamente), eliminando o tempo de bloqueio.
2. **Bias controlado** para compensar a perda de convergência causada pelo desbalanceamento:
   - **Amostragem de dados enviesada por loss (loss-based top-k sampling)**: workers rápidos recebem preferencialmente amostras de maior loss.
   - **Agregação de modelo ponderada**: o modelo global dá mais peso às atualizações de workers que fizeram mais passos locais.

O paper original valida a proposta em benchmarks de visão computacional genéricos (CIFAR-10/100, Oxford Flowers102, Tiny ImageNet) e NLP (AG News), em cenários **CPU (lento) vs. GPU (rápido)**, com gaps de desempenho (`γ`) que chegam a ~22x.

## Proposta de investigação

A ideia central é **investigar a aplicabilidade e o comportamento desse framework no contexto de classificação de imagens médicas**, sob duas mudanças de cenário em relação ao paper original que ainda preciso avaliar com mais profundidade:

- **Heterogeneidade GPU–GPU (não CPU–GPU)**: minha infraestrutura disponível são 3 GPUs — 2 "fortes" e 1 "fraca" — com um gap de desempenho (`γ`) provavelmente bem menor do que o cenário CPU/GPU do paper original. Isso muda o regime de operação do método e é um ponto em aberto a ser medido empiricamente antes de qualquer decisão de escopo.
- **Domínio médico**: datasets de imagens médicas costumam ter características distintas de benchmarks genéricos — maior desbalanceamento de classes, imagens menores (dependendo do dataset), e maior sensibilidade a ruído/outliers. Isso levanta a pergunta de como a amostragem enviesada por loss-alto se comporta nesse contexto (pode ajudar a focar em casos difíceis/classes raras, ou pode acabar enviesando o modelo para outliers/ruído de anotação).

**Este ainda é um recorte amplo.** A pergunta de pesquisa final, o(s) dataset(s) definitivo(s) e o desenho experimental completo dependem de uma fase inicial de investigação (medir `γ` real da minha infraestrutura, rodar uma implementação de referência, avaliar tempo disponível).

## Cenário de infraestrutura

- 3 GPUs disponíveis: 2 "fortes" (similares entre si) + 1 "fraca".
- Cenário preferencial de experimentação: usar apenas as **2 GPUs fortes** como caso principal (heterogeneidade leve/moderada entre elas, se houver, ou como baseline homogêneo).
- A GPU fraca fica como **extensão possível**, caso o tempo permita explorar um cenário de heterogeneidade mais acentuada (2 fortes + 1 fraca), análogo ao "weak scaling" avaliado no paper original.
- Ainda não decidido: framework de comunicação entre processos (o paper original usa `mpi4py`; PyTorch DDP/`torch.distributed` também é uma opção mais direta a avaliar).

## Possíveis datasets (em aberto)

Candidatos naturais, por já fazerem parte da minha linha de pesquisa atual (fine-tuning e augmentation para classificação de imagens médicas):

- **MedMNIST** (PathMNIST, DermaMNIST, BloodMNIST, entre outros) — vantagem de já ter familiaridade com o benchmark, imagens pequenas (treino mais rápido, permite mais rodadas experimentais), e desbalanceamento de classes presente em alguns subsets.
- Outros datasets de imagens médicas de maior resolução (a definir) — caso se mostre relevante avaliar o método sob um regime computacional mais pesado (mais próximo do cenário Oxford Flowers102 do paper original).

A escolha final depende do tempo disponível e da capacidade das GPUs de rodar múltiplas configurações experimentais em prazo viável.

## Possíveis métricas a investigar

- **Acurácia / F1-score (macro, dado o desbalanceamento de classes)** ao final do treinamento, comparando: SGD síncrono, Local SGD balanceado, Local SGD desbalanceado sem bias, Local SGD desbalanceado com bias (proposto).
- **Tempo de parede (wall-clock time)** até convergência, para o mesmo orçamento de épocas.
- **Tempo de bloqueio/sincronização** por etapa, como no Figure 1 do paper original (breakdown de I/O, feedforward, backprop, agregação, bloqueio).
- **Curvas de convergência** (acurácia de validação x tempo), não apenas acurácia final.
- Possivelmente: métricas por classe, para avaliar se o bias por loss-alto beneficia ou prejudica classes minoritárias/raras — ponto específico do contexto médico que o paper original não avalia.

Essa lista não é definitiva; conforme os experimentos preliminares, algumas métricas podem ser descartadas ou outras adicionadas (ex. calibração do modelo, se fizer sentido para o recorte médico).

## Perguntas em aberto / próximos passos

- [ ] Medir `γ` (razão de desempenho) real entre as GPUs disponíveis, em pelo menos um modelo/dataset candidato.
- [ ] Rodar uma implementação de referência do Local SGD balanceado vs. síncrono como baseline, para validar viabilidade de tempo/infra.
- [ ] Definir se o framework de comunicação será `mpi4py` (como no paper original) ou `torch.distributed`/DDP.
- [ ] Decidir dataset(s) definitivo(s) e escopo (2 GPUs fortes apenas vs. incluir a GPU fraca).
- [ ] Levantamento mais aprofundado de trabalhos relacionados em federated/distributed learning para classificação de imagens médicas, para situar a contribuição.

## Referências

[1] Lim, J., Jo, J., Ko, C., Go, Y. M., Hwa, J., & Lee, S. (2025). *Biased Local SGD for Efficient Deep Learning on Heterogeneous Systems*. arXiv:2508.08540.
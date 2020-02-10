# [Data Engineer Code Challenge](https://grupozap.github.io/squad-data-platform/data-engineer-test)

[![Tests](https://github.com/Coqueiro/session-calc-spark/workflows/Run%20tests/badge.svg)](https://github.com/Coqueiro/session-calc-spark/workflows/Run%20tests/badge.svg)
[![codecov](https://codecov.io/gh/Coqueiro/session-calc-spark/branch/master/graph/badge.svg?token=L3VbWQEfb4)](https://codecov.io/gh/Coqueiro/session-calc-spark)
[![Release](https://github.com/Coqueiro/session-calc-spark/workflows/Release/badge.svg)](https://github.com/Coqueiro/session-calc-spark/workflows/Release/badge.svg)

*TL;DR:* Rodar na raiz do projeto:
```bash
make pull_app
make pull_docker_spark
GROUP_KEY={chave_de_grupamento} make -k session_calc # [browser_family, os_family, device_family]
```

Os arquivos de resultado são gravados no endereço local `./session-calc/output`.


# Contagem de sessões de usuários agrupadas por chave


Este *job* tem o objetivo realizar a contagem de sessões de usuários agrupadas por chave, utilizando um *job* em `pyspark` para extrair os dados de um bucket público da S3 e criar um `.json` em disco com os agrupamentos por chave pivotados.

Exemplo de dados na S3:
```json
{"anonymous_id":"84CC8775-0E38-4787-A4FF-DD66CCFCF956","device_sent_timestamp":1554767994401,"browser_family":"Other","os_family":"Other","device_family":"Other"}
{"anonymous_id":"84CC8775-0E38-4787-A4FF-DD66CCFCF956","device_sent_timestamp":1554767994740,"name":"Property Full Screen Gallery","browser_family":"Other","os_family":"Other","device_family":"Other"}
{"anonymous_id":"569D7BC4-1C63-45C1-A1B6-59818D5B8C9D","device_sent_timestamp":1554767981430,"browser_family":"Other","os_family":"Other","device_family":"Other"}
```

Exemplo de saída de dados:
```json
{"iPhone":42,"Generic Smartphone":12,"Samsung SM-J120H":7,"Samsung SM-J500M":4}
```

Este projeto se utiliza de código presente nos seguintes repositórios:
- https://github.com/big-data-europe/docker-spark


## *Setup*
- O projeto foi desenvolvido em ambiente UNIX e, portanto, não é garantido seu funcionamento em outros sistemas operacionais como Windows.

- Para rodar o *job* localmente é necessário ter uma instalação de [docker](https://www.redhat.com/pt-br/topics/containers/what-is-docker) e [docker-compose](https://www.mundodocker.com.br/docker-compose/). Segue um [guia de instalação do Docker para o Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/como-instalar-e-usar-o-docker-no-ubuntu-18-04-pt) e de [docker-compose](https://www.mundodocker.com.br/docker-compose/).

- O projeto também diversos comandos do tipo [`make`](https://pt.wikipedia.org/wiki/Make) para facilitar a parametrização. Segue [*thread* com instruções](https://askubuntu.com/questions/161104/how-do-i-install-make).

- Para rodar localmente, é necessário fazer um *pull* das imagens docker utilizadas. Para fazer isso, rode os seguintes comandos na raiz do projeto:
```bash
make pull_app
make pull_docker_spark
```

- Alternativamente, as imagens podem ser *buildadas* localmente utilizando os seguintes comandos na raiz do projeto:
```bash
make build_app
make build_docker_spark
```


## Rodar o *job* localmente
- É necessário escolher qual a chave que será utilizada para o agrupamento dentre as seguintes opções (de acordo com o desafio):

    - `browser_family` (Família do *Browser* usado pelo usuário)
    - `os_family` (Família do Sistema Operacional usado pelo usuário)
    - `device_family` (Família do Dispositivo usado pelo usuário)

- Uma vez escolhida a chave de agrupamento, a mesma pode ser passada pela variável de ambiente `GROUP_KEY`, e em seguida deve-se chamar o comando `make -k session_calc`, como, por exemplo:
```bash
GROUP_KEY=os_family make -k session_calc
```

- Existem algumas opções de parâmetros que o *job* também aceita como variável de ambiente, cujos valores padrões são os determinados pelo desafio. Segue lista das variáveis de execução, seus valores padrões e suas descrições:

|Parâmetro|Valor Padrão|Descrição|
|---|---|---|
|`READ_PATH`|`s3a://grupozap-data-engineer-test/`|Endereço de leitura dos arquivos de eventos. Pode ser um endereço na S3 ou local do *container* (é necessário adicionar como volume).|
|`WRITE_PATH`|`session-calc/output`|Endereço local de escrita do resultado do agrupamento. O endereço padrão já está volumado no *container*, portanto os resultados já serão expostos fora do mesmo. Um endereço alternativo pode exigir uma adição de volume durante a execução.|
|`USER_KEY`|`anonymous_id`|A chave única de referência do usuário. Ela é usada para identificar um usuário único. No momento a aplicação só dá suporte para um valor de chave.|
|`TIMESTAMP_KEY`|`device_sent_timestamp`|A chave de referência de quando o evento foi realizado. Ela é usada para identificar as janelas de sessões do usuário.|
|`MAX_SESSION_SECONDS`|`1800`|Tempo máximo de uma sessão, por usuário. Essa chave está com o padrão de 30 minutos.|
|`GROUP_KEY`|`device_family`|Chave de agrupamento para contagem de sessões.|

- Ao final da execução da aplicação, os resultados estarão disponíveis dentro do endereço local `WRITE_PATH`, em arquivos .json de acordo com a opção de chave de agrupamento, no padrão `session_by_{GROUP_KEY}.json`. Exemplo de arquivo: `sessions_by_device_family.json`.


## Rodar os testes
- Para rodar os testes unitários da aplicação é necessário utilizar o comando: `make test_app`, que irá validar as funções auxiliares utilizadas pela aplicação assim como a própria aplicação. Este comando utiliza uma [imagem simples com pyspark](https://github.com/Coqueiro/docker-pyspark) para realizar os testes localmente.

- A versão atual não possui testes de integração.


## Fazendo *release* das imagens
- Para atualizar a imagem da aplicação e torná-la disponível através do repositório de imagens [Docker Hub](https://hub.docker.com/) é necessário realizar o comando `make release_app` para a aplicação ou `make release_docker_spark` para as imagens do cluster de Spark em Docker. Atualizações no projeto devem ser seguidas de bumps de versão nas imagens para manter a consistência do projeto.

- Os seguintes parâmetros podem ser utilizados para alterar o *build* da imagem. É recomendado que essas mudanças sejam feitas com cautela por alterarem componentes estruturais da solução:

|Parâmetro|Valor Padrão|Descrição|
|---|---|---|
|`HUB_PUBLISHER`|`coqueirotree`|Usuários dos repositórios no Docker Hub.|
|`HUB_PASSWORD`|`$(shell cat .hub_password)`|*Token* de acesso do Docker Hub.|
|`SPARK_VERSION`|`2.4.4`|Versão de Spark utilizada pelas imagens.|
|`HADOOP_VERSION`|`3.1.2`|Versão de Hadoop utilizada pelas imagens.|
|`BUMP_LEVEL`|`patch`|Nível de bump na versão da imagem, utilizado em novos *releases*. As opções são `patch`, `minor` e `major`. Para rodar este comando é necessário ter uma instalação de `python` local com o gerenciador de pacotes `pip`.|

- O arquivo `.hub_password` precisa ser criado e colocado dentro da pasta raiz do projeto. Ele deve conter o *token* de acesso para o repositório de imagens Docker para que seja possível realizar comandos de `push` de imagens.


## Análise exploratória de dados:

O objetivo desta análise é entender melhor o *dataset* de entrada, e adaptar a solução de acordo com os dados disponíveis. Para rodar a análise exploratória, basta rodar o comando `make -k eda`.

### Descobertas relevantes:

- Não existem campos com valores nulos dentro da amostra. Confiando que este padrão é significante, não iremos adicionar etapas de filtros de dados vazios a fim de otimizar a execução da aplicação.

- Um mesmo `anonymous_id` pode ter mais de um `browser_family`, `device_family` ou `os_family` diferentes, com **393** ocorrências na amostragem. Isto é significante pois significa que uma sessão pode percorrer agrupamentos diferentes, e poderia ser, portanto, contada em mais de um agrupamento. Levando em consideração que regra de sessionamento inclui que a abertura da sessão acontece para o primeiro evento de um usuário, e que a taxa de ocorrência desses casos é muito pequena, iremos desconsiderar mudanças de `browser_family`, `device_family` ou `os_family` durante a sessão.


## TODO

- Action CI
- Medidor de Linting

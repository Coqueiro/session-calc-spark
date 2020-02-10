# WIP

Calcular o tempo de sessão de usuários utilizando um cluster de Spark em Docker

## Setup
O arquivo `.hub_password` precisa ser criado e colocado dentro da pasta raíz do projeto. Ele deve conter o token de acesso para o repositório de imagens Docker para que seja possível realizar comandos de `push` e `pull` de imagens.

Análise exploratória de dados:
- Não existem campos com valores nulos dentro da amostra. Confiando que este padrão é significante, não iremos adicionar etapas de tratamento de dados a fim de otimizar a execução da aplicação.

```python
    df.select([f.count(f.when(f.isnan(c), c)).alias(c) for c in df.columns]).show()
```

- Um mesmo `anonymous_id` pode ter mais de um `browser_family`, `device_family` e `os_family` diferentes?

```python
    df.groupBy("anonymous_id").agg(
        f.countDistinct("browser_family").alias("browser_family_uniques"),
        f.countDistinct("device_family").alias("device_family_uniques"),
        f.countDistinct("os_family").alias("os_family_uniques")
    )
```

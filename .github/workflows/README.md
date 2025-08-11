# 🔄 Workflow de Atualização Automática do README

Este workflow atualiza automaticamente o README.md com informações dos seus projetos e commits do GitHub.

## ⏰ **Agendamento**

- **Execução automática**: Diariamente às 6h UTC (3h BR)
- **Execução manual**: Disponível através do botão "Run workflow"
- **Execução por push**: Sempre que houver push na branch principal

## 🚀 **Como Funciona**

1. **Checkout**: Baixa o código do repositório
2. **Setup Python**: Configura Python 3.11
3. **Dependências**: Instala as bibliotecas necessárias
4. **Atualização**: Executa o script Python para atualizar o README
5. **Verificação**: Detecta se houve mudanças
6. **Commit**: Faz commit automático das mudanças (se houver)
7. **Push**: Envia as mudanças para o repositório

## ⚙️ **Configuração**

### Variáveis de Ambiente

O workflow usa automaticamente:

- `GITHUB_TOKEN`: Token de acesso do GitHub (configurado automaticamente)
- `GITHUB_USERNAME`: Username do proprietário do repositório
- `GITHUB_REPOSITORY`: Nome completo do repositório

### Secrets Necessários

Nenhum secret adicional é necessário. O `GITHUB_TOKEN` é fornecido automaticamente pelo GitHub Actions.

## 📊 **O que é Atualizado**

### Tabela de Projetos

- Nome do projeto
- Tecnologia principal
- Número de stars
- Link direto

### Tabela de Commits

- Hash curto do commit
- Título do commit como link

## 🔧 **Personalização**

### Alterar Frequência

Edite a linha `cron` no workflow:

```yaml
schedule:
  - cron: "0 6 * * *"  # Diariamente às 6h UTC
  - cron: "0 */6 * * *"  # A cada 6 horas
  - cron: "0 9,18 * * *"  # Duas vezes por dia (9h e 18h UTC)
```

### Adicionar Triggers

```yaml
on:
  schedule:
    - cron: "0 6 * * *"
  workflow_dispatch:  # Execução manual
  push:
    branches: [ main, master, develop ]  # Mais branches
  pull_request:
    branches: [ main ]  # Em PRs
```

## 📝 **Logs e Debug**

### Ver Logs de Execução

1. Vá para a aba "Actions" do seu repositório
2. Clique no workflow "Atualizar README"
3. Clique na execução mais recente
4. Veja os logs de cada step

### Executar Manualmente

1. Vá para a aba "Actions"
2. Clique em "Atualizar README"
3. Clique em "Run workflow"
4. Selecione a branch e clique em "Run workflow"

## 🐛 **Solução de Problemas**

### Erro: "Permission denied"

- Verifique se o workflow tem permissão para fazer push
- O `GITHUB_TOKEN` deve ter permissões de escrita

### Erro: "Python not found"

- O workflow usa Python 3.11, que é suportado pelo Ubuntu latest

### Erro: "Dependencies not found"

- O workflow instala automaticamente as dependências do `requirements.txt`

### README não é atualizado

- Verifique se os marcadores `<!--PROJECTS-->` e `<!--COMMITS-->` estão no README.md
- Verifique os logs do workflow para erros

## 📈 **Monitoramento**

### Métricas de Sucesso

- ✅ Workflow executado com sucesso
- ✅ README atualizado
- ✅ Mudanças commitadas e enviadas

### Alertas

- ❌ Falha na execução
- ❌ Erro ao fazer commit
- ❌ Erro ao fazer push

## 🔄 **Integração com Outros Workflows**

Este workflow pode ser integrado com outros workflows:

```yaml
# Em outro workflow
needs: update-readme  # Aguarda este workflow terminar
```

## 📚 **Recursos Adicionais**

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Syntax](https://crontab.guru/)
- [Python Setup Action](https://github.com/actions/setup-python)

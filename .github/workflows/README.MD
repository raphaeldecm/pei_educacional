# 🚀 Deploy Automático - Sistema PEI

## 📋 Visão Geral

O sistema possui deploy automático via **GitHub Actions** para dois ambientes que rodam no mesmo servidor físico através de um túnel SSH.

### 🏗️ Arquitetura

```
GitHub Actions → Túnel SSH (Zaira) → Servidor de Aplicação (Puri)
                     ↓
    ┌─────────────────────────────────────────────┐
    │           Servidor Puri (10.21.0.125)      │
    │                                             │
    │  📁 /opt/sistema_pei_hmg (Homologação)     │
    │      ├── docker-compose.hmg.yml            │
    │      ├── .envs/.hmg/.django                │
    │      └── Porta: 8080                       │
    │                                             │
    │  📁 /opt/sistema_pei (Produção)            │
    │      ├── docker-compose.prod.yml           │
    │      ├── .envs/.prod/.django               │
    │      └── Porta: 8081                       │
    └─────────────────────────────────────────────┘
```

## 🔧 Configuração

### Secrets (GitHub Repository → Settings → Secrets and variables → Actions)

| Secret | Valor | Descrição |
|--------|--------|-----------|
| `SSH_PRIVATE_KEY_HMG` | Chave privada do servidor Puri | Chave RSA do arquivo `~/.ssh/id_rsa` do servidor Puri |
| `KNOWN_HOSTS_HMG` | Known hosts dos servidores | Fingerprints SSH do Zaira e Puri |

**Valor do KNOWN_HOSTS_HMG:**
```
[zaira.ifrn.edu.br]:65222 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFdlBDMQ1yvJLm1fs+MDqr0t75cXtmMOjmfI/lPFklNS
10.21.0.125 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDPNGl+TtEo9zicm1qyLz5ZwK6wUSyFXRcJuzJ2714y/
```

### Variables (GitHub Repository → Settings → Secrets and variables → Actions → Variables)

| Variable | Valor | Descrição |
|----------|--------|-----------|
| `SSH_PORT_HMG` | `65222` | Porta do servidor túnel (Zaira) |
| `SSH_USER_HMG` | `pei` | Usuário do servidor túnel (Zaira) |
| `SSH_HOST_HMG` | `zaira.ifrn.edu.br` | Hostname do servidor túnel |

## 🌍 Ambientes

### 🧪 Homologação (Staging)

- **Branch:** `staging`
- **Workflow:** `.github/workflows/deploy-staging.yml`
- **Diretório:** `/opt/sistema_pei_hmg`
- **Docker Compose:** `docker-compose.hmg.yml`
- **Configurações:** `.envs/.hmg/.django`
- **Porta:** `8080`
- **URL:** https://pei-hmg.ifrn.edu.br/
- **Trigger:** Push para branch `staging`

### 🚀 Produção (Production)

- **Branch:** `main`
- **Workflow:** `.github/workflows/deploy-production.yml`
- **Diretório:** `/opt/sistema_pei`
- **Docker Compose:** `docker-compose.prod.yml`
- **Configurações:** `.envs/.prod/.django`
- **Porta:** `8081`
- **URL:** https://pei.ifrn.edu.br/
- **Trigger:** Push para branch `main`

## 🔄 Processo de Deploy

### 1. **Trigger**
- **Homologação:** Push para `staging`
- **Produção:** Push para `main`

### 2. **Conexão SSH**
```bash
GitHub Actions → SSH Túnel (pei@zaira.ifrn.edu.br:65222) → Servidor (raphael@10.21.0.125:22)
```

### 3. **Etapas do Deploy**

1. **📥 Checkout do código**
2. **🔐 Configuração SSH** (chave + known_hosts + túnel)
3. **📥 Atualização do código** (git pull)
4. **🔧 Verificação de configurações**
5. **🛑 Parada dos containers** existentes
6. **🧹 Limpeza de recursos Docker** (para liberar espaço)
7. **🔨 Build das imagens** Docker
8. **🚀 Inicialização dos containers**
9. **🏥 Health check** da aplicação
10. **✅ Verificação final**

### 4. **Limpeza Automática**

Para evitar problemas de espaço em disco:
```bash
docker system prune -af --volumes
docker builder prune -af
docker image prune -af
```

## 🚨 Troubleshooting

### Problema de Espaço em Disco
```bash
# Conectar ao servidor
ssh -J pei@zaira.ifrn.edu.br:65222 raphael@10.21.0.125

# Verificar espaço
df -h

# Limpeza manual
docker system prune -af --volumes
docker builder prune -af
```

### Problema de Conexão SSH
1. Verificar se as variáveis estão configuradas
2. Verificar se a chave privada está correta
3. Verificar se o known_hosts está atualizado

### Containers não Iniciam
```bash
# Ver logs dos containers
docker compose -f docker-compose.hmg.yml logs
docker compose -f docker-compose.prod.yml logs

# Verificar status
docker compose -f docker-compose.hmg.yml ps
docker compose -f docker-compose.prod.yml ps
```

## 📊 Monitoramento

### Health Checks
- **Homologação:** `curl -H "Host: pei-hmg.ifrn.edu.br" http://10.21.0.125:8080`
- **Produção:** `curl -H "Host: pei.ifrn.edu.br" http://10.21.0.125:8081`

### Logs do Deploy
- GitHub Actions → Repositório → Actions → Workflow específico

## 🛡️ Segurança

- ✅ Chaves SSH privadas armazenadas como secrets
- ✅ Conexão através de túnel SSH seguro
- ✅ Verificação de known_hosts
- ✅ Configurações de ambiente separadas por ambiente
- ✅ Deploy apenas em branches específicas (`staging` e `main`)

## 🎯 Workflow de Desenvolvimento

```mermaid
graph LR
    A[Desenvolvimento] --> B[Push para staging]
    B --> C[Deploy Automático HMG]
    C --> D[Testes em Homologação]
    D --> E[Merge para main]
    E --> F[Deploy Automático PROD]
    F --> G[Aplicação em Produção]
```

## 📞 Suporte

Em caso de problemas com o deploy:
1. Verificar logs no GitHub Actions
2. Conectar ao servidor e verificar status dos containers
3. Verificar espaço em disco
4. Verificar configurações de ambiente

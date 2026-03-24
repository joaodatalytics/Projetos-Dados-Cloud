# 🖥️ Projeto 01 — Arquitetura de Rede Segura e Troubleshooting com Amazon VPC

![AWS](https://img.shields.io/badge/Amazon_VPC-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![EC2](https://img.shields.io/badge/Amazon_EC2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white)
![Linux](https://img.shields.io/badge/Terminal_CLI-4D4D4D?style=for-the-badge&logo=linux&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-1A9C3E?style=for-the-badge)

---

## 🎯 Objetivo

Construir do zero a infraestrutura de rede base para um ambiente corporativo (*Security by Design*), utilizando **Amazon VPC**. O foco principal foi garantir o isolamento de recursos sensíveis (como bancos de dados analíticos) em sub-redes privadas, configurando o roteamento correto para acesso externo seguro e executando o *troubleshooting* em uma falha de conectividade.

---

## 🛠️ Serviços utilizados

| Serviço | Função |
|---|---|
| **Amazon VPC** | Nuvem privada virtual para isolamento lógico da rede (`10.0.0.0/16`). |
| **Subnets** | Segmentação do tráfego em redes Públicas e Privadas. |
| **Route Tables & IGW** | Tabelas de Rotas e Internet Gateway para direcionar o fluxo de tráfego. |
| **NAT Gateway** | Permite que instâncias privadas acessem a internet (para atualizações) sem serem expostas. |
| **Amazon EC2 (Bastion Host)** | *Jump Box* segura na rede pública para acessar instâncias privadas via SSH. |

---

## 🏗️ Arquitetura da solução

```text
       Internet
          │
          ▼
[ Internet Gateway (IGW) ]
          │
┌─────────▼─────────────────────────────────────────────────┐
│                 Joao VPC (10.0.0.0/16)                    │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Sub-rede Pública (Joao-RTPublic)                    │  │
│  │                                                     │  │
│  │   [ Bastion Host (EC2) ]      [ NAT Gateway ]       │  │
│  └───────────┬──────────────────────────┬──────────────┘  │
│              │ (SSH)                    │ (Tráfego Out)   │
│  ┌───────────▼──────────────────────────▼──────────────┐  │
│  │ Sub-rede Privada (Joao-RTPrivate)                   │  │
│  │                                                     │  │
│  │   [ Instância Privada / Banco de Dados ]            │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

📋 Etapas de implementação
Criação da Joao VPC com o bloco CIDR 10.0.0.0/16.

Segmentação lógica criando uma Sub-rede Pública e uma Sub-rede Privada.

Criação e anexo do Internet Gateway (IGW) à VPC.

Configuração da Tabela de Rotas Pública (Joao-RTPublic), direcionando o tráfego externo para o IGW.

Provisionamento de um NAT Gateway na sub-rede pública para gerenciar a saída segura de dados.

Lançamento do servidor Bastion Host (Amazon Linux) na sub-rede pública para acesso SSH.

Teste de conectividade e validação do fluxo de dados da instância privada para a internet.

🔍 Diagnóstico e Troubleshooting
Durante a etapa de validação, ao acessar a instância privada e realizar um teste de conectividade externa (ping amazon.com), deparei-me com uma falha crítica de roteamento: 100% packet loss.

Em vez de recriar a infraestrutura, iniciei a investigação da arquitetura:

Validei se a instância privada estava ligada e o Security Group permitia tráfego ICMP. (Status: OK)

Validei se o NAT Gateway estava ativo na rede pública. (Status: OK)

Causa Raiz: Ao auditar o painel de Tabelas de Rotas, identifiquei que a tabela Joao-RTPrivate não possuía uma associação explícita com a sub-rede privada, deixando o tráfego sem um caminho lógico para o NAT Gateway.

Resolução: Ajustei a rota, associando a sub-rede privada diretamente à Joao-RTPrivate. O teste subsequente (ping google.com) retornou 0% packet loss, comprovando o sucesso da configuração.

📸 Evidências
1. A Base: Criação da Amazon VPC do Zero
(Substitua esta linha pela imagem da Joao VPC - Amazon VPC 1.jpeg)

2. O Diagnóstico: Falha na Tabela de Rotas
(Substitua esta linha pela imagem da Tabela de Rotas - Amazon VPC 2.jpeg)

3. Troubleshooting: Conexão Estabelecida
(Substitua esta linha pela imagem do Terminal com o Ping - Amazon VPC 3.jpeg)

💡 Aprendizados e Impacto de Negócios
✅ Segurança em Dados: Entendimento prático de por que Data Lakes e bancos de dados devem sempre residir em sub-redes privadas.

✅ Troubleshooting Lógico: Como diagnosticar problemas de conectividade (packet loss) analisando tabelas de rotas e fluxo de tráfego, evitando o desperdício de tempo "apagando e refazendo" recursos.

✅ Acesso Blindado: Implementação do conceito de Jump Box (Bastion Host) e NAT Gateway para proteger a infraestrutura contra ataques externos.

🔗 Referências
Documentação Amazon VPC

Padrões de Arquitetura AWS para Bastion Hosts

Projeto realizado durante o programa AWS re/Start — Escola da Nuvem (Março de 2026)

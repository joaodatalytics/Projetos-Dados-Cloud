# 💰 Projeto 04 — FinOps na AWS: Monitoramento e Governança de Custos

![AWS](https://img.shields.io/badge/AWS-Cost_Explorer-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)
![Athena](https://img.shields.io/badge/AWS-Athena-EF9F27?style=for-the-badge&logo=amazonaws&logoColor=white)
![CloudWatch](https://img.shields.io/badge/AWS-CloudWatch-FF4F8B?style=for-the-badge&logo=amazonaws&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-1A9C3E?style=for-the-badge)

---

## 🛑 Problema

Equipes que operam na AWS sem visibilidade de custos descobrem gastos inesperados apenas na fatura do fim do mês, sem saber qual serviço, projeto ou responsável gerou o custo. O desafio era criar uma pipeline automatizada que coletasse, organizasse e alertasse sobre custos em tempo real, eliminando a dependência de revisão manual.

---

## 🎯 Objetivo

Implementar uma pipeline completa de FinOps na AWS, coletando dados de custo automaticamente via Lambda, armazenando no S3, consultando com Athena, configurando alertas de budget e automatizando governança de instâncias EC2 sem tags, tudo dentro do Free Tier.

---

## 🛠️ Serviços utilizados

| Serviço | Função |
|---|---|
| **Amazon EC2** | Instância de laboratório com tags de custo aplicadas |
| **Amazon S3** | Armazenamento dos dados de custo exportados pelo Lambda |
| **AWS Lambda** | Coleta diária de dados do Cost Explorer e governança de instâncias |
| **Amazon EventBridge** | Agendamento automático das funções Lambda |
| **AWS Cost Explorer** | Fonte dos dados de custo e uso por serviço e tag |
| **Amazon Athena** | Consulta SQL dos dados de custo armazenados no S3 |
| **AWS Budgets** | Alertas proativos de custo com múltiplos thresholds |
| **Amazon CloudWatch** | Alarmes de billing e monitoramento de instâncias ociosas |
| **Amazon SNS** | Notificações por e-mail dos alarmes e alertas |
| **AWS IAM** | Controle de acesso com roles e políticas específicas por função |

---

## 🏗️ Arquitetura da solução

```text
┌──────────────────────────────────────────────────────────────────┐
│                          AWS Account                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              Pipeline de Coleta de Dados                │     │
│  │                                                         │     │
│  │  EventBridge (cron diário 09h UTC)                      │     │
│  │       │                                                 │     │
│  │       ▼                                                 │     │
│  │  Lambda: finops-cost-collector                          │     │
│  │       │  (Python 3.12 — Role: lambda-finops-role)       │     │
│  │       │                                                 │     │
│  │       ├──→ Cost Explorer API                            │     │
│  │       │    (custo por serviço + tag Project)            │     │
│  │       │                                                 │     │
│  │       └──→ S3: seu-bucket-finops/                       │     │
│  │                costs/YYYY/MM/YYYY-MM-DD.json            │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌──────────────────────────┐   ┌──────────────────────────┐     │
│  │     Consulta de Dados    │   │    Alertas & Governança  │     │
│  │                          │   │                          │     │
│  │  Athena → finops_db      │   │  AWS Budgets             │     │
│  │  Queries SQL sobre       │   │  → 50% / 80% / 100%      │     │
│  │  os JSONs do S3          │   │  → SNS → E-mail          │     │
│  │                          │   │                          │     │
│  │  Results em:             │   │  CloudWatch Alarm        │     │
│  │  s3://.../athena-results │   │  → Billing > $2          │     │
│  │                          │   │  → EC2 CPU < 1% (ociosa) │     │
│  └──────────────────────────┘   └──────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │        Fase 6 — Automação de Governança                 │     │
│  │                                                         │     │
│  │  EventBridge (cron dias úteis 20h UTC / 17h Brasília)   │     │
│  │       │                                                 │     │
│  │       ▼                                                 │     │
│  │  Lambda: finops-governance-bot                          │     │
│  │  → Lista instâncias EC2 running                         │     │
│  │  → Verifica tags: Project, Environment, Owner           │     │
│  │  → Para instâncias sem tags obrigatórias                │     │
│  └─────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📋 Fases de implementação

| Fase | Nome | Tempo |
|---|---|---|
| 0 | Preparação da conta AWS (IAM, MFA, Cost Explorer) | 10–15 min |
| 1 | Simulação de ambiente com EC2 + S3 tagueados | 20–30 min |
| 2 | Exportação de dados de custo com Lambda + EventBridge |

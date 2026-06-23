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

📋 Fases de implementaçãoFaseNomeTempo0Preparação da conta AWS (IAM, MFA, Cost Explorer)10–15 min1Simulação de ambiente com EC2 + S3 tagueados20–30 min2Exportação de dados de custo com Lambda + EventBridge30–45 min3Consulta dos dados com Amazon Athena20–30 min4Alertas de custo com AWS Budgets10 min5Monitoramento com CloudWatch (billing + CPU ociosa)15 min6 ✦Automação Lambda para parar instâncias sem tag45 min🏷️ Tags aplicadas na EC2 (base do FinOps)

Project     = FinOpsLab
Environment = Dev
Owner       = SeuNome
CostCenter  = Laboratorio

Tags são a base do FinOps. Sem elas, não é possível filtrar custos por projeto no Cost Explorer.

⚙️ Lambda 1: finops-cost-collector
Coleta dados diários do Cost Explorer e salva como JSON no S3.

import boto3
import datetime
import json

ce = boto3.client('ce', region_name='us-east-1')
s3 = boto3.client('s3')

BUCKET = 'seu-bucket-finops-XXXX'

def lambda_handler(event, context):
    today = datetime.date.today()
    start = today.replace(day=1).strftime('%Y-%m-%d')
    end   = today.strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='DAILY',
        Metrics=['UnblendedCost', 'UsageQuantity'],
        GroupBy=[
            {'Type': 'DIMENSION', 'Key': 'SERVICE'},
            {'Type': 'TAG',       'Key': 'Project'}
        ]
    )

    payload = {
        'collected_at': str(datetime.datetime.utcnow()),
        'period': {'start': start, 'end': end},
        'data': response['ResultsByTime']
    }

    key = f"costs/{today.year}/{today.month:02d}/{today}.json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(payload, default=str),
        ContentType='application/json'
    )

    return {'statusCode': 200, 'key': key}

    Agendamento EventBridge: cron(0 9 * * ? *) → todo dia às 09h UTC (06h Brasília)

⚙️ Lambda 2: finops-governance-bot
Para automaticamente instâncias EC2 sem as tags obrigatórias.

import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
REQUIRED_TAGS = ['Project', 'Environment', 'Owner']

def lambda_handler(event, context):
    reservations = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )['Reservations']

    stopped = []
    for r in reservations:
        for i in r['Instances']:
            iid  = i['InstanceId']
            tags = {t['Key']: t['Value'] for t in i.get('Tags', [])}

            missing = [k for k in REQUIRED_TAGS if k not in tags]
            if missing:
                print(f"STOP {iid} — missing tags: {missing}")
                ec2.stop_instances(InstanceIds=[iid])
                stopped.append({'id': iid, 'missing_tags': missing})

    return {'stopped': stopped, 'total': len(stopped)}

    Agendamento EventBridge: cron(0 20 ? * MON-FRI *) → dias úteis às 20h UTC (17h Brasília)

🗂️ Queries Athena

-- Criar banco de dados
CREATE DATABASE finops_db;

-- Criar tabela externa apontando para o S3
CREATE EXTERNAL TABLE finops_db.cost_data (
  collected_at string,
  period       struct<start:string, end:string>,
  data         string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://seu-bucket-finops-XXXX/costs/'
TBLPROPERTIES ('has_encrypted_data'='false');

-- Ver registros coletados
SELECT * FROM finops_db.cost_data LIMIT 10;

-- Verificar datas coletadas
SELECT collected_at, period.start, period.end
FROM finops_db.cost_data
ORDER BY collected_at DESC;

🔔 Configuração de AlertasAWS Budgets, thresholds múltiplos:ThresholdAção50% do orçamentoE-mail de aviso antecipado80% do orçamentoE-mail principal de alerta100% do orçamentoE-mail de limite atingidoCloudWatch Alarms:Billing total estimado > $2 → SNS → E-mailEC2 CPU < 1% por 1h → instância ociosa candidata a desligamento📸 EvidênciasTags EC2:Alarmes do CloudWatch:Query Successful no Athena:Lambda Code:Test Lambda Code:Função Lambda instâncias EC2:Alerta Lambda para instâncias sem tag:Lambda desliga instância sem tag:💡 Aprendizados✅ FinOps não é só cortar custo: Antes desse lab, eu associava FinOps a "gastar menos". Na prática, percebi que o trabalho real é visibilidade — você não pode otimizar o que não consegue enxergar. A pipeline de coleta foi o alicerce de tudo.✅ O Cost Explorer é poderoso, mas cego sem tags: Consegui consultar custos por serviço facilmente, mas filtrar por projeto só funcionou depois que apliquei as tags corretamente na EC2. Sem tagging consistente, o Cost Explorer mostra números sem contexto; é como ter um extrato bancário sem descrição de compra.✅ Separar responsabilidades entre Lambdas faz diferença: Meu primeiro instinto era colocar coleta e governança na mesma função. Mantê-las separadas me obrigou a pensar em permissões IAM distintas, agendamentos diferentes e falhas independentes — um princípio que se aplica a qualquer arquitetura serverless.✅ Athena consulta JSON no S3 e isso é mais poderoso do que parece: Não precisei de banco de dados. Os JSONs salvos pelo Lambda viraram uma tabela consultável com SQL. Isso mudou minha visão sobre onde dados precisam "viver" para serem úteis.✅ Alertas em múltiplos thresholds evitam surpresa: Configurar apenas 100% do budget é tarde demais. Os alertas em 50% e 80% me fizeram pensar em custo como algo progressivo, não binário — uma mudança de mentalidade que carrego pra qualquer projeto cloud.✅ A Lambda de governança me ensinou sobre risco de automação: A função para instâncias sem tag funciona, mas durante os testes percebi que ela pararia qualquer instância, incluindo uma crítica esquecida sem tag. Em produção, isso exige uma lista de exclusão ou aprovação manual antes do stop. Automação sem salvaguarda é risco disfarçado de eficiência.✅ CloudWatch de billing precisa ser ativado manualmente: Perdi tempo tentando entender por que o alarme de billing não aparecia. A causa era simples: o monitoramento de billing no CloudWatch fica desativado por padrão na conta AWS e precisa ser habilitado nas preferências de billing. Um detalhe pequeno que custa horas se você não sabe.✅ Tag é cultura, não configuração: No começo, tratei as tags como um passo técnico do lab. No fim, entendi que tag sem processo de enforcement é tag que some. A Lambda de governança existe exatamente porque humanos não aplicam tags de forma consistente, e isso precisa ser automatizado para funcionar em escala.🔗 ReferênciasAWS Cost ExplorerAWS BudgetsAmazon AthenaAWS LambdaAmazon EventBridgeJoão Gabriel · Data Analyst & Cloud Analytics · Recife, Brazil

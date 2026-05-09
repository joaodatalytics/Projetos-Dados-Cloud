# ☁️ Projeto 02 — Infrastructure as Code (IaC) com AWS CloudFormation

![CloudFormation](https://img.shields.io/badge/AWS_CloudFormation-FF4F8B?style=for-the-badge&logo=amazon-aws&logoColor=white)
![RDS](https://img.shields.io/badge/Amazon_RDS-527FFF?style=for-the-badge&logo=amazon-rds&logoColor=white)
![S3](https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-1A9C3E?style=for-the-badge)

---

## 🎯 Objetivo

Provisionar de forma 100% automatizada uma infraestrutura em nuvem segura, escalável e otimizada para custos (Free Tier) utilizando **AWS CloudFormation**. O projeto foi desenhado separando o processamento, o armazenamento e a interface web, com o objetivo principal de criar um ambiente robusto capaz de sustentar pipelines de **Cloud Data Analytics**.

---

## 🛠️ Serviços utilizados

| Serviço | Função |
|---|---|
| **AWS CloudFormation** | Automação da infraestrutura via código (YAML) e provisionamento de recursos. |
| **Amazon VPC** | Virtual Private Cloud customizada com Internet Gateway e tabelas de roteamento. |
| **Amazon RDS (MySQL)** | Banco de dados relacional isolado em Subnets Privadas (Multi-AZ Ready). |
| **Amazon EC2** | Servidor Linux na Subnet Pública para processamento web (AMI dinâmica via SSM). |
| **Amazon S3** | Bucket público hospedando um portfólio serverless em arquivos estáticos (HTML/CSS). |
| **Amazon CloudWatch** | Configuração de alarmes de monitoramento para a CPU da instância. |

---

## 🏗️ Arquitetura da solução

```text
       Internet
          │
          ▼
 [ Internet Gateway ]
          │
 ┌────────▼─────────────────────────────────────────────────┐
 │                  VPC Customizada                         │
 │                                                          │
 │  ┌────────────────────────────────────────────────────┐  │
 │  │ Sub-rede Pública                                   │  │
 │  │                                                    │  │
 │  │  [ Servidor EC2 (Web) ] ◄──────(Alarmes)──────[ CW ]  │
 │  └─────────────┬──────────────────────────────────────┘  │
 │                │ (Acesso restrito via Security Group)    │
 │  ┌─────────────▼──────────────────────────────────────┐  │
 │  │ Sub-redes Privadas (Multi-AZ Ready)                │  │
 │  │                                                    │  │
 │  │  [ Amazon RDS MySQL (Banco de Dados) ]             │  │
 │  └────────────────────────────────────────────────────┘  │
 └──────────────────────────────────────────────────────────┘

 ────────────────────────────────────────────────────────────
  [ Amazon S3 ] ──► Hospedagem de Site Estático (Portfólio)
```

---

## 📋 Etapas de implementação (Deploy)

1. Faça o clone deste repositório para a sua máquina local.
2. Acesse o console da AWS > **CloudFormation** > **Create Stack**.
3. Faça o upload do arquivo de template `template-infra.yaml`.
4. Preencha os parâmetros dinâmicos solicitados pelo código (Nome do KeyPair e Nome único do Bucket S3).
5. Após o status atingir `CREATE_COMPLETE`, faça o upload do site estático (`index.html` e `perfil.jpg`) para o bucket S3 recém-criado via AWS CLI:

```bash
aws s3 cp index.html s3://portfolio-joao-gabriel/
aws s3 cp perfil.jpg s3://portfolio-joao-gabriel/
```

---

## 💡 Diferenciais Técnicos Aplicados

Ao invés de apenas criar os recursos, apliquei práticas avançadas de engenharia e governança de nuvem:

* **Segurança em Camadas (*Security by Design*):** O banco de dados (RDS) não possui IP público. Ele está blindado e programado para aceitar apenas conexões originadas do Security Group da instância EC2.
* **Previsibilidade com Change Sets:** Utilização de Change Sets para validar preventivamente como a arquitetura irá evoluir antes de aplicar as mudanças no ambiente de produção.
* **Custo Zero (FinOps):** Todo o código YAML foi rigorosamente parametrizado para manter os recursos dentro dos limites do AWS Free Tier (instância `t2.micro`, discos entre 8GB e 20GB, Single-AZ).

---

## 📸 Evidências

### 1. Automação: Criação e Revisão da Pilha
![Criação da Pilha](evidencias/Criação%20da%20Pilha%20-%2001.jpeg)

![Revisão da Pilha](evidencias/Revisão%20da%20Pilha%20-%2003.jpeg)

### 2. Infraestrutura Lançada com Sucesso
![Pilha Criada](evidencias/Pilha%20Criada%20-%2004.jpeg)

### 3. Computação e Rede Provisionadas (EC2 e VPC)
![EC2 Criada](evidencias/EC2%20Criada%20-%2005.jpeg)

![VPC Criada](evidencias/VPC%20Criada%20-%2007.jpeg)

### 4. Camada de Dados e Monitoramento (RDS e CloudWatch)
![RDS Criado](evidencias/RDS%20Criado%20-%2009.jpeg)

![CloudWatch Criada](evidencias/CloudWatch%20Criada%20-%2008.jpeg)

### 5. Entrega Final (Servidor Web e Bucket S3)
![Server Web Teste](evidencias/Server%20Web%20Teste%20-%2006.jpeg)

![Site Estático no S3](evidencias/Site%20Estático%20-%2010.jpeg)

---

## 🧠 Aprendizados e Impacto de Negócios

- ✅ **Agilidade Operacional:** Redução do tempo de deploy de horas de configuração manual para apenas alguns minutos executando um template, mitigando o erro humano.
- ✅ **Padronização:** Garantia de que os ambientes de Desenvolvimento, Homologação e Produção possam ser idênticos.
- ✅ **Integração de Dados:** Preparação de um terreno sólido e seguro para futuras ingestões de dados, pipelines e queries analíticas estruturadas.

---

## 🔗 Referências e Contato

- [Documentação AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/)
- **Autor:** João Gabriel
- **LinkedIn:** [Conecte-se comigo](https://www.linkedin.com/in/joaognscmnt-dados/)

---

*Projeto desenvolvido e aprimorado durante o programa AWS re/Start — Escola da Nuvem (Março de 2026)*

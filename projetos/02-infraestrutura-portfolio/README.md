# ☁️ AWS Infrastructure as Code (IaC) - Data Analytics Environment

Este projeto demonstra o provisionamento 100% automatizado de uma infraestrutura em nuvem segura, escalável e otimizada para custos (Free Tier) utilizando **AWS CloudFormation**. 

Desenvolvido como parte do meu avanço prático no programa **AWS re/Start (Escola da Nuvem)**, com foco em sustentar pipelines de **Cloud Data Analytics**.

## 🏗️ Arquitetura do Projeto

A infraestrutura foi desenhada para separar o processamento, o armazenamento e a interface web, aplicando as melhores práticas do mercado:

* **Camada Global (S3):** Bucket público hospedando um portfólio serverless em HTML/CSS.
* **Camada de Rede (VPC):** Virtual Private Cloud customizada com Internet Gateway e tabelas de roteamento.
* **Camada de Computação (EC2):** Servidor Linux na Subnet Pública para processamento, buscando a AMI (Amazon Linux 2) mais recente dinamicamente via Systems Manager (Parameter Store).
* **Camada de Dados (RDS MySQL):** Banco de dados relacional isolado em Subnets Privadas (Multi-AZ Ready) com acesso restrito via Security Groups.
* **Observabilidade:** Alarmes do AWS CloudWatch configurados para monitoramento de CPU.

## 🛠️ Tecnologias Utilizadas
* **AWS CloudFormation** (YAML)
* **Amazon S3, EC2, RDS, VPC, CloudWatch**
* **HTML5 / CSS3** (Frontend do Portfólio)

## 💡 Diferenciais Técnicos Aplicados
1.  **Segurança em Camadas:** O banco de dados (RDS) não possui IP público e só aceita conexões vindas do Security Group da instância EC2.
2.  **Previsibilidade com Change Sets:** Evolução da arquitetura validada preventivamente antes do deploy.
3.  **Custo Zero (FinOps):** Recursos rigorosamente parametrizados dentro dos limites do AWS Free Tier (`t2.micro`, discos de 8GB a 20GB, Single-AZ).

## 🚀 Como fazer o Deploy

1. Faça o clone deste repositório.
2. Acesse o console da AWS > **CloudFormation** > **Create Stack**.
3. Faça o upload do arquivo `template-infra.yaml`.
4. Preencha os parâmetros solicitados (Nome do KeyPair e Nome único do Bucket).
5. Após o status `CREATE_COMPLETE`, faça o upload do `index.html` e `perfil.jpg` para o bucket S3 criado usando o AWS CLI:
   ```bash
   aws s3 cp index.html s3://portfolio-joao-gabriel /
   aws s3 cp perfil.jpg s3://portfolio-joao-gabriel /

Desenvolvido por João Gabriel - Conecte-se comigo no https://www.linkedin.com/in/joaognscmnt-dados/.

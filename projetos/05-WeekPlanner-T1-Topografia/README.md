# 🗺️ Projeto Profissional — Cloud Data Architecture & Serverless Web App: WeekPlanner T1 Topografia

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-1A9C3E?style=for-the-badge)

---

## 📌 Sobre o Projeto

![Interface WeekPlanner T1 Topografia](./Weekplanner.png)
> *Interface da aplicação rodando em produção na Vercel, utilizada para gestão de equipes de campo.*

Este projeto prático consistiu no desenvolvimento de uma aplicação web completa (Full-Stack) voltada para a gestão de agendamentos e acompanhamento de pendências operacionais de uma equipe técnica de topografia.

O objetivo principal foi substituir controles locais isolados por uma **arquitetura de dados centralizada em nuvem (Serverless)**. A aplicação atua como a principal fonte de ingestão de dados de campo, estabelecendo uma fundação relacional sólida e íntegra para habilitar futuras modelagens analíticas (Cloud Data Analytics).

---

## 🏗️ Arquitetura da Solução

A engenharia da aplicação foi estruturada no modelo de **Monorepo** com arquitetura desacoplada, dividindo as camadas de apresentação, computação e persistência em provedores de nuvem especializados (*Free Tier Optimization*).

    [ Engenheiro / Topógrafo no Campo ]
                    │
                    ▼
    [ Portal Web (Frontend) ] ────────► Hospedado na Vercel
                    │ (HTTP Requests JSON)
                    ▼
    ┌─────────────────────────────────────────────────────────┐
    │                     Nuvem Serverless                    │
    │                                                         │
    │  [ API REST Backend ] ◄──────── Hospedado no Render     │
    │                       │         (Engine Python/FastAPI) │
    │                       │ (ORM / SQLAlchemy)              │
    │                       ▼                                 │
    │  [ Banco de Dados ]   ◄──────── Hospedado no Neon.tech  │
    │                                 (PostgreSQL 18)         │
    └─────────────────────────────────────────────────────────┘

---

## 🛠️ Tecnologias e Serviços Utilizados

| Camada | Tecnologia / Serviço | Função no Pipeline |
|---|---|---|
| **Frontend** | **Vercel / HTML / JS** | Hospedagem serverless da interface responsiva otimizada para coleta de dados via dispositivos móveis. |
| **Backend / API** | **Render / Python (FastAPI)** | Servidor assíncrono processando regras de negócio e validação estrutural dos dados (CRUD). |
| **Banco de Dados** | **Neon.tech (PostgreSQL)** | Armazenamento relacional em nuvem garantindo atomicidade e integridade das chaves estrangeiras. |
| **Integração** | **SQLAlchemy (ORM)** | Mapeamento objeto-relacional para tradução das rotas Python em dialeto SQL seguro contra injeções. |

---

## 🚀 Próximos Passos (Data Analytics)

Com o pipeline de ingestão funcionando e os dados da equipe sendo gravados corretamente no banco PostgreSQL relacional, a próxima fase do projeto consiste em conectar ferramentas de visualização de dados (como **Power BI**) diretamente ao servidor Neon. O foco será construir dashboards para a gestão extrair métricas como:
*   Balanceamento da carga de trabalho semanal por colaborador.
*   SLAs de resolução de vistorias planimétricas e planialtimétricas.

---

## 🔗 Contato

*   **Autor:** João Gabriel
*   **LinkedIn:** [Conecte-se comigo](https://www.linkedin.com/in/joaognscmnt-dados/)

---
*Projeto desenvolvido visando a estruturação de infraestruturas de dados e modelagem relacional em nuvem.*

# AUTOMOTIVENEWS - Automotive News Project
## Projeto de Coleta e Visualização de Notícias Automotivas

Este projeto é uma solução completa para coleta, processamento e distribuição de notícias automobilísticas, utilizando uma arquitetura moderna e tecnologias de ponta. O sistema é composto por uma API Gateway, backend, frontend, app móvel e processamento de IA.

## Estrutura do Projeto

    automotive-news-project/
    │
    ├── src/
    │   ├── api-gateway/            # Rust-based API Gateway
    │   ├── app/                    # Rust-based Mobile App (notícia e envio para Telegram)
    │   ├── backend/                # Backend principal em Rust
    │   ├── frontend/               # Frontend em React e Next.js
    │   ├── kafka/                  # Configurações e scripts relacionados ao Apache Kafka
    │   ├── machine-learning/       # Scripts e modelos para processamento de IA
    │   │   ├── models/             # Modelos treinados de IA
    │   │   └── scripts/            # Scripts de pré-processamento e inferência de IA
    │   ├── scraping/               # Scripts de scraping de notícias automotivas
    │   │   └── python-scripts/     # Scripts em Python para coleta de notícias
    │   └── database/               # Contém o MongoDB e PostgreSQL
    │       ├── mongodb/            # MongoDB para armazenamento de notícias e dados não estruturados
    │       │   ├── schemas/        # Esquemas para documentos armazenados no MongoDB
    │       │   └── utils/          # Scripts para conexão e manipulação do MongoDB
    │       └── postgres/           # PostgreSQL para armazenamento de dados estruturados
    │           ├── schemas/        # Esquemas para tabelas no PostgreSQL
    │           └── utils/          # Scripts para conexão e manipulação do PostgreSQL
    │
    ├── docker-compose.yml           # Arquivo Docker Compose para orquestração
    └── README.md                    # Documentação do projeto


## Sumário

- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## Arquitetura do Sistema

A arquitetura do sistema é composta por diversas etapas, integrando a coleta, armazenamento e visualização das notícias. A estrutura geral pode ser visualizada abaixo:

+----------------------+        +------------------------+        +---------------------+
|  Sites de Notícias   |        |   Scraping (Python)    |        | MongoDB (Database)  |
|     Automotivas      | -----> |  + Mensageria (Kafka)  | -----> | (Armazena Notícias) |
+----------------------+        +------------------------+        +---------------------+
                                    |          |                            |
                                    |          |                            |
                                    V          V                            V
               +--------------------------+ +------------------------+  +-----------------------+
               | Grupo Telegram (Notifica)| |  App (.NET MAUI, C#)   |  |      API (.NET)       |
               +--------------------------+ |      (Assina Kafka)    |  |    (Comunica com DB)  |    
                                            +------------------------+  +-----------------------+
                                                                                   |
                                                                                   |
                                                                                   V
                                                                        +-----------------------+
                                                                        |  Frontend (React)     |
                                                                        +-----------------------+



### Componentes:

1. **Sites de Notícias Automotivas**:
    - Fontes de onde as notícias são coletadas, utilizando scraping em páginas da web de interesse.

2. **Scraping (Python)**:
    - Um script Python realiza o web scraping em fontes selecionadas de notícias automotivas.
    - O sistema de mensageria com Kafka permite o envio e processamento assíncrono dos dados extraídos.

3. **MongoDB (Database)**:
    - Banco de dados NoSQL onde as notícias extraídas são armazenadas. O MongoDB é utilizado para gerenciar grandes volumes de dados não estruturados (notícias).

4. **Grupo Telegram (Automotive News)**:
    - As notícias são enviadas para um grupo do Telegram, mantendo os membros informados em tempo real.

5. **API (FastAPI)**:
    - Fornece uma interface para acessar as notícias armazenadas no MongoDB.
    - A API também permite integração com o frontend e outros serviços.

6. **Frontend (React)**:
    - Um frontend desenvolvido em React para exibir as notícias de forma interativa e dinâmica para os usuários finais.

## Tecnologias Utilizadas

- **Rust**: Para desenvolvimento da API Gateway, app móvel e backend.
- **React e Next.js**: Para desenvolvimento do frontend.
- **Apache Kafka**: Para mensageria e transmissão de dados.
- **MongoDB**: Para armazenamento de dados não estruturados, como notícias.
- **PostgreSQL**: Para armazenamento de dados estruturados.
- **Python**: Para scripts de scraping e processamento de IA.

## Funcionalidades

- Coleta de notícias automobilísticas através de scraping.
- Processamento de dados utilizando modelos de IA.
- Envio de notificações para usuários via Telegram.
- API para integração com frontend e app móvel.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu_usuario/repositorio.git
    cd repositorio
    ```

2. Instale as dependências do backend (Python):
    ```bash
    pip install -r requirements.txt
    ```

3. Configure o ambiente para o Kafka e MongoDB.

4. Rode os scripts de scraping:
    ```bash
    python scrape_news.py
    ```

5. Execute o servidor da API (FastAPI):
    ```bash
    uvicorn app.main:app --reload
    ```

6. Inicie o frontend (React):
    ```bash
    cd frontend
    npm install
    npm start
    ```

## Como Usar

- Acesse a interface web para visualizar as notícias automotivas extraídas.
- O grupo do Telegram será atualizado em tempo real com as notícias mais recentes.
- A API estará disponível para integrar as notícias com outras aplicações.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir um Pull Request ou reportar problemas no [repositório oficial](https://github.com/amauricunha/automotivenews).

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).




# AUTOMOTIVENEWS - Automotive News Project
## Projeto de Coleta e Visualização de Notícias Automotivas

Este projeto está sendo desenvolvido para aplicar conhecimentos em tecnlogias usadas em soluções integradas para a coleta, processamento, armazenamento e distribuição de dados, neste caso, notícias relacionadas ao setor automotivo. O sistema é composto por **API Gateway**, **Backend**, **Frontend**, **App Móvel**, **Processamento com IA** e **Mensageria Avançada**.

O objetivo principal do projeto é proporcionar uma experiência fluida e eficiente para usuários interessados em notícias automobilísticas, conectando fontes confiáveis, tecnologia de mensageria e uma interface amigável para consumo de informações. 


## Estrutura do Projeto

    automotive-news-project/
    │
    ├── src/
    │   ├── api/                     # Rust-based API Gateway
    │   │   ├── src/                 # Código-fonte do API Gateway
    │   │   ├── config/              # Configurações (ex.: arquivos YAML ou TOML)
    │   │   └── tests/               # Testes automatizados para o API Gateway
    │   │
    │   ├── app/                     # Rust-based Mobile App (consome Kafka e API para notificações)
    │   │   ├── src/                 # Código-fonte do app
    │   │   ├── assets/              # Recursos estáticos (imagens, ícones, etc.)
    │   │   └── tests/               # Testes do app
    │   │
    │   ├── backend/                 # Backend principal em Rust
    │   │   ├── src/                 # Código-fonte do backend
    │   │   ├── config/              # Configurações (ex.: variáveis de ambiente, YAML, etc.)
    │   │   ├── integration/         # Integrações com Kafka, Redis, Telegram, etc.
    │   │   └── tests/               # Testes do backend
    │   │
    │   ├── bot/                     # Telegram Bot para notificações (Python)
    │   │   ├── src/                 # Código-fonte principal do bot
    │   │   ├── config/              # Configurações do bot (tokens, variáveis de ambiente, etc.)
    │   │   └── tests/               # Testes unitários e de integração do bot
    │   │
    │   ├── frontend/                # Frontend em React e Next.js
    │   │   ├── src/                 # Código-fonte do frontend
    │   │   ├── components/          # Componentes reutilizáveis
    │   │   ├── pages/               # Páginas do Next.js
    │   │   ├── styles/              # Estilos CSS/SCSS
    │   │   └── tests/               # Testes de interface
    │   │
    │   ├── kafka/                   # Configurações e scripts relacionados ao Apache Kafka
    │   │   ├── config/              # Configurações do Kafka (server.properties, etc.)
    │   │   ├── topics/              # Gerenciamento e documentação dos tópicos do Kafka
    │   │   └── utils/               # Scripts utilitários (ex.: criação de tópicos)
    │   │
    │   ├── machine-learning/        # Scripts e modelos para processamento de IA
    │   │   ├── models/              # Modelos treinados de IA
    │   │   ├── data/                # Dados usados para treinamento/teste (opcional)
    │   │   ├── scripts/             # Scripts de pré-processamento e inferência de IA
    │   │   └── tests/               # Testes de modelos e inferências
    │   │
    │   ├── scraping/                # Scripts de scraping de notícias automotivas
    │   │   ├── src/                 # Código-fonte principal dos scrapers
    │   │   ├── config/              # Configurações (ex.: URLs, headers, etc.)
    │   │   ├── logs/                # Logs gerados pelos scrapers
    │   │   └── tests/               # Testes para validação de scraping
    │   │
    │   ├── redis/                   # Configurações e scripts relacionados ao Redis (cache)
    │   │   ├── configs/             # Configurações do Redis (redis.conf, etc.)
    │   │   ├── utils/               # Scripts utilitários para manipulação do Redis
    │   │   └── tests/               # Testes de integração do Redis
    │   │
    │   └── database/                # Contém MongoDB e PostgreSQL
    │       ├── mongodb/             # MongoDB para armazenamento de dados não estruturados
    │       │   ├── schemas/         # Esquemas para documentos armazenados no MongoDB
    │       │   ├── utils/           # Scripts para conexão e manipulação do MongoDB
    │       │   └── tests/           # Testes de integração com MongoDB
    │       │
    │       └── postgres/            # PostgreSQL para armazenamento de dados estruturados
    │           ├── schemas/         # Esquemas para tabelas no PostgreSQL
    │           ├── utils/           # Scripts para conexão e manipulação do PostgreSQL
    │           └── tests/           # Testes de integração com PostgreSQL
    │
    ├── tests/                       # Testes de integração e ponta a ponta (gerais)
    │   ├── integration/             # Testes de integração entre serviços
    │   └── e2e/                     # Testes ponta a ponta (ex.: Cypress para frontend)
    │
    ├── docs/                        # Documentação adicional
    │   ├── api/                     # Documentação da API (ex.: OpenAPI/Swagger)
    │   ├── architecture/            # Diagramas de arquitetura e fluxos
    │   └── setup/                   # Guias de configuração e deploy
    │
    ├── docker/                      # Configurações Docker específicas
    │   ├── images/                  # Dockerfiles para imagens customizadas
    │   ├── scripts/                 # Scripts de inicialização de contêineres
    │   └── volumes/                 # Volumes persistentes
    │
    ├── docker-compose.yml           # Arquivo Docker Compose para orquestração
    ├── Makefile                     # Comandos de automação de build, testes e deploy
    ├── .env                         # Variáveis de ambiente
    ├── .gitignore                   # Arquivos e pastas ignorados pelo Git
    └── README.md                    # Documentação geral do projeto


## Sumário

- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Componentes](#componentes)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## Arquitetura do Sistema

A arquitetura do sistema é composta por diversas etapas, integrando a coleta, armazenamento e visualização das notícias. A estrutura geral pode ser visualizada abaixo:

```bash
+----------------------+                      +----------------------------------+          +------------------------------------------------+
|  Sites de Notícias   |                      | Machine Learning (Python)        |          | Redis (Cache)                                  |
|     Automotivas      |                      | - Consome mensagens do Kafka     |<-------->| - Inferências e dados de uso frequente         |
+----------------------+                      | - Processa e retorna para Kafka  |          +------------------------------------------------+ 
           |                                  | - Cache de inferências com Redis |              ^
           |                                  +----------------------------------+              |        +------------------------------------------------+
           |------------------------|                ^                          ^               |        | MongoDB (Database)                             |
                                    |                |                          |               |        | - Armazena Notícias, Entrada e saída de        |
                                    |                |                          |               |        |   inferências, Histórico de resultados para    |
                                    |                |                          |               |        |   análises ou relatórios futuros               |
                                    |                |                          |               |        +------------------------------------------------+
                                    |                |                          |               |        | PostgreSQL (Database)                          |
                                    |                |                          |               |        | - Dados Estruturados                           |
                                    V                V                          |               |        +------------------------------------------------+
                                +--------------------------+                    V               V           ^  
                                |   Mensageria (Kafka)     |               +---------------------------+    |
                                |  + Scraping (Python))    |<------------->| Backend (Rust)            |    |
                                +--------------------------+               | - Comunica com DB, Cache, |<---|
                                                          ^                |   Kafka e gerencia lógica)|
                                                          |                +---------------------------+
                                                          |                 ^
                                                          |                 |
                                                          V                 V                                 
    +-----------------------+                         +-----------------------+
    |Telegram Bot (Python)  |<----------------------->| API Gateway (Rust)    |
    +-----------------------+                         +-----------------------+
                 ^                                          ^               ^
                 |                                          |               |
                 V                                          V               |
    +--------------------------+         +-------------------------+        |
    | Grupo Telegram (Notifica)|         | App (Rust-based)        |        V
    +--------------------------+         | - API para notificações |     +-----------------------+
                                         |   e API para operações  |     |  Frontend (React)     |
                                         +-------------------------+     +-----------------------+
```

## Componentes:

1. **Sites de Notícias Automotivas**:
    - Fontes de onde as notícias são coletadas, utilizando scraping em páginas da web de interesse.

2. **Scraping (Python)**:
    - Um script Python realiza o web scraping em fontes selecionadas de notícias automotivas.
    - O sistema de mensageria com Kafka permite o envio e processamento assíncrono dos dados extraídos.

3. **Redis (Cache)**:
    - Implementado para otimizar o desempenho e reduzir a latência no processamento de inferências e dados frequentemente acessados.

4. **MongoDB (Database)**:
    - Banco de dados NoSQL onde as notícias extraídas são armazenadas.
    - Utilizado para gerenciar grandes volumes de dados não estruturados (notícias).

5. **Grupo Telegram (Automotive News)**:
    - As notícias são enviadas para um grupo do Telegram, mantendo os membros informados em tempo real por meio de um bot Python.

6. **API Gateway (Rust)**:
    - Um gateway centralizado desenvolvido em Rust para gerenciar requisições e integração entre os serviços backend e frontend.

7. **Frontend (React e Next.js)**:
    - Uma interface interativa e dinâmica para exibição das notícias.
    - Desenvolvida com React e Next.js para melhor desempenho e otimização.

8. **App Móvel (Rust)**:
    - Um aplicativo móvel desenvolvido em Rust para usuários finais, que consome notificações e notícias em tempo real.

9. **Apache Kafka (Mensageria)**:
    - Para transmissão assíncrona de dados, incluindo o envio de mensagens entre os componentes do sistema.

10. **PostgreSQL (Database)**:
    - Banco de dados relacional usado para gerenciar dados estruturados, como dados de usuários e estatísticas do sistema.

## Tecnologias Utilizadas

- **Rust**: Para desenvolvimento da API Gateway, backend e app móvel.
- **React e Next.js**: Para desenvolvimento do frontend.
- **Apache Kafka**: Para mensageria e transmissão de dados.
- **Redis**: Para armazenamento em cache de dados frequentemente acessados.
- **MongoDB**: Para armazenamento de dados não estruturados, como notícias.
- **PostgreSQL**: Para armazenamento de dados estruturados.
- **Python**: Para scripts de scraping, IA e Telegram Bot.

## Funcionalidades

- **Coleta de Notícias**:
    - Realiza scraping de notícias automobilísticas em sites selecionados.
    - Permite o uso de filtros para selecionar palavras-chave.

- **Mensageria Avançada**:
    - Utiliza Apache Kafka para processar e transmitir dados entre os serviços.
    - Redis melhora a performance em requisições frequentes.

- **Processamento com IA**:
    - Classificação e priorização de notícias baseadas em relevância.
    - Geração de resumos automáticos.

- **Notificações em Tempo Real**:
    - Envia notificações para usuários via Telegram Bot.

- **Interface Amigável**:
    - Exibição das notícias extraídas em uma interface web desenvolvida em React.
    - App móvel para usuários acessarem notícias diretamente em seus dispositivos.


## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu_usuario/repositorio.git
    cd repositorio
    ```

2. Configure o ambiente:
    - Adicione o arquivo `.env` na raiz do projeto com as seguintes variáveis:
      ```plaintext
      TELEGRAM_BOT_TOKEN=<token_do_bot>
      KAFKA_HOST=<host_kafka>
      REDIS_HOST=<host_redis>
      MONGO_URI=<uri_mongodb>
      POSTGRES_URI=<uri_postgresql>
      ```

3. Instale as dependências do backend (Python):
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o Redis, Kafka, MongoDB e PostgreSQL.

5. Rode os scripts de scraping:
    ```bash
    python src/scraping/scrape_news.py
    ```

6. Execute o servidor da API Gateway (Rust):
    ```bash
    cargo run --release
    ```

7. Inicie o frontend (React):
    ```bash
    cd src/frontend
    npm install
    npm run dev
    ```

8. Inicie o Telegram Bot:
    ```bash
    python src/telegram-bot/main.py
    ```

## Como Usar

- **Interface Web**:
    - Acesse a interface web para visualizar as notícias automotivas extraídas.
    - Use filtros disponíveis para explorar notícias relevantes.

- **Grupo do Telegram**:
    - Receba notificações em tempo real sobre novas notícias automobilísticas.

- **App Móvel**:
    - Acesse diretamente do app notícias e notificações personalizadas.

## Acompanhamento do Projeto
A proposta desse projeto é mantê-lo com contribuidores, como um projeto para desenvolvimento de habilidades.

### Issues

Utilizaremos o sistema de **Issues** do GitHub para rastrear bugs, novos recursos, melhorias e tarefas em andamento. Você poderá acompanhar o progresso do projeto, verificar o que está sendo trabalhado, e também sugerir novas funcionalidades ou relatar problemas.

- **Bug**: Relatar erros encontrados no sistema.
- **Feature Request**: Sugerir novas funcionalidades ou melhorias.
- **In Progress**: Tarefas que estão atualmente em andamento.
- **Completed**: Funcionalidades ou correções concluídas.

### Pull Requests (PRs)

O processo de desenvolvimento será colaborativo. Se você tiver sugestões ou melhorias, sinta-se à vontade para criar um **Pull Request**. Ao fazer isso, um dos mantenedores revisará as modificações e, se aprovado, o código será integrado ao projeto principal.

### Project Board

Utilizaremos o **Project Board** do GitHub para gerenciar as tarefas do projeto de forma visual e organizada. O quadro é dividido em colunas como:

- **To Do**: Tarefas que ainda precisam ser iniciadas.
- **In Progress**: Tarefas que estão sendo trabalhadas ativamente.
- **Done**: Tarefas concluídas.

Isso facilita o acompanhamento do andamento do projeto e das prioridades.

### Logs de Versão

As atualizações e alterações importantes no projeto serão registradas no **Changelog**. Cada nova versão ou release será detalhada com as mudanças significativas, correções de bugs e adição de novas funcionalidades. Você poderá consultar o histórico de versões para ver a evolução do projeto.

### Contribuindo

Caso queira contribuir para o projeto, consulte a seção [**Contribuindo**](#contribuindo) para entender como pode ajudar. Estamos abertos a melhorias, correções e sugestões!

### Como Acompanhar

1. **Star o repositório**: Dê uma estrela no repositório para ser notificado sobre novas atualizações.
2. **Watch**: Se deseja ser notificado de todas as atividades no repositório, ative a opção de **watch** no GitHub.
3. **Participar de Discussões**: Se houver alguma dúvida ou discussão aberta, você pode participar ativamente nas **Discussions** do repositório.

Fique à vontade para acompanhar o progresso do projeto e participar de sua evolução!

## Contribuindo

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:
1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b minha-feature
3. Faça as alterações e submeta um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
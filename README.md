# 🌐 Portal Dinâmico de Notícias Tech

![Vue.js](https://img.shields.io/badge/vue-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![Quasar](https://img.shields.io/badge/Quasar-16B7ED?style=for-the-badge&logo=quasar&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Uma plataforma Full-Stack automatizada focada na agregação e exibição em tempo real de matérias sobre a esfera da Tecnologia (Linguagens de programação, Mercado de Trabalho, Inteligência Artificial e Afins). 

O software varre portais especializados (Web Scraping direcionado ao G1) e transmite os novos conteúdos captados via **WebSocket** diretamente para a interface dos clientes conectados à rede de forma reativa. 

---

## ✨ Features e Funcionalidades

- **Scraping Automatizado**: Motor backend desenvolvido em `BeautifulSoup4` capaz de analisar estruturalmente páginas e pescar as tags essenciais contendo título, resumo e a foto-capa original da matéria.
- **Transmissão Bidirecional (WebSockets)**: Os usuários não precisam dar refresh na tela; a malha de componentes escuta um servidor de socket dinâmico em `ws://` enviando eventos de sincronia em tempo real quando novas matérias chegam no banco.
- **Fluxo de Autenticação Robusto (JWT)**: A segurança de painéis conta com Middlewares interceptadores para assinar e validar Tokens Bearer. O front-end blinda o acesso utilizando Navigation Guards de Rotas acoplados à Store do Pinia.
- **Dois Níveis de Acesso**: 
    - Supremos `Admins` que podem engatilhar Scrapers manuais, registrar Colaboradores e apagar notícias lixo da plataforma.
    - `Colaboradores` padrão para visualização do fluxo de fundo da empresa limitados na leitura.
- **Design SPA Elegante**: Usufruindo do poder total do ecossistema Quasar, contando com CSS Utilirário dinâmico, navegação sem refetch da tela, drawers laterais responsivos e menus modulares, recriando o layout de feeds modernos.

---

## 🛠 Arquitetura do Repositório

O repositório está quebrado logicamente em três camadas macro rodando fluidamente via ambiente orquestrado Docker.

```bash
projeto-noticias-tecnologias/
├── backend/                # Aplicação FastAPI Core
│   ├── app/                # Endpoints (api), DB Schema (models), Schemas Pydantic, Workers de Scraping
│   ├── Dockerfile          # Builder da imagem Python 3.10
│   └── requirements.txt    # Gestor de pacotes (passlib, sqlalchemy, etc)
├── frontend/               # Aplicação Vue 3 (Vite + Quasar)
│   ├── src/                # Boot, Components, Layouts, Core Pages do Portal e Router config
│   ├── Dockerfile          # Builder da imagem em Node 22+
│   └── quasar.config.js    # Injetor global de plugins e dev config
└── docker-compose.yml      # Master builder que compila Back, Front e atrela o microserviço do Postgres.
```

---

## 🚀 Como Executar Localmente

### 1. Pré-Requisitos
- Ter o [Docker](https://www.docker.com/) e o `compose plugin` instalados na sua máquina local.
- Conexão à internet para a primeira varredura das dependências.

### 2. Levantando o Ambiente

Rode o comando mestre diretamente da pasta onde se encontra o arquivo `docker-compose.yml`. Todos os ambientes e a network de comunicação surgirão num piscar de olhos:
```bash
docker compose up -d --build
```
> O parâmetro `-d` garante que os containers rodem no formato background para o terminal não travar.
> O Postgres, o Uvicorn do Backend a porta de compilação do Vite do Frontend trabalharão sozinhos!

### 3. Acessando a Aplicação
Com tudo esverdeado nos logs, sinta-se livre para acessar:
- 🌐 **O Painel de Notícias**: http://localhost:9000
- 📜 **Swagger UI da API e Documentação**: http://localhost:8000/docs

### 4. Entrando Pela Primeira Vez
O evento `Lifespan` nativo do projeto percebe o momento exato em que a tabela é criada e insere um **Usuário Administrador de Emergência** para você testar a engrenagem no primeiro *Take*.

**Credenciais:**
- **E-mail:** `admin@tecnologia.com`
- **Senha:** `admin123`

Entre, aperte em **Acionar Scraper** e divirta-se!

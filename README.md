# CodeFlix Catalog Admin

Sistema de administração de catálogo para a plataforma CodeFlix, desenvolvido seguindo os princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**.

## 📋 Descrição

Este projeto é uma API REST para gerenciamento de **categorias**, **gêneros** e **membros de elenco (cast members)** de vídeos, construída com Django e Django REST Framework. A arquitetura foi projetada para ser desacoplada, testável e de fácil manutenção.

## 🏗️ Arquitetura

O projeto segue a **Clean Architecture**, separando as responsabilidades em camadas:

```
src/
├── core/                          # Núcleo da aplicação (independente de framework)
│   ├── category/
│   │   ├── domain/                # Entidades e contratos do domínio
│   │   │   ├── category.py        # Entidade Category
│   │   │   └── category_repository.py  # Interface do repositório
│   │   ├── application/           # Casos de uso
│   │   │   └── usecase/
│   │   │       ├── create_category.py
│   │   │       ├── delete_category.py
│   │   │       ├── get_category.py
│   │   │       ├── list_category.py
│   │   │       └── update_category.py
│   │   ├── infra/                 # Implementações de infraestrutura
│   │   │   └── in_memory_category_repository.py
│   │   └── tests/                 # Testes unitários e de integração
│   │
│   ├── genre/
│   │   ├── domain/                # Entidades e contratos do domínio
│   │   │   ├── genre.py           # Entidade Genre
│   │   │   └── genre_repository.py  # Interface do repositório
│   │   ├── application/           # Casos de uso
│   │   │   └── usecase/
│   │   │       ├── create_genre.py
│   │   │       ├── delete_genre.py
│   │   │       ├── list_genre.py
│   │   │       └── update_genre.py
│   │   ├── infra/                 # Implementações de infraestrutura
│   │   │   └── in_memory_genre_repository.py
│   │   └── tests/                 # Testes unitários e de integração
│   │
│   └── cast_member/
│       ├── domain/                # Entidades e contratos do domínio
│       │   ├── cast_member.py     # Entidade CastMember
│       │   └── cast_member_repository.py  # Interface do repositório
│       ├── application/           # Casos de uso
│       │   └── usecase/
│       │       ├── create_cast_member.py
│       │       ├── delete_cast_member.py
│       │       ├── list_cast_member.py
│       │       └── update_cast_member.py
│       ├── infra/                 # Implementações de infraestrutura
│       │   └── in_memory_cast_member_repository.py
│       └── tests/                 # Testes unitários e de integração
│
└── django_project/                # Camada de infraestrutura Django
    ├── category_app/
    │   ├── models.py              # Model Django
    │   ├── repository.py          # Implementação do repositório com ORM
    │   ├── views.py               # ViewSet da API REST
    │   ├── serializers.py         # Serializers DRF
    │   └── tests/                 # Testes de integração Django
    │
    ├── genre_app/
    │   ├── models.py              # Model Django
    │   ├── repository.py          # Implementação do repositório com ORM
    │   ├── views.py               # ViewSet da API REST
    │   ├── serializers.py         # Serializers DRF
    │   └── tests/                 # Testes de integração Django
    │
    └── cast_member_app/
        ├── models.py              # Model Django
        ├── repository.py          # Implementação do repositório com ORM
        ├── views.py               # ViewSet da API REST
        ├── serializers.py         # Serializers DRF
        └── tests/                 # Testes de integração Django
```

## 🚀 Tecnologias

- **Python 3.x**
- **Django 6.0**
- **Django REST Framework**
- **pytest** (testes)
- **SQLite** (banco de dados)

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/LeomaraAC/codeflix-catalog-admin.git
cd codeflix-catalog-admin
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações

```bash
python manage.py migrate
```

### 5. Inicie o servidor

```bash
python manage.py runserver
```

## 🔌 API Endpoints

### Categories (`/api/categories/`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/categories/` | Lista todas as categorias |
| `GET` | `/api/categories/{id}/` | Obtém uma categoria específica |
| `POST` | `/api/categories/` | Cria uma nova categoria |
| `PUT` | `/api/categories/{id}/` | Atualiza uma categoria |
| `PATCH` | `/api/categories/{id}/` | Atualiza parcialmente uma categoria |
| `DELETE` | `/api/categories/{id}/` | Remove uma categoria |

### Genres (`/api/genres/`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/genres/` | Lista todos os gêneros |
| `POST` | `/api/genres/` | Cria um novo gênero |
| `PUT` | `/api/genres/{id}/` | Atualiza um gênero |
| `DELETE` | `/api/genres/{id}/` | Remove um gênero |

### Cast Members (`/api/cast_members/`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/cast_members/` | Lista todos os membros de elenco |
| `POST` | `/api/cast_members/` | Cria um novo membro de elenco |
| `PUT` | `/api/cast_members/{id}/` | Atualiza um membro de elenco |
| `DELETE` | `/api/cast_members/{id}/` | Remove um membro de elenco |

### Exemplos de Requisição

**Criar categoria:**
```bash
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Filmes", "description": "Categoria de filmes", "is_active": true}'
```

**Criar gênero:**
```bash
curl -X POST http://localhost:8000/api/genres/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Ação", "is_active": true, "category_ids": ["<category-uuid>"]}'
```

**Criar membro de elenco:**
```bash
curl -X POST http://localhost:8000/api/cast_members/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Robert Downey Jr.", "type": "ACTOR"}'
```

**Resposta (criação):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## 🧪 Testes

O projeto possui uma suíte completa de testes:

- **Testes Unitários**: Testam componentes isolados (domínio, casos de uso)
- **Testes de Integração**: Testam a integração entre camadas
- **Testes E2E**: Testam fluxos completos da aplicação

### Executar todos os testes

```bash
pytest
```

### Executar testes específicos

```bash
# Testes unitários do domínio - Category
pytest src/core/category/tests/domain/

# Testes unitários do domínio - Genre
pytest src/core/genre/tests/domain/

# Testes unitários do domínio - CastMember
pytest src/core/cast_member/tests/domain/

# Testes unitários dos casos de uso - Category
pytest src/core/category/tests/application/usecase/unit/

# Testes unitários dos casos de uso - Genre
pytest src/core/genre/tests/application/usecase/unit/

# Testes unitários dos casos de uso - CastMember
pytest src/core/cast_member/tests/application/unit/

# Testes de integração dos casos de uso - Category
pytest src/core/category/tests/application/usecase/integration/

# Testes de integração dos casos de uso - Genre
pytest src/core/genre/tests/application/usecase/integration/

# Testes de integração dos casos de uso - CastMember
pytest src/core/cast_member/tests/application/integration/

# Testes da camada Django - Category
pytest src/django_project/category_app/tests/

# Testes da camada Django - Genre
pytest src/django_project/genre_app/tests/

# Testes da camada Django - CastMember
pytest src/django_project/cast_member_app/tests/

# Testes E2E
pytest src/tests_e2e/
```

## 📂 Estrutura de Testes

```
tests/
├── category/
│   ├── domain/                        # Testes da entidade Category
│   ├── application/usecase/
│   │   ├── unit/                      # Testes unitários (mock do repositório)
│   │   └── integration/               # Testes de integração (repositório real)
│   └── infra/                         # Testes do repositório in-memory
│
├── genre/
│   ├── domain/                        # Testes da entidade Genre
│   ├── application/usecase/
│   │   ├── unit/                      # Testes unitários (mock do repositório)
│   │   └── integration/               # Testes de integração (repositório real)
│   └── infra/                         # Testes do repositório in-memory
│
├── cast_member/
│   ├── domain/                        # Testes da entidade CastMember
│   ├── application/
│   │   ├── unit/                      # Testes unitários (mock do repositório)
│   │   └── integration/               # Testes de integração (repositório real)
│   └── infra/                         # Testes do repositório in-memory
│
├── django_project/
│   ├── category_app/tests/            # Testes de integração Django (Category)
│   ├── genre_app/tests/               # Testes de integração Django (Genre)
│   └── cast_member_app/tests/         # Testes de integração Django (CastMember)
│
└── tests_e2e/                         # Testes end-to-end
```

## 🎯 Casos de Uso

### Category

#### CreateCategory
Cria uma nova categoria no sistema.

#### GetCategory
Obtém os detalhes de uma categoria pelo ID.

#### ListCategory
Lista todas as categorias cadastradas.

#### UpdateCategory
Atualiza os dados de uma categoria existente.

#### DeleteCategory
Remove uma categoria do sistema.

### Genre

#### CreateGenre
Cria um novo gênero no sistema. Valida se todas as categorias associadas existem.

#### ListGenre
Lista todos os gêneros cadastrados.

#### UpdateGenre
Atualiza os dados de um gênero existente, incluindo as categorias associadas.

#### DeleteGenre
Remove um gênero do sistema.

### CastMember

#### CreateCastMember
Cria um novo membro de elenco no sistema (ator ou diretor).

#### ListCastMember
Lista todos os membros de elenco cadastrados.

#### UpdateCastMember
Atualiza os dados de um membro de elenco existente.

#### DeleteCastMember
Remove um membro de elenco do sistema.

## 📝 Entidades

### Category

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único (gerado automaticamente) |
| `name` | string | Nome da categoria (máx. 255 caracteres) |
| `description` | string | Descrição da categoria (opcional) |
| `is_active` | boolean | Status ativo/inativo |

#### Regras de Negócio

- O nome da categoria é **obrigatório**
- O nome não pode exceder **255 caracteres**
- Uma categoria pode ser **ativada** ou **desativada**

### Genre

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único (gerado automaticamente) |
| `name` | string | Nome do gênero (máx. 255 caracteres) |
| `is_active` | boolean | Status ativo/inativo |
| `categories` | set[UUID] | Conjunto de IDs das categorias associadas |

#### Regras de Negócio

- O nome do gênero é **obrigatório**
- O nome não pode exceder **255 caracteres**
- Um gênero pode ser **ativado** ou **desativado**
- Um gênero pode estar associado a **múltiplas categorias**
- Ao criar um gênero, todas as **categorias devem existir** no sistema

### CastMember

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único (gerado automaticamente) |
| `name` | string | Nome do membro de elenco (máx. 255 caracteres) |
| `type` | CastMemberType | Tipo: `ACTOR` ou `DIRECTOR` |

#### Regras de Negócio

- O nome do membro de elenco é **obrigatório**
- O nome não pode exceder **255 caracteres**
- O tipo deve ser **ACTOR** (ator) ou **DIRECTOR** (diretor)

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

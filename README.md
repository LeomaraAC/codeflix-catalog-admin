# CodeFlix Catalog Admin

Sistema de administração de catálogo para a plataforma CodeFlix, desenvolvido seguindo os princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**.

## 📋 Descrição

Este projeto é uma API REST para gerenciamento de categorias de vídeos, construída com Django e Django REST Framework. A arquitetura foi projetada para ser desacoplada, testável e de fácil manutenção.

## 🏗️ Arquitetura

O projeto segue a **Clean Architecture**, separando as responsabilidades em camadas:

```
src/
├── core/                          # Núcleo da aplicação (independente de framework)
│   └── category/
│       ├── domain/                # Entidades e contratos do domínio
│       │   ├── category.py        # Entidade Category
│       │   └── category_repository.py  # Interface do repositório
│       ├── application/           # Casos de uso
│       │   └── usecase/
│       │       ├── create_category.py
│       │       ├── delete_category.py
│       │       ├── get_category.py
│       │       ├── list_category.py
│       │       └── update_category.py
│       ├── infra/                 # Implementações de infraestrutura
│       │   └── in_memory_category_repository.py
│       └── tests/                 # Testes unitários e de integração
│
└── django_project/                # Camada de infraestrutura Django
    └── category_app/
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

A API está disponível em `/api/categories/`:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/categories/` | Lista todas as categorias |
| `GET` | `/api/categories/{id}/` | Obtém uma categoria específica |
| `POST` | `/api/categories/` | Cria uma nova categoria |
| `PUT` | `/api/categories/{id}/` | Atualiza uma categoria |
| `PATCH` | `/api/categories/{id}/` | Atualiza parcialmente uma categoria |
| `DELETE` | `/api/categories/{id}/` | Remove uma categoria |

### Exemplo de Requisição

**Criar categoria:**
```bash
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Filmes", "description": "Categoria de filmes", "is_active": true}'
```

**Resposta:**
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
# Testes unitários do domínio
pytest src/core/category/tests/domain/

# Testes unitários dos casos de uso
pytest src/core/category/tests/application/usecase/unit/

# Testes de integração dos casos de uso
pytest src/core/category/tests/application/usecase/integration/

# Testes da camada Django
pytest src/django_project/category_app/tests/

# Testes E2E
pytest src/tests_e2e/
```

## 📂 Estrutura de Testes

```
tests/
├── domain/                        # Testes da entidade Category
├── application/usecase/
│   ├── unit/                      # Testes unitários (mock do repositório)
│   └── integration/               # Testes de integração (repositório real)
├── infra/                         # Testes do repositório in-memory
└── tests_e2e/                     # Testes end-to-end
```

## 🎯 Casos de Uso

### CreateCategory
Cria uma nova categoria no sistema.

### GetCategory
Obtém os detalhes de uma categoria pelo ID.

### ListCategory
Lista todas as categorias cadastradas.

### UpdateCategory
Atualiza os dados de uma categoria existente.

### DeleteCategory
Remove uma categoria do sistema.

## 📝 Entidade Category

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único (gerado automaticamente) |
| `name` | string | Nome da categoria (máx. 255 caracteres) |
| `description` | string | Descrição da categoria (opcional) |
| `is_active` | boolean | Status ativo/inativo |

### Regras de Negócio

- O nome da categoria é **obrigatório**
- O nome não pode exceder **255 caracteres**
- Uma categoria pode ser **ativada** ou **desativada**

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

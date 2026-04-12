# Sistema Locadora – Dashboard e Exportação

# Teste

Aplicação full-stack construída em Flask + Vanilla JS para gerenciar uma locadora fictícia. O projeto oferece CRUD completo de clientes, filmes e aluguéis, além de um dashboard analítico com filtros de período, gráficos (curva S, donut, barras) e exportação de relatórios (CSV/XLSX) com histórico de downloads.

## Sumário
1. [Arquitetura & Tecnologias](#arquitetura--tecnologias)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração do Ambiente](#configuração-do-ambiente)
4. [Execução](#execução)
5. [Endpoints Principais](#endpoints-principais)
6. [Exportações & Histórico](#exportações--histórico)
7. [Estrutura de Pastas](#estrutura-de-pastas)
8. [Testes & Dicas](#testes--dicas)

## Arquitetura & Tecnologias
- **Backend**: [Flask 3](https://flask.palletsprojects.com/), Flask-CORS, Flask-SQLAlchemy.
- **Banco**: PostgreSQL (Supabase) acessado via SQLAlchemy/psycopg2.
- **Frontend**: HTML/CSS/JS puro, Chart.js para gráficos.
- **Planilhas**: Pandas + OpenPyXL para gerar CSV/XLSX.
- **Histórico**: Tabela `historico_exportacoes` registra cada exportação com metadados (período, formato, bytes, status).

## Pré-requisitos
- Python 3.12+
- Projeto criado no Supabase (PostgreSQL)
- Variáveis de ambiente configuradas no arquivo `.env`

## Configuração do Ambiente
```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/Sistema-Locadora.git
cd Sistema-Locadora

# 2. Crie e ative a virtualenv (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instale as dependências
pip install -r requirements.txt
```
> Dica: se usar Linux/macOS, ative com `source .venv/bin/activate`.

## Execução
```bash
# Ainda dentro da virtualenv
python run.py
```
O Flask sobe em `http://127.0.0.1:5000`. As páginas HTML ficam em `frontend/`; abra `frontend/dashboard.html` ou `frontend/index.html` diretamente no navegador (ou sirva com qualquer static server). Para consumir a API via fetch, use `http://localhost:5000` (já configurado no JS).

### Variáveis importantes
- Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`.
- Informe as credenciais fornecidas pelo Supabase (Host, User, Password, DB Name).

## Endpoints Principais
| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/clientes/` | Lista clientes |
| POST | `/clientes/` | Cria cliente |
| GET | `/filmes/` | Lista filmes |
| POST | `/alugueis/` | Cria aluguel |
| GET | `/dashboard/resumo` | KPIs filtrados por período (query params `inicio`,`fim`) |
| GET | `/dashboard/series` | Dados para curva S |
| GET | `/dashboard/status` | Dados para donut |
| GET | `/dashboard/top-filmes` | Top filmes |
| POST | `/exportacoes` | Gera CSV/XLSX e devolve arquivo |
| GET | `/exportacoes/historico` | Lista últimas exportações |

> Todos os endpoints de dashboard/exportação aceitam `inicio` e `fim` no formato `YYYY-MM-DD`.

## Exportações & Histórico
1. Abra `frontend/dashboard.html`.
2. Clique em **Exportar** ➜ escolha **tipo** (Aluguéis/Filmes), **formato** (CSV/XLSX) e período.
3. O backend gera o arquivo com Pandas e retorna o download.
4. Cada tentativa é logada em `historico_exportacoes` com status `sucesso` ou `erro`.
5. O card "Histórico de downloads" mostra as últimas entradas (data/hora, tipo, formato, período, registros, status).

### Formatos
- **CSV**: delimitador `;`, codificação UTF-8 BOM (compatível com Excel PT-BR).
- **XLSX**: única aba "Relatório".

## Estrutura de Pastas
```
app/
  controllers/        # Lógica de negócios (aluguel, dashboard, exportação ...)
  models/             # SQLAlchemy models (Cliente, Filme, Aluguel, HistoricoExportacao)
  routes/             # Blueprints Flask
  config_db.py        # Configuração MySQL
  extensions.py       # Instância do SQLAlchemy
dashboard/ (frontend)
  dashboard.html      # UI do dashboard
  css/style.css       # Estilos globais + dashboard
  js/dashboard.js     # Lógica de gráficos, filtros, exportações
PRD-exportacao.md     # Documento de requisitos (exportação)
requirements.txt      # Dependências Python
run.py                # Entry point (invoca create_app)
```

## Testes & Dicas
- O projeto não possui suite automatizada; recomenda-se testar manualmente:
  1. Criar cliente, filme e aluguel via frontend.
  2. Validar KPIs e gráficos mudando o período.
  3. Gerar exportações CSV/XLSX para ambos os tipos.
  4. Conferir atualização do histórico (inclui falhas).
- Para depurar o backend use `flask_app.logger.info(...)` ou breakpoint `pdb`.
- Em produção, use um servidor WSGI (Gunicorn/uwsgi) e configure variáveis de ambiente para credenciais de banco.

---
Qualquer dúvida ou sugestão abra uma issue/pull request. Bons estudos! :clapper:

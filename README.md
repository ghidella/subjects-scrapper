# 📚 Scraper de Disciplinas - Júpiter Web USP

Script Python para extrair informações de disciplinas da USP do sistema Júpiter Web.

## 🚀 Início Rápido

### 1. Instalar dependências

```bash
pip install requests beautifulsoup4
```

### 2. Editar as siglas

Abra `scraper_disciplinas.py` e edite a lista no início do arquivo:

```python
SIGLAS_DISCIPLINAS = [
    "ACH0021",
    "ACH0041",
    "ACH0141",
    # Adicione suas disciplinas aqui
]
```

### 3. Executar

```bash
python3 scraper_disciplinas.py
```

### 4. Escolher formatos

O script perguntará quais formatos você quer:

- `1` - JSON
- `2` - Markdown
- `3` - TXT
- Enter - todos os formatos

## � Pré-requisitos

- Python 3.6+
- Bibliotecas: `requests` e `beautifulsoup4`

## 📄 Arquivos Gerados

- `disciplinas_info.json` - Dados estruturados
- `disciplinas_info.md` - Formato legível
- `disciplinas_info.txt` - Texto simples

## 🔍 Informações Extraídas

Para cada disciplina:

- Nome e sigla
- Créditos e carga horária
- Ementa e objetivos
- Conteúdo programático
- Bibliografia
- Docentes responsáveis

## � Exemplo

```bash
$ python3 scraper_disciplinas.py

================================================================================
SCRAPER DE DISCIPLINAS - JÚPITER WEB USP
================================================================================

📋 Total de siglas a processar: 3
Siglas: ACH0021, ACH0041, ACH0141

Escolha os formatos (1-JSON, 2-MD, 3-TXT ou Enter para todos): 2

🔍 Iniciando scraping...

✅ 3 disciplinas processadas com sucesso!
📁 Arquivo gerado: disciplinas_info.md
```

## 🐛 Problemas Comuns

**Erro de instalação:**

```bash
pip3 install --user requests beautifulsoup4
```

**Python não encontrado:**

- Instale de [python.org](https://www.python.org/downloads/)

**Lista vazia:**

- Edite `SIGLAS_DISCIPLINAS` no arquivo .py

---

Desenvolvido para facilitar a coleta de informações acadêmicas da USP 🎓

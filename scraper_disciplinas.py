#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SCRAPER DE DISCIPLINAS - JÚPITER WEB USP
================================================================================

COMO USAR:
1. Instale as dependências: pip install requests beautifulsoup4
2. Edite a lista SIGLAS_DISCIPLINAS abaixo com suas disciplinas
3. Execute: python3 scraper_disciplinas.py
4. Escolha os formatos de saída (JSON, Markdown e/ou TXT)

================================================================================
"""

# ============================================================================
# CONFIGURE AQUI AS SIGLAS DAS DISCIPLINAS QUE VOCÊ QUER BUSCAR
# ============================================================================
SIGLAS_DISCIPLINAS = [
    "ACH0021",
    "ACH0041",
    "ACH0141",
    # Adicione mais siglas abaixo (uma por linha):
    # "ACH2003",
    # "MAC0110",
]
# ============================================================================

import sys
import json
import time
from typing import List, Dict, Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Erro: Dependências não instaladas!")
    print("\nPor favor, instale as dependências necessárias:")
    print("  pip install requests beautifulsoup4")
    print("\nOu com pip3:")
    print("  pip3 install requests beautifulsoup4")
    sys.exit(1)


class DisciplinaScraper:
    """Classe para fazer scraping de informações de disciplinas da USP."""
    
    BASE_URL = "https://uspdigital.usp.br/jupiterweb/obterDisciplina"
    
    def __init__(self, delay: float = 1.0):
        """
        Inicializa o scraper.
        
        Args:
            delay: Tempo de espera entre requisições (em segundos)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def obter_informacoes_disciplina(self, sigla: str) -> Optional[Dict]:
        """
        Obtém informações de uma disciplina específica.
        
        Args:
            sigla: Sigla da disciplina (ex: ACH2003)
            
        Returns:
            Dicionário com as informações da disciplina ou None se houver erro
        """
        try:
            url = f"{self.BASE_URL}?sgldis={sigla}"
            print(f"Buscando informações de {sigla}...")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair informações da disciplina
            info = {
                'sigla': sigla,
                'url': url,
                'dados': {}
            }
            
            # Título da disciplina
            titulo = soup.find('span', class_='titulo')
            if titulo:
                info['titulo'] = titulo.get_text(strip=True)
            
            # Buscar informações em tabelas
            tabelas = soup.find_all('table')
            
            for tabela in tabelas:
                linhas = tabela.find_all('tr')
                for linha in linhas:
                    colunas = linha.find_all('td')
                    if len(colunas) >= 2:
                        chave = colunas[0].get_text(strip=True).replace(':', '')
                        valor = colunas[1].get_text(strip=True)
                        if chave and valor:
                            info['dados'][chave] = valor
            
            # Buscar conteúdo programático
            programa = soup.find('div', class_='programa')
            if not programa:
                # Tentar encontrar por texto
                for elem in soup.find_all(['div', 'p', 'span']):
                    texto = elem.get_text(strip=True)
                    if 'Programa' in texto or 'Objetivos' in texto:
                        programa = elem
                        break
            
            if programa:
                info['programa'] = programa.get_text(strip=True)
            
            # Buscar todo o conteúdo da página como fallback
            corpo = soup.find('body')
            if corpo:
                info['conteudo_completo'] = corpo.get_text(separator='\n', strip=True)
            
            time.sleep(self.delay)  # Respeitar o delay entre requisições
            return info
            
        except requests.RequestException as e:
            print(f"Erro ao buscar {sigla}: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao processar {sigla}: {e}")
            return None
    
    def processar_lista_siglas(self, siglas: List[str]) -> List[Dict]:
        """
        Processa uma lista de siglas e obtém informações de todas.
        
        Args:
            siglas: Lista de siglas de disciplinas
            
        Returns:
            Lista com as informações de todas as disciplinas
        """
        resultados = []
        total = len(siglas)
        
        for idx, sigla in enumerate(siglas, 1):
            print(f"Processando {idx}/{total}: {sigla}")
            info = self.obter_informacoes_disciplina(sigla)
            if info:
                resultados.append(info)
        
        return resultados
    
    def salvar_json(self, dados: List[Dict], arquivo: str):
        """Salva os dados em formato JSON."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"\nDados salvos em {arquivo}")
    
    def salvar_markdown(self, dados: List[Dict], arquivo: str):
        """Salva os dados em formato Markdown."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("# Informações das Disciplinas\n\n")
            f.write(f"Total de disciplinas: {len(dados)}\n\n")
            f.write("---\n\n")
            
            for disc in dados:
                f.write(f"## {disc.get('sigla', 'N/A')}\n\n")
                
                if 'titulo' in disc:
                    f.write(f"**{disc['titulo']}**\n\n")
                
                if disc.get('dados'):
                    f.write("### Informações Gerais\n\n")
                    for chave, valor in disc['dados'].items():
                        f.write(f"- **{chave}**: {valor}\n")
                    f.write("\n")
                
                if 'programa' in disc:
                    f.write("### Programa\n\n")
                    f.write(f"{disc['programa']}\n\n")
                
                f.write(f"[Link para Júpiter Web]({disc['url']})\n\n")
                f.write("---\n\n")
        
        print(f"Dados salvos em {arquivo}")
    
    def salvar_txt(self, dados: List[Dict], arquivo: str):
        """Salva os dados em formato TXT."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("INFORMAÇÕES DAS DISCIPLINAS\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total de disciplinas: {len(dados)}\n\n")
            
            for disc in dados:
                f.write("=" * 80 + "\n")
                f.write(f"SIGLA: {disc.get('sigla', 'N/A')}\n")
                f.write("=" * 80 + "\n\n")
                
                if 'titulo' in disc:
                    f.write(f"{disc['titulo']}\n\n")
                
                if disc.get('dados'):
                    f.write("INFORMAÇÕES GERAIS:\n")
                    f.write("-" * 80 + "\n")
                    for chave, valor in disc['dados'].items():
                        f.write(f"{chave}: {valor}\n")
                    f.write("\n")
                
                if 'programa' in disc:
                    f.write("PROGRAMA:\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"{disc['programa']}\n\n")
                
                f.write(f"URL: {disc['url']}\n\n")
        
        print(f"Dados salvos em {arquivo}")


def escolher_formatos() -> Dict[str, bool]:
    """
    Permite ao usuário escolher quais formatos de arquivo deseja gerar.
    
    Returns:
        Dicionário com as escolhas do usuário para cada formato
    """
    print("=" * 80)
    print("ESCOLHA OS FORMATOS DE ARQUIVO PARA SALVAR")
    print("=" * 80)
    print("\nDigite suas escolhas separadas por vírgula (ou pressione Enter para todos):")
    print("  1 - JSON (formato estruturado para programação)")
    print("  2 - Markdown (formato legível e bem formatado)")
    print("  3 - TXT (formato texto simples)")
    print("\nExemplos: '1,2' ou '1' ou '2,3' ou apenas Enter para todos")
    
    escolha = input("\nSua escolha: ").strip()
    
    # Se não digitou nada, gerar todos
    if not escolha:
        return {'json': True, 'md': True, 'txt': True}
    
    # Processar escolha
    formatos = {'json': False, 'md': False, 'txt': False}
    
    try:
        opcoes = [int(x.strip()) for x in escolha.split(',')]
        if 1 in opcoes:
            formatos['json'] = True
        if 2 in opcoes:
            formatos['md'] = True
        if 3 in opcoes:
            formatos['txt'] = True
        
        if not any(formatos.values()):
            print("\n⚠️  Nenhum formato válido selecionado. Gerando todos os formatos...")
            return {'json': True, 'md': True, 'txt': True}
        
        return formatos
    except ValueError:
        print("\n⚠️  Opção inválida. Gerando todos os formatos...")
        return {'json': True, 'md': True, 'txt': True}


def main():
    """Função principal."""
    print("=" * 80)
    print("SCRAPER DE DISCIPLINAS - JÚPITER WEB USP")
    print("=" * 80)
    print()
    
    # Usar a lista global de siglas
    siglas = SIGLAS_DISCIPLINAS
    
    if not siglas:
        print("\n⚠️  ATENÇÃO: Lista de siglas está vazia!")
        print("Por favor, edite o script e adicione as siglas na variável SIGLAS_DISCIPLINAS.")
        print("A variável está no início do arquivo.\n")
        input("Pressione Enter para sair...")
        return
    
    print(f"📋 Total de siglas a processar: {len(siglas)}")
    print(f"Siglas: {', '.join(siglas)}\n")
    
    # Escolher formatos de saída
    formatos = escolher_formatos()
    print()
    
    # Criar scraper
    scraper = DisciplinaScraper(delay=1.0)
    
    # Processar disciplinas
    print("🔍 Iniciando scraping...\n")
    dados = scraper.processar_lista_siglas(siglas)
    
    if dados:
        print(f"\n✅ {len(dados)} disciplinas processadas com sucesso!\n")
        
        # Salvar nos formatos escolhidos
        arquivos_gerados = []
        
        if formatos['json']:
            scraper.salvar_json(dados, "disciplinas_info.json")
            arquivos_gerados.append("disciplinas_info.json (formato estruturado)")
        
        if formatos['md']:
            scraper.salvar_markdown(dados, "disciplinas_info.md")
            arquivos_gerados.append("disciplinas_info.md (formato Markdown)")
        
        if formatos['txt']:
            scraper.salvar_txt(dados, "disciplinas_info.txt")
            arquivos_gerados.append("disciplinas_info.txt (formato texto)")
        
        print("\n📁 Concluído! Arquivos gerados:")
        for arquivo in arquivos_gerados:
            print(f"  - {arquivo}")
        
        print("\n✨ Processo finalizado com sucesso!")
    else:
        print("\n❌ Nenhuma disciplina foi processada com sucesso.")
    
    print()
    try:
        input("Pressione Enter para sair...")
    except (EOFError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()

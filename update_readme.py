#!/usr/bin/env python3
"""
Script para automatizar o README.md com tabelas de projetos e commits
"""

import os
import subprocess
import json
import re
from datetime import datetime
import requests

class ReadmeUpdater:
    def __init__(self):
        # Usar username do ambiente ou padrão
        self.github_username = os.getenv('GITHUB_USERNAME', "tonybsilva")
        self.github_token = os.getenv('GITHUB_TOKEN')
        
    def get_recent_projects(self):
        """Busca os últimos 5 projetos do GitHub"""
        if not self.github_token:
            print("⚠️  GITHUB_TOKEN não configurada. Usando dados de exemplo.")
            return self.get_sample_projects()
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f"https://api.github.com/users/{self.github_username}/repos"
            params = {
                'sort': 'updated',
                'per_page': 5,
                'type': 'owner'
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            repos = response.json()
            projects = []
            
            for repo in repos:
                # Buscar stars
                stars_url = f"https://api.github.com/repos/{self.github_username}/{repo['name']}"
                stars_response = requests.get(stars_url, headers=headers)
                if stars_response.status_code == 200:
                    stars_data = stars_response.json()
                    stars = stars_data.get('stargazers_count', 0)
                else:
                    stars = 0
                
                # Determinar tecnologia principal
                language = repo.get('language', 'N/A')
                
                projects.append({
                    'name': repo['name'],
                    'technology': language,
                    'stars': stars,
                    'url': repo['html_url']
                })
            
            return projects
            
        except Exception as e:
            print(f"❌ Erro ao buscar projetos: {e}")
            return self.get_sample_projects()
    
    def get_sample_projects(self):
        """Retorna projetos de exemplo quando a API não está disponível"""
        return [
            {
                'name': 'Projeto Exemplo 1',
                'technology': 'Python',
                'stars': 15,
                'url': 'https://github.com/tonybsilva/projeto1'
            },
            {
                'name': 'Projeto Exemplo 2',
                'technology': 'JavaScript',
                'stars': 8,
                'url': 'https://github.com/tonybsilva/projeto2'
            },
            {
                'name': 'Projeto Exemplo 3',
                'technology': 'React',
                'stars': 12,
                'url': 'https://github.com/tonybsilva/projeto3'
            },
            {
                'name': 'Projeto Exemplo 4',
                'technology': 'Node.js',
                'stars': 6,
                'url': 'https://github.com/tonybsilva/projeto4'
            },
            {
                'name': 'Projeto Exemplo 5',
                'technology': 'Python',
                'stars': 20,
                'url': 'https://github.com/tonybsilva/projeto5'
            }
        ]
    
    def get_recent_commits(self):
        """Busca os últimos commits do repositório atual"""
        try:
            # Buscar commits locais
            result = subprocess.run(
                ['git', 'log', '--oneline', '-10'],
                capture_output=True,
                text=True,
                cwd='.'
            )
            
            if result.returncode == 0:
                commits = []
                lines = result.stdout.strip().split('\n')
                
                for line in lines[:5]:  # Apenas os últimos 5
                    if line.strip():
                        parts = line.split(' ', 1)
                        if len(parts) == 2:
                            hash_short = parts[0]
                            title = parts[1]
                            
                            # Criar link para o commit (assumindo GitHub)
                            # Tentar detectar o nome do repositório do git
                            repo_name = self.get_repo_name()
                            commit_url = f"https://github.com/{self.github_username}/{repo_name}/commit/{hash_short}"
                            
                            commits.append({
                                'hash': hash_short,
                                'title': title,
                                'url': commit_url
                            })
                
                return commits
            else:
                return self.get_sample_commits()
                
        except Exception as e:
            print(f"❌ Erro ao buscar commits: {e}")
            return self.get_sample_commits()
    
    def get_repo_name(self):
        """Detecta o nome do repositório atual"""
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                cwd='.'
            )
            
            if result.returncode == 0:
                remote_url = result.stdout.strip()
                # Extrair nome do repositório da URL
                if 'github.com' in remote_url:
                    repo_name = remote_url.split('/')[-1]
                    if repo_name.endswith('.git'):
                        repo_name = repo_name[:-4]
                    return repo_name
            
            # Fallback para o nome do diretório
            return os.path.basename(os.getcwd())
            
        except Exception:
            return os.path.basename(os.getcwd())
    
    def get_sample_commits(self):
        """Retorna commits de exemplo quando o git não está disponível"""
        return [
            {
                'hash': 'a1b2c3d',
                'title': 'feat: adiciona nova funcionalidade',
                'url': 'https://github.com/tonybsilva/repo/commit/a1b2c3d'
            },
            {
                'hash': 'e4f5g6h',
                'title': 'fix: corrige bug na validação',
                'url': 'https://github.com/tonybsilva/repo/commit/e4f5g6h'
            },
            {
                'hash': 'i7j8k9l',
                'title': 'docs: atualiza documentação',
                'url': 'https://github.com/tonybsilva/repo/commit/i7j8k9l'
            },
            {
                'hash': 'm0n1o2p',
                'title': 'refactor: melhora estrutura do código',
                'url': 'https://github.com/tonybsilva/repo/commit/m0n1o2p'
            },
            {
                'hash': 'q3r4s5t',
                'title': 'style: formata código',
                'url': 'https://github.com/tonybsilva/repo/commit/q3r4s5t'
            }
        ]
    
    def generate_projects_table(self, projects):
        """Gera a tabela de projetos no estilo especificado"""
        table = "| Nome | Tecnologia | Stars | Link |\n"
        table += "|------|------------|-------|------|\n"
        
        for project in projects:
            name = project['name']
            technology = project['technology']
            stars = project['stars']
            url = project['url']
            
            table += f"| {name} | {technology} | {stars} | [🔗]({url}) |\n"
        
        return table
    
    def generate_commits_table(self, commits):
        """Gera a tabela de commits no estilo especificado"""
        table = "| Hash | Título |\n"
        table += "|------|--------|\n"
        
        for commit in commits:
            hash_short = commit['hash']
            title = commit['title']
            url = commit['url']
            
            table += f"| {hash_short} | [{title}]({url}) |\n"
        
        return table
    
    def update_readme(self):
        """Atualiza o README.md com as novas tabelas"""
        try:
            # Ler o README atual
            with open('README.md', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar dados
            print("🔄 Buscando projetos recentes...")
            projects = self.get_recent_projects()
            
            print("🔄 Buscando commits recentes...")
            commits = self.get_recent_commits()
            
            # Gerar tabelas
            projects_table = self.generate_projects_table(projects)
            commits_table = self.generate_commits_table(commits)
            
            # Substituir marcadores
            content = re.sub(
                r'<!--PROJECTS-->.*?<!--PROJECTS-->',
                f'<!--PROJECTS-->\n{projects_table}\n<!--PROJECTS-->',
                content,
                flags=re.DOTALL
            )
            
            content = re.sub(
                r'<!--COMMITS-->.*?<!--COMMITS-->',
                f'<!--COMMITS-->\n{commits_table}\n<!--COMMITS-->',
                content,
                flags=re.DOTALL
            )
            
            # Adicionar timestamp de atualização
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            content = re.sub(
                r'(# 📊 Estatísticas)',
                f'\\1\n\n*Última atualização: {timestamp}*',
                content
            )
            

            
            # Salvar README atualizado
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ README.md atualizado com sucesso!")
            print(f"📊 {len(projects)} projetos adicionados")
            print(f"⏱ {len(commits)} commits adicionados")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar README: {e}")



def main():
    print("🚀 Iniciando atualização automática do README...")
    
    updater = ReadmeUpdater()
    updater.update_readme()
    
    print("\n💡 Dicas:")
    print("• Configure GITHUB_TOKEN para dados reais do GitHub")
    print("• Execute este script periodicamente para manter o README atualizado")
    print("• Personalize o username do GitHub no script se necessário")

if __name__ == "__main__":
    main()
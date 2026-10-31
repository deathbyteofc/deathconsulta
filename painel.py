import urllib.request
import json
import urllib.parse
import os
import random

APIKEY = "YjQcKvkukhOWfLbA6ck"

# Estilos de Cores e Temática Hacking / Gota de Sangue 🩸
VERMELHO_BG = "\033[41;1;37m"
VERMELHO = "\033[1;31m"
VERMELHO_ESCURO = "\033[0;31m"
BRANCO = "\033[1;37m"
CINZA = "\033[0;90m"
AMARELO = "\033[1;33m"
VERDE = "\033[1;32m"
RESET = "\033[0m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    limpar_tela()
    print(f"{VERMELHO_ESCURO}┌──────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{VERMELHO_ESCURO}│{RESET} {VERMELHO_BG}              DEATH CONSULTAS // PAINEL CLI                  {RESET} {VERMELHO_ESCURO}│{RESET}")
    print(f"{VERMELHO_ESCURO}├──────────────────────────────────────────────────────────────┤{RESET}")
    print(f"{VERMELHO_ESCURO}│{RESET} {CINZA}STATUS: CONEXÃO SEGURA{RESET} | {AMARELO}MODO: OSINT & FERRAMENTAS{RESET}    {VERMELHO_ESCURO}│{RESET}")
    print(f"{VERMELHO_ESCURO}└──────────────────────────────────────────────────────────────┘{RESET}\n")

def caixa_titulo(texto):
    print(f"\n{VERMELHO_ESCURO}╔{"═" * (len(texto) + 6)}╗{RESET}")
    print(f"{VERMELHO_ESCURO}║{RESET}  🩸 {VERMELHO}{texto}{RESET}  🩸  {VERMELHO_ESCURO}║{RESET}")
    print(f"{VERMELHO_ESCURO}╚{"═" * (len(texto) + 6)}╝{RESET}\n")

def item(rotulo, valor):
    print(f"  {VERMELHO}🩸 ├─►{RESET} {BRANCO}{rotulo:<20}:{RESET} {valor}")

# ==================== MÓDULO DE PUXADAS ====================
def consultar_cpf(cpf):
    print(f"\n{AMARELO}[⏳] Executando injeção e varredura na matriz para o CPF: {cpf}...{RESET}")
    url = f"http://node.tconect.xyz:1116/api/consulta/cpf/v6?apikey={APIKEY}&code={cpf}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") != "true":
                print(f"\n{VERMELHO_ESCURO}[!] FALHA DE RETORNO: {data.get('resposta', 'CPF não localizado')}{RESET}")
                return
            
            res = data.get("resultado", {})
            b = res.get("dadosBasicos", {})
            rg = res.get("rgHistorico", [{}])[0] if res.get("rgHistorico") else {}
            cnh = res.get("carteiraHabilitacao", [{}])[0] if res.get("carteiraHabilitacao") else {}
            poder = res.get("poderAquisitivo", {})
            
            caixa_titulo("DOSSIÊ DE IDENTIDADE (CPF)")
            item("Nome Completo", b.get('nome', 'N/D'))
            item("CPF", b.get('cpf', 'N/D'))
            item("Nascimento", f"{b.get('dataNasc', 'N/D')} ({b.get('idade', 'N/D')} anos)")
            item("Sexo / Est. Civil", f"{b.get('sexo', 'N/D')} / {b.get('estCivil', 'N/D')}")
            item("Escolaridade", b.get('escolaridade', 'N/D'))
            item("Nacionalidade", f"{b.get('nacionalidade', 'N/D')} ({b.get('naturalidade', 'N/D')})")
            item("Nome da Mãe", b.get('filiacao', {}).get('nomeMae', 'N/D'))
            item("Nome do Pai", b.get('filiacao', {}).get('nomePai', 'N/D'))

            caixa_titulo("DOCUMENTAÇÃO & FINANCEIRO")
            item("RG", f"{rg.get('registroGeral', 'N/D')} ({rg.get('orgaoEmissor', '')}/{rg.get('ufEmissao', '')})")
            item("CNH", f"{cnh.get('numeroRegistro', 'N/D')} (Cat: {cnh.get('categoriaAtual', 'N/D')})")
            item("Score Serasa", b.get('faixaScore', 'N/D'))
            item("Renda Estimada", f"R$ {b.get('rendaAtual', 'N/D')}")
            item("Poder Aquisitivo", f"{poder.get('poderAquisitivo', 'N/D')} ({poder.get('faixaRenda', '')})")

            caixa_titulo("INTERCEPTS DE CONTATO")
            for t in res.get("telefonesHistorico", []):
                item("Telefone", f"({t.get('ddd')}) {t.get('telefone')} | Operadora: {t.get('operadora', 'N/D')} ({t.get('tipo', 'N/D')})")
            for e in res.get("emails", []):
                item("E-mail", e.get('email'))

            caixa_titulo("LOCALIZAÇÃO PRINCIPAL")
            if res.get("enderecos"):
                end = res["enderecos"][0]
                end_str = f"{end.get('logradouro', '')}, Nº {end.get('numero', 'S/N')} - {end.get('bairro', '')}, {end.get('cidade', '')}/{end.get('siglaUf', '')} (CEP: {end.get('cep', '')})"
                link_mapa = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(end_str)}"
                item("Endereço", end_str)
                item("Google Maps", f"{VERDE}{link_mapa}{RESET}")

    except Exception as e:
        print(f"\n{VERMELHO_ESCURO}[!] ERRO DE CONEXÃO: {e}{RESET}")

def consultar_cnpj(cnpj):
    print(f"\n{AMARELO}[⏳] Executando varredura na matriz para o CNPJ: {cnpj}...{RESET}")
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            caixa_titulo("RELATÓRIO CADASTRAL (CNPJ)")
            item("Razão Social", data.get('razao_social', 'N/D'))
            item("Nome Fantasia", data.get('nome_fantasia', 'N/D'))
            item("CNPJ", data.get('cnpj', 'N/D'))
            item("Situação", data.get('descricao_situacao_cadastral', 'N/D'))
            item("Abertura", data.get('data_inicio_atividade', 'N/D'))
            item("Porte / Natureza", f"{data.get('porte', 'N/D')} / {data.get('natureza_juridica', 'N/D')}")
            item("Capital Social", f"R$ {data.get('capital_social', 'N/D')}")
            item("E-mail", data.get('email', 'N/D'))
            item("Telefone", data.get('ddd_telefone_1', 'N/D'))
            
            end_emp = f"{data.get('logradouro', '')}, Nº {data.get('numero', 'S/N')} - {data.get('bairro', '')}, {data.get('municipio', '')}/{data.get('uf', '')} (CEP: {data.get('cep', '')})"
            link_mapa = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(end_emp)}"
            item("Endereço Sede", end_emp)
            item("Google Maps", f"{VERDE}{link_mapa}{RESET}")

    except Exception as e:
        print(f"\n{VERMELHO_ESCURO}[!] ERRO DE CONEXÃO: {e}{RESET}")

def consultar_ip(ip):
    print(f"\n{AMARELO}[⏳] Executando varredura para o IP: {ip}...{RESET}")
    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,lat,lon,timezone,isp,org,as,query"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            caixa_titulo("RELATÓRIO DE REDE & GEOLOCALIZAÇÃO (IP)")
            item("Endereço IP", data.get('query', 'N/D'))
            item("Provedor (ISP)", data.get('isp', 'N/D'))
            item("Organização", data.get('org', 'N/D'))
            item("Autonomous System", data.get('as', 'N/D'))
            item("Localização", f"{data.get('city', 'N/D')} - {data.get('regionName', 'N/D')} / {data.get('country', 'N/D')}")
            item("Fuso Horário", data.get('timezone', 'N/D'))
            
            lat, lon = data.get('lat', 0), data.get('lon', 0)
            link_mapa = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            item("Google Maps IP", f"{VERDE}{link_mapa}{RESET}")

    except Exception as e:
        print(f"\n{VERMELHO_ESCURO}[!] ERRO DE CONEXÃO: {e}{RESET}")

def consultar_cep(cep):
    print(f"\n{AMARELO}[⏳] Executando varredura para o CEP: {cep}...{RESET}")
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            caixa_titulo("RELATÓRIO DE ENDEREÇAMENTO (CEP)")
            item("CEP", data.get('cep', 'N/D'))
            item("Logradouro", data.get('logradouro', 'N/D'))
            item("Bairro", data.get('bairro', 'N/D'))
            item("Cidade / UF", f"{data.get('localidade', 'N/D')} / {data.get('uf', 'N/D')}")
            item("DDD Local", f"({data.get('ddd', 'N/D')})")
            item("Código IBGE", data.get('ibge', 'N/D'))
            
            end_cep = f"{data.get('logradouro', '')}, {data.get('bairro', '')} - {data.get('localidade', '')}/{data.get('uf', '')}, {data.get('cep', '')}"
            link_mapa = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(end_cep)}"
            item("Google Maps CEP", f"{VERDE}{link_mapa}{RESET}")

    except Exception as e:
        print(f"\n{VERMELHO_ESCURO}[!] ERRO DE CONEXÃO: {e}{RESET}")

# ==================== MÓDULO DE GERADOR ====================
def gerar_cpf_valido():
    digitos = [random.randint(0, 9) for _ in range(9)]
    
    # Primeiro dígito verificador
    soma = sum(digitos[i] * (10 - i) for i in range(9))
    resto = soma % 11
    d1 = 0 if resto < 2 else 11 - resto
    digitos.append(d1)
    
    # Segundo dígito verificador
    soma = sum(digitos[i] * (11 - i) for i in range(10))
    resto = soma % 11
    d2 = 0 if resto < 2 else 11 - resto
    digitos.append(d2)
    
    cpf_gerado = "".join(map(str, digitos))
    cpf_formatado = f"{cpf_gerado[:3]}.{cpf_gerado[3:6]}.{cpf_gerado[6:9]}-{cpf_gerado[9:]}"
    return cpf_formatado

def menu_gerador():
    while True:
        banner()
        caixa_titulo("MÓDULO GERADOR DE DADOS")
        print(f"  {VERMELHO}🩸 [1]{RESET} {BRANCO}Gerar CPF Válido{RESET}")
        print(f"  {VERMELHO}🩸 [0]{RESET} {CINZA}Voltar ao Menu Principal{RESET}\n")
        
        op = input(f"{VERMELHO_ESCURO}ESCOLHA UMA OPÇÃO ──► {RESET}").strip()
        if op == '1':
            cpf_f = gerar_cpf_valido()
            print(f"\n  {VERMELHO}🩸 CPF Gerado:{RESET} {VERDE}{cpf_f}{RESET}")
            input(f"\n{CINZA}Pressione [ENTER] para gerar outro...{RESET}")
        elif op == '0':
            break

# ==================== MÓDULO DE MÉTODO TRAVAZAP ====================
def exibir_metodo_travazap():
    banner()
    caixa_titulo("MÉTODO & SCRIPTS DE TRAVAZAP (ANDROID / iPHONE)")
    print(f"""{BRANCO}
 [!] INFORMAÇÕES TÉCNICAS E CONCEITUAIS:

 O "Travazap" consiste no envio de sequências massivas de caracteres 
 especiais invisíveis, blocos Unicode corrompidos ou payloads binários 
 excessivamente longos que sobrecarregam o buffer de processamento do 
 aplicativo WhatsApp do alvo.

 ──► PARA ANDROID:
  • Android possui um motor de renderização de texto mais flexível, 
    porém a persistência de payloads longos em arquivos de banco de 
    dados locais (SQLite) causa congelamento do launcher e loop de crashes.
  • Método: Envio via Termux usando requisições automatizadas ou scripts 
    Python em loop com Baileys/Selenium injetando strings corrompidas.

 ──► PARA iPHONE (iOS):
  • O iOS possui alta rigidez no gerenciamento de memória da API gráfica, 
    fazendo com que caracteres Unicode específicos (como fontes em árabe, 
    tibetano ou caracteres zero-width combinados) estourem a pilha de 
    execução do framework CoreText, forçando o Respring ou travamento total.
  • Método: Payload Unicode em texto compactado enviado diretamente pelo chat.

 [⚠️ AVISO OPERACIONAL]: O uso de scripts de travamento viola os termos de 
 serviço da plataforma e pode resultar no banimento imediato do número.
{RESET}""")
    input(f"\n{CINZA}Pressione [ENTER] para voltar ao menu principal...{RESET}")

# ==================== MENU PRINCIPAL ====================
def main():
    while True:
        banner()
        print(f"  {VERMELHO}🩸 [1]{RESET} {BRANCO}MÓDULO DE PUXADAS (CPF / CNPJ / IP / CEP){RESET}")
        print(f"  {VERMELHO}🩸 [2]{RESET} {BRANCO}MÓDULO GERADOR DE DADOS (CPF VÁLIDO){RESET}")
        print(f"  {VERMELHO}🩸 [3]{RESET} {BRANCO}MÉTODO & SCRIPTS TRAVAZAP (ANDROID / iPHONE){RESET}")
        print(f"  {VERMELHO}🩸 [0]{RESET} {CINZA}SAIR{RESET}\n")
        
        opcao = input(f"{VERMELHO_ESCURO}SELECIONE O MÓDULO ──► {RESET}").strip()
        
        if opcao == '1':
            while True:
                banner()
                caixa_titulo("MÓDULO DE PUXADAS OSINT")
                print(f"  {VERMELHO}🩸 [1]{RESET} {BRANCO}Puxar CPF{RESET}")
                print(f"  {VERMELHO}🩸 [2]{RESET} {BRANCO}Puxar CNPJ{RESET}")
                print(f"  {VERMELHO}🩸 [3]{RESET} {BRANCO}Puxar IP{RESET}")
                print(f"  {VERMELHO}🩸 [4]{RESET} {BRANCO}Puxar CEP{RESET}")
                print(f"  {VERMELHO}🩸 [0]{RESET} {CINZA}Voltar{RESET}\n")
                
                sub = input(f"{VERMELHO_ESCURO}SELECIONE O ALVO ──► {RESET}").strip()
                if sub == '1':
                    v = input(f"\n{BRANCO}INFORME O CPF (SOMENTE NÚMEROS): {RESET}").strip()
                    if v: consultar_cpf(v)
                    input(f"\n\n{CINZA}Pressione [ENTER] para continuar...{RESET}")
                elif sub == '2':
                    v = input(f"\n{BRANCO}INFORME O CNPJ (SOMENTE NÚMEROS): {RESET}").strip()
                    if v: consultar_cnpj(v)
                    input(f"\n\n{CINZA}Pressione [ENTER] para continuar...{RESET}")
                elif sub == '3':
                    v = input(f"\n{BRANCO}INFORME O IP: {RESET}").strip()
                    if v: consultar_ip(v)
                    input(f"\n\n{CINZA}Pressione [ENTER] para continuar...{RESET}")
                elif sub == '4':
                    v = input(f"\n{BRANCO}INFORME O CEP: {RESET}").strip()
                    if v: consultar_cep(v)
                    input(f"\n\n{CINZA}Pressione [ENTER] para continuar...{RESET}")
                elif sub == '0':
                    break
        elif opcao == '2':
            menu_gerador()
        elif opcao == '3':
            exibir_metodo_travazap()
        elif opcao == '0':
            print(f"\n{VERMELHO}🩸 Encerrando sessão...{RESET}")
            break
        else:
            print(f"\n{VERMELHO_ESCURO}Opção inválida!{RESET}")
            input(f"\n{CINZA}Pressione [ENTER] para continuar...{RESET}")

if __name__ == "__main__":
    main()

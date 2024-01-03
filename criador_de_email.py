from openai import OpenAI
import openai
import dotenv
import time
import json

dotenv.load_dotenv()
client = OpenAI()

def gerador_de_perfil(lista_de_compras_por_cliente):
    print("1. Iniciando gerador de perfil")
    prompt_sistema = """
    Você é um identificador de perfil de compra.
    Identifique o perfil para cada cliente a seguir.

    O formato de saída deve ser em JSON:

    {
        "clientes": [
            {
                "nome": "nome do cliente",
                "perfil": "descreva o perfil do cliente em 3 palavras"
            }
        ]
    }
    """

    tentativas = 0
    tempo_de_espera = 5
    while tentativas < 3:
        tentativas += 1
        print(f"Tentativa: {tentativas}")
        try:
            resposta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                {
                    "role": "system",
                    "content": prompt_sistema
                },
                {
                    "role": "user",
                    "content": lista_de_compras_por_cliente
                }
                ]
            )

            conteudo = resposta.choices[0].message.content
            json_resultado = json.loads(conteudo)
            print("1. Finalizou identificação de perfis")
            return json_resultado
        except openai.AuthenticationError as e:
            print(f"Erro de autenticacao: {e}")
        except openai.APIError as e:
            print(f"Erro de API: {e}")
            time.sleep(5)
        except openai.RateLimitError as e:
            print(f"Erro de limite de taxa: {e}")
            time.sleep(tempo_de_espera)
            tempo_de_espera *= 2

def recomendador_de_produtos(perfil, lista_de_produtos):
    print("2. Iniciando recomendacao")
    prompt_sistema = f"""
    Você é um recomendador de produtos.
    A partir de um perfil, recomende 3 produtos para um cliente.

    #### Pefil
    {perfil}

    #### Lista de produtos
    {lista_de_produtos}
    
    #### Saída
    3 nomes de produtos em bullets points
    """

    tentativas = 0
    tempo_de_espera = 5
    while tentativas < 3:
        tentativas += 1
        print(f"Tentativa: {tentativas}")
        try:
            resposta = client.chat.completions.create(
               model = "gpt-3.5-turbo",
               messages = [
                   {
                       "role": "system",
                       "content": prompt_sistema
                   }
              ]
            )
            print("Finaliza recomendacao")
            return resposta.choices[0].message.content
        except openai.AuthenticationError as e:
            print(f"Erro de autenticacao: {e}")
        except openai.APIError as e:
            print(f"Erro de API: {e}")
            time.sleep(5)
        except openai.RateLimitError as e:
            print(f"Erro de limite de taxa: {e}")
            time.sleep(tempo_de_espera)
            tempo_de_espera *= 2

def escreve_email(produtos):
    print("3. Escrevendo email de recomendacao")

    prompt_sistema = f"""
    Você é um gerador de email que recomenda produtos a clientes.
    Use uma linguagem mais natural, não tão descontraída mas nem tão formal.
    Faça sugestões sobre o produto e sempre deixe claro suas vantagens.

    A saída deve ser no máximo de 3 parágrafos.

    #### Produtos que devem ser recomendados
    {produtos}
    """

    tentativas = 0
    tempo_de_espera = 5
    while tentativas < 3:
        tentativas += 1
        print(f"Tentativa: {tentativas}")
        try:
            resposta = client.chat.completions.create(
               model = "gpt-3.5-turbo",
               messages = [
                   {
                       "role": "system",
                       "content": prompt_sistema
                   }
              ]
            )
            print("Finaliza recomendacao")
            return resposta.choices[0].message.content
        except openai.AuthenticationError as e:
            print(f"Erro de autenticacao: {e}")
        except openai.APIError as e:
            print(f"Erro de API: {e}")
            time.sleep(5)
        except openai.RateLimitError as e:
            print(f"Erro de limite de taxa: {e}")
            time.sleep(tempo_de_espera)
            tempo_de_espera *= 2

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

lista_de_produtos = carrega("./dados/lista_de_produtos.txt")
lista_de_compras_por_cliente = carrega("./dados/lista_de_compras_10_clientes.csv")
perfis = gerador_de_perfil(lista_de_compras_por_cliente)

for cliente in perfis["clientes"]:
    nome_do_cliente = cliente["nome"]
    print(f"Iniciando recomendação para o cliente {nome_do_cliente}")
    produtos = recomendador_de_produtos(cliente["perfil"], lista_de_produtos)
    email = escreve_email(produtos)
    salva(f"./email/email-{nome_do_cliente}.txt", email)

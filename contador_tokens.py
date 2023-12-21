from openai import OpenAI
import dotenv
import tiktoken

dotenv.load_dotenv()
client = OpenAI()
codificador = tiktoken.encoding_for_model("gpt-3.5-turbo")

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")


prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_usuario = carrega("./dados/lista_de_compras_10_clientes.csv")
lista_tokens = codificador.encode(prompt_sistema + prompt_usuario)
modelo = "gpt-3.5-turbo"
numero_tokens_resposta = 256

if len(lista_tokens) >= 4096 - numero_tokens_resposta:
    modelo = "gpt-3.5-turbo-16k"

print(f"Numero de tokens na entrada: {len(lista_tokens)}")
print(f"Modelo: {modelo}")

resposta = client.chat.completions.create(
  model= modelo,
  messages=[
    {
      "role": "system",
      "content": prompt_sistema
    },
    {
      "role": "user",
      "content": prompt_usuario
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(resposta.choices[0].message.content)
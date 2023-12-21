from openai import OpenAI
import dotenv

def categorizador_produtos(nome_produto, categorias):
    prompt = f"""
    Você é um categorizador de produtos.
    Deve dizer apenas qual é a categoria de produtos, se não souber informar que: "Não posso te ajudar"
    ### Lista de categorias
    {categorias}
    ### Exemplo de saída
    Esporte
    Beleza
    """

    resposta = client.chat.completions.create(
        model = "gpt-3.5-turbo-16k",
        messages = [
            {
                "role" : "system",
                "content" : prompt
            },
            {
                "role" : "user",
                "content" : nome_produto
            }
        ]
    )

    print(resposta.choices[0].message.content)

    
dotenv.load_dotenv()
client = OpenAI()
categorias = input("Digite as categorias de produtos: ")

while True:
    nome_produto = input("Digite o nome do produto: ")
    categorizador_produtos(nome_produto=nome_produto, categorias=categorias)    
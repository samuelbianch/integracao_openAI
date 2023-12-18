from openai import OpenAI
import dotenv

client = OpenAI()

client.chat.completions.create(
    model = "gpt-3.5-turbo-16k",
    messages = [
        {
            "role" : "system",
            "content" : "Gere nomes de produtos fictícios sem descrição de acordo com a requisição do usuário."
        },
        {
            "role" : "user",
            "content" : "Gere 5 produtos"
        }
    ]
)
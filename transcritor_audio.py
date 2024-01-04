from openai import OpenAI
from PIL import Image
import os, shutil, dotenv, requests, time
from instabot import Bot

def postar_com_instabot(usuario, senha, imagem, legenda):
    print("Iniciando postagem no instagram ...")

    if os.path.exists("config"):
        shutil.rmtree("config")

    bot = Bot()
    bot.login(username=usuario, password=senha)
    
    try:
        bot.upload_photo(imagem, caption=legenda)
        #time.sleep(30) # pausa de 30 segundos entre postagens
    except ConnectionAbortedError as e:
        print(f"Erro ao publicar non instagram: {e}")

def selecionar_imagem(nome_arquivo):
    opcao = int(input("Qual imagem você deseja selecionar, informe o número do sufixo da imagem gerada? "))
    if opcao < 0 or opcao > 3:
        opcao = 0
    return f"./images/{nome_arquivo}_{opcao}.png"

def ferramenta_converter_png_para_jpg(caminho_imagem_escolhida):
    img_png = Image.open(caminho_imagem_escolhida)
    img_png.save(f"{caminho_imagem_escolhida.split(".")[0]}.jpg")
    return f"{caminho_imagem_escolhida.split(".")[0]}.jpg"

def confirmar_postagem(caminho_imagem_convertida, legenda_postagem):
    print(f"\nCaminho Imagem: {caminho_imagem_convertida}")
    print(f"\nLegenda: {legenda_postagem}")
    print("\n\nDeseja postar os dados acima no seu instagram? Digite 's' para sim e 'n' para não.")
    return input()

def trancritor_audio(caminho_audio, nome_arquivo, client):
    print("Escrevendo com o Whispers ...")

    audio = open(caminho_audio, "rb")

    resposta = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )

    with open(f"./audio/saida_{nome_arquivo}.txt", "w", encoding='utf-8') as saida:
        saida.write(resposta.text)

    return resposta.text

def byte_to_string(texto):
    if isinstance(texto, byte):
        return str(texto)
    else:
        return texto
    
def leitor_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "rb") as arquivo:
            return arquivo.read()
    except IOError as e:
        return f"Erro ao ler arquivo {e}"

def resumo_instagram_gpt(transcricao_completa, nome_arquivo, client):
    print("Gerando resumo/legenda do Instagram ...")

    prompt_sistema = """
    Você é um gerador de legendas do instagram, para influencers turbinarem seus posts.

    A legenda deve conter as seguintes observações:
    - Uma linguagem jovial
    - Deve ser ecrita em Postugês do Brasil
    - Pode conter emojis
    - Não deve ser maior do que 50 palavras
    """

    prompt_usuario = f"""
    Esta é a transcrição do podcast: {transcricao_completa}.
    Gere uma legenda para o instagram, com essa transcrição.
    """
    resposta = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {
                        "role": "system",
                        "content": prompt_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt_usuario
                    }
                ]
    )

    with open(f"audio/saida_instagram_{nome_arquivo}.txt", "w", encoding='utf-8') as saida:
        saida.write(resposta.choices[0].message.content)

    return resposta.choices[0].message.content

def gerador_hashtag_gpt(resumo_instagram, nome_arquivo, client):
    print("Gerando as hashtags ...")

    prompt_sistema = f"""
    Você é um analisador de legenda e criador de hashtag para o instagram.
    A entrada é uma legenda de instagram.
    A saíde deve conter 5 hashtags sobre o assunto da legenda.
    """

    prompt_usuario = f"""
    De acordo com a legenda: {resumo_instagram}.
    Gere 5 hashtags.
    """

    resposta = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {
                        "role": "system",
                        "content": prompt_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt_usuario
                    }
                ]
    )

    with open(f"audio/saida_hashtags_{nome_arquivo}.txt", "w", encoding='utf-8') as saida:
        saida.write(resposta.choices[0].message.content)

    return resposta.choices[0].message.content

def geraror_texto_para_imagem_gpt(resumo_instagram, nome_arquivo, client):
    print("Gerando texto para a geração de imagem ...")

    prompt_sistema = """
    Você é um gerador de texto para a criação de imagens.
    Você deve ler um texto e criar um texto para uma API criar uma imagem baseada no texto.

    #### Entrada
    Um resumo de um texto com os princípais pontos que a imagem deve conter

    #### Saída
    A saída não pode conter caracteres especiais.
    Deve ser um texto simples para a geração de uma imagem, a partir da entrada.
    """

    prompt_usuario = f"Gere um texto para a criação da imagem com o seguinte resumo: {resumo_instagram}"

    resposta = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {
                        "role": "system",
                        "content": prompt_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt_usuario
                    }
                ]
    )

    with open(f"audio/saida_texto_para_imagem_{nome_arquivo}.txt", "w", encoding='utf-8') as saida:
        saida.write(resposta.choices[0].message.content)

    return resposta.choices[0].message.content

def ferramenta_download_imagem(nome_arquivo, imagem_gerada, qtd_imagens):
  lista_nome_imagens = []
  try:
    for contador_imagens in range(0,qtd_imagens):
        caminho = imagem_gerada[contador_imagens].url
        imagem = requests.get(caminho)

        with open(f"{nome_arquivo}_{contador_imagens}.png", "wb") as arquivo_imagem:
            arquivo_imagem.write(imagem.content)

        lista_nome_imagens.append(f"{nome_arquivo}_{contador_imagens}.png")
    return lista_nome_imagens
  except:
    print("Ocorreu um erro!")
    return  None

def gerador_imamgem_dalle(resolucao, texto_para_imagem, client, qtd):
    print("Gerando imagem na ferramenta DALL-E ...")

    prompt = f"Uma pintura ultra futurista, textless, 3d que retrate: {texto_para_imagem}"

    resposta = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size=resolucao,
        quality="standard",
        n=qtd,
    )

    return resposta.data

def main():
    dotenv.load_dotenv()
    client = OpenAI()

    caminho_audio = "./audio/podcast_IA.mp3"
    nome_arquivo = "podcast_IA"
    url = ""
    resolucao = "1024x1024"
    qtd_imagens = 4

    user_instagram = os.getenv("INSTAGRAM_USER")
    password_instagram = os.getenv("INSTAGRAM_PASS")

    ## Consumindo a API
    # transcricao_completa = trancritor_audio(caminho_audio, nome_arquivo, client)
    # resumo_instagram = resumo_instagram_gpt(transcricao_completa, nome_arquivo, client)
    # hashtags = gerador_hashtag_gpt(resumo_instagram, nome_arquivo, client)
    # texto_para_imagem = geraror_texto_para_imagem_gpt(resumo_instagram, nome_arquivo, client)
    
    # Lendo os arquivos locais
    #transcricao_completa = leitor_arquivo("./audio/saida_podcast_IA.txt")
    resumo_instagram = leitor_arquivo("./audio/saida_instagram_podcast_IA.txt")
    hashtags = leitor_arquivo("./audio/saida_hashtags_podcast_IA.txt")
    texto_para_imagem = leitor_arquivo("./audio/saida_texto_para_imagem_podcast_IA.txt")
    lista_imagens = gerador_imamgem_dalle(resolucao, texto_para_imagem, client, qtd_imagens)
    
    ferramenta_download_imagem(f"./images/{nome_arquivo}", lista_imagens, qtd_imagens)

    #print("Lista imagens geradas: ", lista_imagens)
    imagem_escolhida = selecionar_imagem(nome_arquivo)
    
    imagem_convertida = ferramenta_converter_png_para_jpg(imagem_escolhida)

    legenda_convertida = f"{byte_to_string(resumo_instagram)}\nLink: {byte_to_string(url)}\n{byte_to_string(hashtags)}"

    if confirmar_postagem(imagem_convertida, legenda_convertida).lower() == 's':
        postar_com_instabot(user_instagram, password_instagram)


    
if __name__ == '__main__':
    main()
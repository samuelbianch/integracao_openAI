from openai import OpenAI
import dotenv

def trancritor_audio(caminho_audio, nome, client):
    print("Escrevendo com o Whispers ...")

    audio = open(caminho_audio, "rb")

    resposta = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )

    return resposta.text

def main():
    dotenv.load_dotenv()
    client = OpenAI()

    caminho_audio = "./audio/memoria.mp3"
    nome_arquivo = "memoria"
    url = ""

    transcricao_completa = trancritor_audio(caminho_audio, nome_arquivo, client)

    with open(f"./audio/saida_{nome_arquivo}.txt", "w", encoding='utf-8') as saida:
        saida.write(transcricao_completa)

if '__main__':
    main()
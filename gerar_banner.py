import asyncio
from PIL import Image, ImageDraw, ImageFont
from telegram import Bot
from telegram.error import TelegramError

TOKEN = 'SEU TOKEN AQUI'
CHAT_ID = SEU CHAT_ID AQUI.

bot = Bot(token=TOKEN)


async def enviar_banner(caminho_imagem, mensagem=None):
    try:
        with open(caminho_imagem, 'rb') as img:
            await bot.send_photo(chat_id=CHAT_ID, photo=img)
            if mensagem:
                await bot.send_message(chat_id=CHAT_ID, text=mensagem)
        print("✅ Banner e mensagem enviados com sucesso!")
    except TelegramError as e:
        print(f"❌ Erro ao enviar: {e}")
    except FileNotFoundError:
        print("❌ Arquivo de imagem não encontrado")


def gerar_banner(dados, cor_texto="black", cor_fundo=None):
    try:
        # Carrega imagem base
        imagem = Image.open("base_banner.png").convert("RGBA")

        # Se cor_fundo for especificada, cria um fundo colorido
        if cor_fundo:
            fundo = Image.new('RGBA', imagem.size, cor_fundo)
            imagem = Image.alpha_composite(fundo, imagem)

        desenhador = ImageDraw.Draw(imagem)

        # Carrega fontes (com fallback caso a fonte não exista)
        try:
            fonte_grande = ImageFont.truetype("BebasNeue-Regular.ttf", 80)
            fonte_media = ImageFont.truetype("BebasNeue-Regular.ttf", 40)
        except:
            fonte_grande = ImageFont.load_default()
            fonte_media = ImageFont.load_default()
            print("⚠️ Usando fonte padrão - verifique se as fontes estão instaladas")

        largura_img, _ = imagem.size

        def centralizar_texto(texto, fonte, y, cor=cor_texto):
            caixa = desenhador.textbbox((0, 0), texto, font=fonte)
            largura_texto = caixa[2] - caixa[0]
            x = (largura_img - largura_texto) // 2
            desenhador.text((x, y), texto, font=fonte, fill=cor)

        # Adiciona textos centralizados
        centralizar_texto(f"{dados['time_casa']} {dados['placar_casa']}", fonte_grande, 380)
        centralizar_texto(f"{dados['time_fora']} {dados['placar_fora']}", fonte_grande, 480)
        centralizar_texto(f"{dados['data']} - {dados['horario']}", fonte_media, 580)

        # Salva a imagem
        nome_arquivo = f"banner_{dados['time_casa'].replace(' ', '_')}_vs_{dados['time_fora'].replace(' ', '_')}.png"
        imagem.save(nome_arquivo)
        print(f"✅ Banner gerado: {nome_arquivo}")

        return nome_arquivo

    except Exception as e:
        print(f"❌ Erro ao gerar banner: {e}")
        return None


async def main():
    # Dados do jogo
    dados_jogo = {
        "time_casa": "Real Madrid",
        "time_fora": "Barcelona",
        "placar_casa": 2,
        "placar_fora": 1,
        "horario": "15:00",
        "data": "11/06/2025"
    }

    # Mensagem que será enviada junto com o banner
    mensagem_grupo = "⚽ Partida emocionante hoje! ⚽\n\nNão percam o jogo entre {} vs {}!".format(
        dados_jogo['time_casa'], dados_jogo['time_fora'])

    # Gera e envia o banner
    nome_arquivo = gerar_banner(dados_jogo, cor_texto="white", cor_fundo="#1a3e72")
    if nome_arquivo:
        await enviar_banner(nome_arquivo, mensagem=mensagem_grupo)

    # Mensagem de confirmação
    await bot.send_message(chat_id=CHAT_ID, text="✅ Bot está ativo e funcionando!")


if __name__ == "__main__":
    asyncio.run(main())

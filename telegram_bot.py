from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from PIL import Image, ImageDraw, ImageFont
import logging
import os
import asyncio

# Configuração básica
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configurações do banner (MODIFIQUE AQUI)
CHAT_ID = -1002841860609  # ID do seu grupo
TOKEN = "7642062953:AAEcofpmtP1KLWOQI20zmsbEYahZkKbk6Oo"  # Token do seu bot

# Dados do banner (personalize)
DADOS_BANNER = {
    'time_casa': 'Real Madrid',
    'time_fora': 'Barcelona',
    'placar_casa': 2,
    'placar_fora': 1,
    'data': '25/06/2025',
    'horario': '20:00'
}


def criar_banner(dados):
    """Cria a imagem do banner"""
    try:
        # Cria imagem (800x600 pixels)
        img = Image.new('RGB', (800, 600), color='#1a3e72')
        draw = ImageDraw.Draw(img)

        # Carrega fontes (substitua pelas suas)
        try:
            fonte_grande = ImageFont.truetype("arialbd.ttf", 60)
            fonte_pequena = ImageFont.truetype("arial.ttf", 30)
        except:
            fonte_grande = ImageFont.load_default()
            fonte_pequena = ImageFont.load_default()

        # Textos do banner
        draw.text((200, 100), f"{dados['time_casa']} {dados['placar_casa']}",
                  font=fonte_grande, fill="white")
        draw.text((200, 200), f"{dados['time_fora']} {dados['placar_fora']}",
                  font=fonte_grande, fill="white")
        draw.text((200, 300), f"{dados['data']} - {dados['horario']}",
                  font=fonte_pequena, fill="yellow")

        # Salva temporariamente
        img.save("banner_temp.png")
        return "banner_temp.png"

    except Exception as e:
        logger.error(f"Erro ao criar banner: {e}")
        return None


async def enviar_banner_automatico(context: ContextTypes.DEFAULT_TYPE):
    """Envia o banner automaticamente"""
    try:
        banner_path = criar_banner(DADOS_BANNER)
        if banner_path:
            with open(banner_path, 'rb') as banner:
                await context.bot.send_photo(
                    chat_id=CHAT_ID,
                    photo=banner,
                    caption="⚽ Partida do Dia! ⚽"
                )
            os.remove(banner_path)  # Limpa o arquivo temporário
            logger.info("Banner enviado com sucesso!")
    except Exception as e:
        logger.error(f"Falha ao enviar banner: {e}")


async def on_startup(app):
    """Executa quando o bot inicia"""
    await app.bot.send_message(
        chat_id=CHAT_ID,
        text="🤖 Bot iniciado! Enviando banner..."
    )
    await enviar_banner_automatico(app)


def main():
    app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

    logger.info("Iniciando bot...")
    app.run_polling()


if __name__ == "__main__":
    main()
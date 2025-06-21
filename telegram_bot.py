from telegram.ext import ApplicationBuilder, ContextTypes
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

# Configurações
CHAT_ID = -1002841860609  # ID do grupo
TOKEN = "7642062953:AAEcofpmtP1KLWOQI20zmsbEYahZkKbk6Oo"  # Token do bot

# Dados do banner
DADOS_BANNER = {
    'time_casa': 'Real Madrid',
    'time_fora': 'Barcelona',
    'placar_casa': 2,
    'placar_fora': 1,
    'data': '25/06/2025',
    'horario': '20:00'
}


def criar_banner(dados):
    """Cria a imagem do banner com fundo personalizado"""
    try:
        # Carrega o fundo
        fundo = Image.open('base_banner.png').convert('RGBA')
        img = fundo.copy()

        draw = ImageDraw.Draw(img)

        # Fontes
        try:
            fonte_grande = ImageFont.truetype("arialbd.ttf", 70)  # Fonte maior pra destacar
            fonte_pequena = ImageFont.truetype("arial.ttf", 40)
        except:
            fonte_grande = ImageFont.load_default()
            fonte_pequena = ImageFont.load_default()

        # Cores
        cor_texto = "black"  # Texto preto pra fundo claro
        cor_destaque = "darkred"  # Cor diferente pra horário ou data, se quiser destacar

        # Adiciona textos no banner (ajustado mais pra baixo)
        draw.text((330, 400), f"{dados['time_casa']} {dados['placar_casa']}",
                  font=fonte_grande, fill=cor_texto)
        draw.text((330, 490), f"{dados['time_fora']} {dados['placar_fora']}",
                  font=fonte_grande, fill=cor_texto)
        draw.text((330, 600), f"{dados['data']} - {dados['horario']}",
                  font=fonte_pequena, fill=cor_destaque)

        # Salva temporariamente
        output_path = "banner_temp.png"
        img.convert('RGB').save(output_path)
        return output_path

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
            os.remove(banner_path)
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

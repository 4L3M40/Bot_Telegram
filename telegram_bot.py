from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
from PIL import Image, ImageDraw, ImageFont
import logging
import os

# Configurações do bot
TOKEN = "SEU TOKEN AQUI"  # ⚠️ Coloque seu token aqui
CHAT_ID = SEU CHAT_ID AQUI  # ✅ ID do grupo onde o banner será postado

# Configuração do log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dados iniciais do banner
DADOS_BANNER = {
    'time_casa': 'Real Madrid',
    'time_fora': 'Barcelona',
    'placar_casa': 2,
    'placar_fora': 1,
    'data': '25/06/2025',
    'horario': '20:00'
}

# 📦 Função para criar o banner
def criar_banner(dados):
    try:
        # Carregar fundo
        fundo = Image.open('base_banner.png').convert('RGBA')
        img = fundo.copy()

        draw = ImageDraw.Draw(img)

        # Carregar fontes
        try:
            fonte_grande = ImageFont.truetype("BebasNeue-Regular.ttf", 80)
            fonte_media = ImageFont.truetype("BebasNeue-Regular.ttf", 40)
        except:
            fonte_grande = ImageFont.load_default()
            fonte_media = ImageFont.load_default()

        largura_img, _ = img.size

        # Inserir logos
        for idx, time in enumerate(['time_casa', 'time_fora']):
            logo_path = f'logos/{dados[time].replace(" ", "_")}.png'
            if os.path.exists(logo_path):
                logo = Image.open(logo_path).convert("RGBA")
                logo = logo.resize((150, 150))
                pos_x = 150 if idx == 0 else largura_img - 300
                img.paste(logo, (pos_x, 50), logo)

        # Centraliza textos
        def centralizar_texto(texto, fonte, y, cor="black"):
            caixa = draw.textbbox((0, 0), texto, font=fonte)
            largura_texto = caixa[2] - caixa[0]
            x = (largura_img - largura_texto) // 2
            draw.text((x, y), texto, font=fonte, fill=cor)

        # Adiciona os textos
        centralizar_texto(f"{dados['time_casa']} {dados['placar_casa']}", fonte_grande, 380)
        centralizar_texto(f"{dados['time_fora']} {dados['placar_fora']}", fonte_grande, 480)
        centralizar_texto(f"{dados['data']} - {dados['horario']}", fonte_media, 580, cor="darkred")

        # Salvar imagem temporária
        output_path = "banner_temp.png"
        img.convert('RGB').save(output_path)
        return output_path

    except Exception as e:
        logger.error(f"Erro ao criar banner: {e}")
        return None


# 🏗️ Comando /placar (apenas no privado)
async def comando_placar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return  # Ignora se não for no privado

    try:
        if len(context.args) < 6:
            await update.message.reply_text("❌ Uso correto: /placar TimeCasa PlacarCasa TimeFora PlacarFora Data Hora")
            return

        time_casa = context.args[0].replace("_", " ")
        placar_casa = int(context.args[1])
        time_fora = context.args[2].replace("_", " ")
        placar_fora = int(context.args[3])
        data = context.args[4]
        horario = context.args[5]

        DADOS_BANNER.update({
            'time_casa': time_casa,
            'placar_casa': placar_casa,
            'time_fora': time_fora,
            'placar_fora': placar_fora,
            'data': data,
            'horario': horario
        })

        await update.message.reply_text("✅ Dados atualizados com sucesso!")

    except Exception as e:
        logger.error(f"Erro no comando /placar: {e}")
        await update.message.reply_text("❌ Ocorreu um erro ao atualizar os dados.")


# 🎯 Comando /enviar (apenas no privado, envia no grupo)
async def comando_enviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return  # Ignora se não for no privado

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
            await update.message.reply_text("✅ Banner enviado no grupo com sucesso!")
        else:
            await update.message.reply_text("❌ Falha ao criar o banner.")
    except Exception as e:
        logger.error(f"Erro no comando /enviar: {e}")
        await update.message.reply_text("❌ Ocorreu um erro ao enviar o banner.")


# 🚀 Quando inicia
async def on_startup(app):
    logger.info("🤖 Bot iniciado!")


# ▶️ Main
def main():
    app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

    # Handlers
    app.add_handler(CommandHandler("placar", comando_placar))
    app.add_handler(CommandHandler("enviar", comando_enviar))

    logger.info("Bot rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()

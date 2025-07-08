# 🤖 Bot Telegram - Banner de Jogos

Projeto de bot para Telegram que gera e envia automaticamente um banner de resultados de partidas para um grupo específico.  
Feito em Python com `python-telegram-bot` e `PIL` para manipulação de imagens.

---

## 📌 Funcionalidades
✅ Receber comando privado `/placar` para atualizar dados do jogo  
✅ Gerar banner personalizado com escudos, placar, data e horário  
✅ Enviar o banner para um grupo usando o comando `/enviar` (também via privado)

---

## 🛠️ Tecnologias e Bibliotecas
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Pillow (PIL)](https://python-pillow.org/)
- logging (padrão do Python)
- Python 3.10+

---

## 📦 Estrutura resumida do projeto
```text
📂 logos/                 # Pasta com logos dos times (nomes como Real_Madrid.png)
├── base_banner.png       # Imagem de fundo do banner
├── BebasNeue-Regular.ttf # Fonte utilizada (opcional)
├── bot.py                # Código principal do bot
└── README.md             # Este arquivo
```

---

## ⚙️ Como configurar
1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

> Exemplo de `requirements.txt`:
> ```
> python-telegram-bot
> Pillow
> ```

3. **Configure variáveis importantes no código:**
No `bot.py`, substitua:
```python
TOKEN = "SEU TOKEN AQUI"  # Token do Bot
CHAT_ID = SEU_CHAT_ID_AQUI  # ID do grupo que receberá o banner
```

4. **Garanta que existam as imagens:**
- `base_banner.png`: fundo do banner
- `logos/Time.png`: logos dos times (o nome do arquivo deve corresponder ao nome do time usado no comando, trocando espaços por _)

---

## 🚀 Como usar
1. Inicie o bot:
```bash
python bot.py
```

2. No Telegram, envie no privado do bot:
- Atualizar placar:
```bash
/placar TimeCasa PlacarCasa TimeFora PlacarFora Data Hora
```
Exemplo:
```
/placar Real_Madrid 3 Barcelona 1 25/06/2025 20:00
```

- Gerar e enviar banner no grupo:
```bash
/enviar
```

---

## ✏️ Explicação do fluxo
- O bot só aceita comandos no **privado** para evitar bagunça no grupo.
- `/placar` atualiza os dados em memória.
- `/enviar` gera a imagem do banner e publica no grupo usando o `CHAT_ID`.

---

## 🛡️ Observações importantes
- O projeto precisa ter as logos salvas na pasta `logos/`.
- Se faltar a fonte ou ela não puder ser carregada, o script usa uma fonte padrão.
- O bot precisa ter permissão de envio de imagens no grupo.

---

## 📄 Licença
Este projeto é livre, sinta-se à vontade para adaptar ou melhorar.

---

## ✉️ Contato
Desenvolvido por [Evandro](https://github.com/4L3M40)

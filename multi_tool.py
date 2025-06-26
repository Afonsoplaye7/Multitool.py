import os
import requests
import random
import string
import asyncio
import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook
 
# Token do bot
TOKEN_BOT_DISCORD = 'MTM1MDUwOTk2MjQwMDUwMTg0MQ.GKlmVm.iItZt6JsmlLjIVcfucvZee6xX3JFV1h0DitZl4'
 
# Webhooks do Discord
webhook_url = 'https://discord.com/api/webhooks/1386857206414311496/sNDUv_PxgS6TnOlqEVzx88pCGU-kCO8_wATUl6Ue6CNxeWQf2MtuKFLJuH5e97cFKxkS'
webhook_pv_url = 'https://discord.com/api/webhooks/1386864850835345458/OWlsYU9SBkawH_2NLOCRGy7GK-965viJnZBUV34bW60afCJ-7cTbiD8r34ANVvkvX92n'
 
# Link do servidor
link_servidor_discord = 'https://discord.gg/EcsRWQapqc'
 
# ANSI Colors
azul_escuro = '\033[34m'
branco = '\033[37m'
reset = '\033[0m'
 
# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
 
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
 
def chat_geral():
    limpar_tela()
    print('\nChat Geral - Digite "sair" para voltar.\n')
    while True:
        mensagem = input('Digite sua mensagem: ')
        if mensagem.lower() == 'sair':
            break
        if mensagem.strip() == '':
            print('Não pode enviar mensagem vazia.')
            continue
        if mensagem.lower() == '/k.serve':
            mensagem = f'Nosso servidor do Discord: {link_servidor_discord}'
        webhook = DiscordWebhook(url=webhook_url, content=mensagem)
        response = webhook.execute()
        if response.status_code in (200, 204):
            print('Mensagem enviada no chat do server!\n')
        else:
            print(f'Erro: {response.status_code} - {response.text}')
 
def chat_pv():
    limpar_tela()
    nome = input('Seu nome ou apelido: ').strip() or 'Anônimo'
    print(f'\nEntrando no chat como [{nome}]. Digite "sair" para voltar.\n')
    while True:
        mensagem = input(f'[{nome}] ')
        if mensagem.lower() == 'sair':
            break
        if mensagem.strip() == '':
            print('Mensagem vazia.')
            continue
        conteudo = f'[{nome}] {mensagem}'
        webhook = DiscordWebhook(url=webhook_pv_url, content=conteudo)
        response = webhook.execute()
        print('Enviado!' if response.status_code in (200, 204) else f'Erro: {response.status_code}')
 
def info_usuario_discord():
    limpar_tela()
    user_id = input("Digite o ID do usuário do Discord: ").strip()
    if not user_id.isdigit():
        print("ID inválido.")
        input("ENTER para continuar...")
        return
    url = f"https://discord.com/api/v10/users/{user_id}"
    headers = {"Authorization": f"Bot {TOKEN_BOT_DISCORD}"}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print(f"\nNome: {data['username']}#{data.get('discriminator', '0000')}")
            print(f"ID: {user_id}")
            if data.get('avatar'):
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{data['avatar']}.png"
                print(f"Avatar: {avatar_url}")
        else:
            print(f"Erro: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f'Erro: {e}')
    input("ENTER para continuar...")
 
def gerar_senha_segura():
    limpar_tela()
    print('Gerador de Senhas')
    try:
        comprimento = int(input('Tamanho da senha (mínimo 8): '))
        if comprimento < 8:
            print('Muito pequena.')
            return
    except:
        print('Entrada inválida.')
        return
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(comprimento))
    print(f'\nSenha gerada:\n\n{branco}{senha}{reset}\n')
    input("ENTER para continuar...")
 
def nosso_servidor_discord():
    limpar_tela()
    print(f'\nServidor: {link_servidor_discord}\n')
    webhook = DiscordWebhook(url=webhook_url, content=f'Nosso servidor: {link_servidor_discord}')
    response = webhook.execute()
    print('Link enviado!' if response.status_code in (200, 204) else f'Erro: {response.status_code}')
    input("ENTER para continuar...")
 
async def spam_em_todos_canais():
    limpar_tela()
    guild_id = int(input("Qual ID do servidor? "))
    mensagem = input("Mensagem para spamar: ")
    vezes = int(input("Quantas vezes em cada canal? "))
    guild = bot.get_guild(guild_id)
    if not guild:
        print("Bot não está no servidor.")
        return
    total = 0
    for canal in guild.text_channels:
        try:
            for _ in range(vezes):
                await canal.send(mensagem)
                total += 1
            print(f"Canal: {canal.name}")
        except:
            print(f"Falha no canal: {canal.name}")
    print(f"\nFinalizado! Total: {total} mensagens.")
    input("ENTER para voltar...")
 
async def menu_principal():
    while True:
        limpar_tela()
        print(rf"""{azul_escuro}
KALEB INVASOES TOOL {reset}
 
{branco}[01]{reset} Chat geral do servidor
{branco}[02]{reset} Chat privado (PV)
{branco}[03]{reset} Ver informações de usuário Discord
{branco}[04]{reset} Gerador de senhas seguras
{branco}[05]{reset} Sair
{branco}[06]{reset} Nosso servidor do Discord
{branco}[07]{reset} Spamar em todos os canais do servidor (via ID do serve)
""")
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            chat_geral()
        elif opcao == '2':
            chat_pv()
        elif opcao == '3':
            info_usuario_discord()
        elif opcao == '4':
            gerar_senha_segura()
        elif opcao == '5':
            print('Saindo...')
            await bot.close()
            break
        elif opcao == '6':
            nosso_servidor_discord()
        elif opcao == '7':
            await spam_em_todos_canais()
        else:
            print('Opção inválida.')
            input("ENTER para voltar...")
 
@bot.event
async def on_ready():
    print(f'Bot online como: {bot.user}')
    await menu_principal()
 
if __name__ == '__main__':
    asyncio.run(bot.start(TOKEN_BOT_DISCORD))

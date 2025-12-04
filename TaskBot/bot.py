import discord
from discord.ext import commands
import json, base64, os, requests
from datetime import datetime

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'pykmintin/Repo')
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
PREFIX = os.environ.get('PREFIX', '!')
AUTHORIZED_USER = int(os.environ.get('AUTHORIZED_USER', '0'))
TASKS_FILE = 'tasks.json'
GITHUB_API = f'https://api.github.com/repos/{GITHUB_REPO}/contents'

def get_file_sha(path):
    url = f'{GITHUB_API}/{path}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    r = requests.get(url, headers=headers)
    return r.json()['sha'] if r.status_code == 200 else None

def get_tasks():
    url = f'{GITHUB_API}/{TASKS_FILE}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    r = requests.get(url, headers=headers)
    if r.status_code == 404:
        save_tasks([])
        return []
    r.raise_for_status()
    return json.loads(base64.b64decode(r.json()['content']).decode('utf-8'))['tasks']

def save_tasks(tasks):
    url = f'{GITHUB_API}/{TASKS_FILE}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    sha = get_file_sha(TASKS_FILE)
    content = json.dumps({'tasks': tasks}, indent=2)
    encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {'message': 'Update tasks', 'content': encoded}
    if sha: data['sha'] = sha
    r = requests.put(url, headers=headers, json=data)
    r.raise_for_status()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def is_authorized(ctx):
    return ctx.author.id == AUTHORIZED_USER

@bot.command()
@commands.check(is_authorized)
async def add(ctx, prio: str, *, text: str):
    prio = prio.lower()
    if prio not in ['h', 'n']:
        return await ctx.send('❌ Priority must be h/n')
    prio_full = 'high' if prio == 'h' else 'normal'
    tasks = get_tasks()
    task_id = max([t['id'] for t in tasks], default=0) + 1
    task = {'id': task_id, 'text': text, 'prio': prio_full, 'done': False, 'created': datetime.utcnow().isoformat()}
    tasks.append(task)
    save_tasks(tasks)
    await ctx.send(f'✅ #{task_id} [{prio}] {text}')

@bot.command()
@commands.check(is_authorized)
async def tasks(ctx):
    tasks = get_tasks()
    if not tasks: return await ctx.send('📭 No tasks')
    sorted_tasks = sorted(tasks, key=lambda x: (x['done'], x['prio'] != 'high'))
    lines = [f"{'🔴' if t['prio']=='high' else '⚪'} #{t['id']} {'✅' if t['done'] else '⏳'} {t['text']}" for t in sorted_tasks]
    await ctx.send('📋 **Tasks**\n' + '\n'.join(lines) + '\n\n✅ React to complete first undone task')

@bot.command()
@commands.check(is_authorized)
async def done(ctx, task_id: int):
    tasks = get_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['done'] = True
            save_tasks(tasks)
            return await ctx.send(f'✅ #{task_id} done')
    await ctx.send(f'❌ #{task_id} not found')

@bot.command()
@commands.check(is_authorized)
async def delete(ctx, task_id: int):
    tasks = get_tasks()
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            removed = tasks.pop(i)
            save_tasks(tasks)
            return await ctx.send(f'🗑️ Deleted: #{task_id} "{removed["text"]}"')
    await ctx.send(f'❌ #{task_id} not found')

@bot.event
async def on_reaction_add(r, user):
    if user.bot or r.emoji != '✅' or user.id != AUTHORIZED_USER: return
    if r.message.author != bot.user or 'Tasks' not in r.message.content: return
    tasks = get_tasks()
    undone = [t for t in tasks if not t['done']]
    if undone:
        undone[0]['done'] = True
        save_tasks(tasks)
        await r.message.channel.send(f'✅ Reacted: #{undone[0]["id"]} done')

@bot.event
async def on_ready():
    print(f'{bot.user} is ready')

bot.run(DISCORD_TOKEN)

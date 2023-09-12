#!/usr/bin/env python3
import os
from datetime import datetime, timezone
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
import openai
from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status

__version__ = '0.1.0'
console = Console(width=120)
console.print(f'aicli - OpenAI powered AI CLI v{__version__}', style='green bold', highlight=False)

try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    console.print('You must set the OPENAI_API_KEY environment variable', style='red')
    exit(1)

now_utc = datetime.now(timezone.utc)
setup = f"""
Help the user by responding to their request, the output should be concise and always written in markdown.
The current date and time is {datetime.now()} {now_utc.astimezone().tzinfo.tzname(now_utc)}.
"""
messages = [{'role': 'system', 'content': setup}]

history = Path().home() / '.openai-prompt-history.txt'
session = PromptSession(history=FileHistory(history))
while True:
    try:
        text = session.prompt('➤ ')
    except (KeyboardInterrupt, EOFError):
        break
    if not text:
        continue
    status = Status('[dim]Working on it…[/dim]', console=console)
    status.start()
    messages.append({'role': 'user', 'content': text})
    try:
        response = openai.ChatCompletion.create(model='gpt-4', messages=messages)
    except KeyboardInterrupt:
        break
    content = response['choices'][0]['message']['content']
    messages.append({'role': 'assistant', 'content': content})
    status.stop()
    md = Markdown(content)
    console.print(md)
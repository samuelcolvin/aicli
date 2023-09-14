#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status

__version__ = '0.1.0'


def cli() -> int:
    console = Console(width=120)
    console.print(f'aicli - OpenAI powered AI CLI v{__version__}', style='green bold', highlight=False)

    try:
        openai.api_key = os.environ['OPENAI_API_KEY']
    except KeyError:
        console.print('You must set the OPENAI_API_KEY environment variable', style='red')
        return 1

    now_utc = datetime.now(timezone.utc)
    setup = f"""
Help the user by responding to their request, the output should be concise and always written in markdown.
The current date and time is {datetime.now()} {now_utc.astimezone().tzinfo.tzname(now_utc)}.
"""
    messages = [{'role': 'system', 'content': setup}]

    history = Path().home() / '.openai-prompt-history.txt'
    session = PromptSession(history=FileHistory(str(history)))
    while True:
        try:
            text = session.prompt('➤ ')
        except (KeyboardInterrupt, EOFError):
            return 0

        if not text:
            continue

        status = Status('[dim]Working on it…[/dim]', console=console)
        status.start()
        messages.append({'role': 'user', 'content': text})

        try:
            response = openai.ChatCompletion.create(model='gpt-4', messages=messages)
        except KeyboardInterrupt:
            status.stop()
            return 0

        content = response['choices'][0]['message']['content']
        messages.append({'role': 'assistant', 'content': content})
        status.stop()
        md = Markdown(content)
        console.print(md)


if __name__ == '__main__':
    sys.exit(cli())

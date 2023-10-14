#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.console import Console, ConsoleOptions, RenderResult
from rich.live import Live
from rich.markdown import CodeBlock, Markdown
from rich.status import Status
from rich.syntax import Syntax
from rich.text import Text

__version__ = '0.5.0'


class SimpleCodeBlock(CodeBlock):
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        code = str(self.text).rstrip()
        yield Text(self.lexer_name, style='dim')
        yield Syntax(code, self.lexer_name, theme=self.theme, background_color='default', word_wrap=True)
        yield Text(f'/{self.lexer_name}', style='dim')


Markdown.elements['fence'] = SimpleCodeBlock


def cli() -> int:
    console = Console()
    console.print(f'aicli - OpenAI powered AI CLI v{__version__}', style='green bold', highlight=False)

    try:
        openai.api_key = os.environ['OPENAI_API_KEY']
    except KeyError:
        console.print('You must set the OPENAI_API_KEY environment variable', style='red')
        return 1

    now_utc = datetime.now(timezone.utc)
    setup = f"""\
Help the user by responding to their request, the output should be concise and always written in markdown.
The current date and time is {datetime.now()} {now_utc.astimezone().tzinfo.tzname(now_utc)}."""

    messages = [{'role': 'system', 'content': setup}]

    history = Path().home() / '.openai-prompt-history.txt'
    session = PromptSession(history=FileHistory(str(history)))

    # allows you to disable streaming responses if they get annoying or are more expensive.
    stream = True

    while True:
        try:
            text = session.prompt('aicli ➤ ', auto_suggest=AutoSuggestFromHistory())
        except (KeyboardInterrupt, EOFError):
            return 0

        if not text.strip():
            continue

        if text.lower().replace(' ', '-') == 'show-markdown':
            last_content = messages[-1]['content']
            console.print('[dim]Last markdown output of last question:[/dim]\n')
            console.print(Syntax(last_content, lexer='markdown', background_color='default'))
            continue

        status = Status('[dim]Working on it…[/dim]', console=console)
        status.start()
        messages.append({'role': 'user', 'content': text})

        try:
            response = openai.ChatCompletion.create(model='gpt-4', messages=messages, stream=stream)
        except KeyboardInterrupt:
            status.stop()
            return 0

        status.stop()
        if stream:
            content = ''
            try:
                with Live('', refresh_per_second=15, console=console) as live:
                    for chunk in response:
                        if chunk['choices'][0]['finish_reason'] is not None:
                            break
                        chunk_text = chunk['choices'][0]['delta'].get('content', '')
                        content += chunk_text
                        live.update(Markdown(content))
            except KeyboardInterrupt:
                console.print('[dim]Interrupted[/dim]')
        else:
            content = response['choices'][0]['message']['content']
            md = Markdown(content)
            console.print(md)

        messages.append({'role': 'assistant', 'content': content})


if __name__ == '__main__':
    sys.exit(cli())

import shlex
from repository import Repository
from diffing import diff_files


def format_nodes(nodes):
    return '\n'.join(f'{n.hash} | {n.author} | {n.timestamp.isoformat()} | {n.message}' for n in nodes) or 'No commits'


def execute(repository, line):
    """문법 파싱과 오류 표시를 알고리즘에서 분리합니다."""
    try:
        args = shlex.split(line)
        if not args:
            return ''
        command = args[0].upper()
        if command == 'DIFF':
            return diff_files(args[1],args[2]) if len(args)==3 else 'Invalid args'
        if command == 'INIT' and len(args) == 2:
            repository.init(args[1])
            return f'Initialized repository.\nCurrent branch: main\nCurrent user: {args[1]}'
        if command == 'BRANCH' and len(args) == 2:
            repository.branch(args[1])
            return 'Created branch: ' + args[1]
        if command == 'SWITCH' and len(args) == 2:
            repository.switch(args[1])
            return 'Switched to branch: ' + args[1]
        if command == 'COMMIT' and len(args) == 2:
            node = repository.commit(args[1])
            return f'[{repository.current} {node.hash}] {node.message}'
        if command == 'MERGE' and len(args) == 2:
            node = repository.merge(args[1])
            return f'[{repository.current} {node.hash}] {node.message}'
        repository.ready()
        if command == 'LOG' and len(args) in (1, 2):
            if len(args) == 1:
                return format_nodes(repository.log())
            if args[1].startswith('--sort-by='):
                return format_nodes(repository.log(args[1].split('=', 1)[1]))
        if command == 'PATH' and len(args) == 3:
            path = repository.graph.path(args[1], args[2])
            return 'Path: ' + '->'.join(path) if path else 'No path'
        if command == 'ANCESTORS' and len(args) == 2:
            return format_nodes(repository.graph.ancestors(args[1]))
        if command == 'SEARCH' and len(args) == 2:
            if args[1].startswith('--author='):
                return format_nodes(repository.search(author=args[1].split('=', 1)[1]))
            if not args[1].startswith('--'):
                return format_nodes(repository.search(keyword=args[1]))
        if command in ('INIT', 'BRANCH', 'SWITCH', 'COMMIT', 'LOG', 'PATH', 'ANCESTORS', 'SEARCH', 'MERGE'):
            return 'Invalid args'
        return 'Unknown command: ' + args[0]
    except (ValueError, OSError, UnicodeError) as error:
        return str(error)


def main():
    repository = Repository()
    while True:
        try:
            line = input('mini-git> ')
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip().lower() in ('exit', 'quit'):
            break
        output = execute(repository, line)
        if output:
            print(output)


if __name__ == '__main__':
    main()

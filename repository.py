from datetime import datetime
from graph import Commit, CommitGraph
from sorting import merge_sort


class Repository:
    """브랜치 포인터와 역색인을 커밋 생성 시 함께 갱신합니다."""
    def __init__(self, clock=lambda: datetime.now().astimezone()):
        self.clock = clock
        self.graph = CommitGraph()
        self.branches = {}
        self.current = None
        self.author = None
        self.sequence = 0
        self.keywords = {}
        self.authors = {}

    def init(self, user):
        if self.current is not None:
            raise ValueError('Already initialized')
        if not user.strip():
            raise ValueError('Invalid args')
        self.author = user
        self.current = 'main'
        self.branches['main'] = None

    def ready(self):
        if self.current is None:
            raise ValueError('Initialize repository first')

    def branch(self, name):
        self.ready()
        if not name.strip() or name in self.branches:
            raise ValueError('Invalid or duplicate branch: ' + name)
        self.branches[name] = self.branches[self.current]

    def switch(self, name):
        self.ready()
        if name not in self.branches:
            raise ValueError('Unknown branch: ' + name)
        self.current = name

    def commit(self, message, extra_parent=None):
        self.ready()
        if not message.strip():
            raise ValueError('Invalid args')
        parents = []
        head = self.branches[self.current]
        if head is not None:
            parents.append(head)
        if extra_parent is not None and extra_parent not in parents:
            self.graph.require(extra_parent)
            parents.append(extra_parent)
        self.sequence += 1
        identifier = f'c{self.sequence:08x}'
        node = Commit(identifier, message, self.author, self.clock(), tuple(parents))
        self.graph.add(node)
        self.branches[self.current] = identifier
        self.authors.setdefault(node.author, []).append(identifier)
        for word in set(message.lower().split()):
            self.keywords.setdefault(word, []).append(identifier)
        return node

    def merge(self, branch):
        self.ready()
        if branch not in self.branches:
            raise ValueError('Unknown branch: ' + branch)
        if branch == self.current or self.branches[branch] is None:
            raise ValueError('Invalid merge target')
        return self.commit('Merge ' + branch, self.branches[branch])

    def log(self, order=None):
        self.ready()
        if order is None:
            return self.graph.topological()
        if order == 'date':
            return merge_sort(list(self.graph.nodes.values()), lambda node: node.timestamp)
        if order == 'author':
            return merge_sort(list(self.graph.nodes.values()), lambda node: node.author)
        raise ValueError('Invalid args')

    def search(self, keyword=None, author=None):
        self.ready()
        if author is not None:
            identifiers = self.authors.get(author, [])
        else:
            tokens = keyword.lower().split()
            if not tokens:
                return []
            identifiers = list(self.keywords.get(tokens[0], []))
            for token in tokens[1:]:
                candidates = set(self.keywords.get(token, []))
                identifiers = [identifier for identifier in identifiers if identifier in candidates]
        return [self.graph.nodes[identifier] for identifier in identifiers]

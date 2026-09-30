from collections import deque
from dataclasses import dataclass
from datetime import datetime
from sorting import merge_sort


@dataclass(frozen=True)
class Commit:
    hash: str
    message: str
    author: str
    timestamp: datetime
    parents: tuple[str, ...]


class CommitGraph:
    """커밋 노드와 부모/자식 인접 목록을 분리합니다."""
    def __init__(self):
        self.nodes = {}
        self.children = {}

    def add(self, commit):
        if commit.hash in self.nodes:
            raise ValueError('Duplicate commit: ' + commit.hash)
        for parent in commit.parents:
            self.require(parent)
        self.nodes[commit.hash] = commit
        self.children[commit.hash] = []
        for parent in commit.parents:
            self.children[parent].append(commit.hash)

    def require(self, identifier):
        if identifier not in self.nodes:
            raise ValueError('Unknown commit: ' + identifier)
        return self.nodes[identifier]

    def topological(self):
        """진입 차수가 0인 노드부터 출력하는 Kahn 위상 정렬."""
        degree = {identifier: len(node.parents) for identifier, node in self.nodes.items()}
        queue = deque(identifier for identifier in self.nodes if degree[identifier] == 0)
        result = []
        while queue:
            identifier = queue.popleft()
            result.append(self.nodes[identifier])
            for child in self.children[identifier]:
                degree[child] -= 1
                if degree[child] == 0:
                    queue.append(child)
        if len(result) != len(self.nodes):
            raise ValueError('Commit graph contains a cycle')
        return result

    def ancestors(self, identifier):
        self.require(identifier)
        visited = set()
        stack = list(self.nodes[identifier].parents)
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                stack.extend(self.nodes[current].parents)
        return [node for node in self.topological() if node.hash in visited]

    def path(self, start, end):
        """BFS에서 이웃을 사전순으로 방문해 같은 길이의 경로를 결정합니다."""
        self.require(start)
        self.require(end)
        queue = deque([start])
        previous = {start: None}
        while queue:
            current = queue.popleft()
            if current == end:
                path = []
                while current is not None:
                    path.append(current)
                    current = previous[current]
                return list(reversed(path))
            neighbors = list(self.nodes[current].parents) + self.children[current]
            for neighbor in merge_sort(neighbors):
                if neighbor not in previous:
                    previous[neighbor] = current
                    queue.append(neighbor)
        return None

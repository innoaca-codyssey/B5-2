from datetime import datetime, timezone
import unittest
from graph import Commit, CommitGraph
from main import execute
from repository import Repository
from sorting import merge_sort


class GraphTests(unittest.TestCase):
    def graph(self):
        graph = CommitGraph()
        for identifier, parents in [('r', ()), ('a', ('r',)), ('b', ('r',)), ('m', ('b', 'a')), ('x', ())]:
            graph.add(Commit(identifier, identifier, 'Tester', datetime.now(timezone.utc), parents))
        return graph

    def test_shortest_lexical_paths_and_disconnected(self):
        graph = self.graph()
        self.assertEqual(graph.path('r', 'm'), ['r', 'a', 'm'])
        self.assertEqual(graph.path('m', 'r'), ['m', 'a', 'r'])
        self.assertEqual(graph.path('a', 'b'), ['a', 'm', 'b'])
        self.assertEqual(graph.path('r', 'r'), ['r'])
        self.assertIsNone(graph.path('r', 'x'))
        with self.assertRaises(ValueError):
            graph.path('r', 'missing')

    def test_parents_before_children_and_all_ancestors(self):
        graph = self.graph()
        positions = {node.hash: i for i, node in enumerate(graph.topological())}
        for node in graph.nodes.values():
            for parent in node.parents:
                self.assertLess(positions[parent], positions[node.hash])
        self.assertEqual(set(node.hash for node in graph.ancestors('m')), {'r', 'a', 'b'})

    def test_duplicate_missing_parent_and_long_chain(self):
        graph = CommitGraph()
        now = datetime.now(timezone.utc)
        with self.assertRaises(ValueError):
            graph.add(Commit('a', '', '', now, ('missing',)))
        for i in range(3000):
            graph.add(Commit(str(i), '', '', now, (str(i-1),) if i else ()))
        self.assertEqual(len(graph.ancestors('2999')), 2999)
        with self.assertRaises(ValueError):
            graph.add(graph.nodes['0'])

    def test_stable_merge_sort(self):
        values = [(2, 'first'), (1, 'a'), (2, 'second'), (1, 'b')]
        self.assertEqual(merge_sort(values, lambda value: value[0]), [(1, 'a'), (1, 'b'), (2, 'first'), (2, 'second')])
        self.assertEqual(merge_sort(list(range(1000, -1, -1))), list(range(1001)))


class RepositoryTests(unittest.TestCase):
    def test_branch_merge_index_and_unique_hashes(self):
        repository = Repository()
        repository.init('Zoe')
        root = repository.commit('Initial commit')
        repository.branch('feature')
        repository.switch('feature')
        repository.author = 'Alice'
        feature = repository.commit('Add LOGIN login feature')
        repository.switch('main')
        repository.commit('Add payment')
        merged = repository.merge('feature')
        self.assertEqual(len(merged.parents), 2)
        self.assertEqual([node.hash for node in repository.search(keyword='LOGIN')], [feature.hash])
        self.assertEqual([node.hash for node in repository.search(keyword='add login')], [feature.hash])
        self.assertEqual([node.hash for node in repository.search(author='Zoe')], [root.hash])
        self.assertEqual(repository.log('author')[-1].author, 'Zoe')
        self.assertEqual(len(set(repository.graph.nodes)), 4)

    def test_cli_errors_case_and_spaces(self):
        repository = Repository()
        self.assertEqual(execute(repository, 'log'), 'Initialize repository first')
        self.assertIn('Current user: Shin Yejun', execute(repository, 'init "Shin Yejun"'))
        self.assertIn('c00000001', execute(repository, 'commit "Add login"'))
        self.assertEqual(execute(repository, 'switch missing'), 'Unknown branch: missing')
        self.assertEqual(execute(repository, 'path missing c00000001'), 'Unknown commit: missing')
        self.assertEqual(execute(repository, 'log --sort-by=wrong'), 'Invalid args')
        self.assertEqual(execute(repository, 'commit'), 'Invalid args')
        self.assertEqual(execute(repository, 'unknown'), 'Unknown command: unknown')


if __name__ == '__main__':
    unittest.main()

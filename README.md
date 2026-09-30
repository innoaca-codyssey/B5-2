# B5-2: 파일이 언제 어떻게 바뀌었는지 기록하는 작은 프로그램 만들기

커밋 메타데이터를 DAG로 관리하는 Mini Git입니다. 브랜치와 HEAD, 부모 우선 로그, 최단 경로, 조상 탐색, 역색인 검색을 제공합니다. 정렬은 안정적인 병합 정렬로 구현합니다.

## 실행 방법

Python 3.10 이상에서 표준 라이브러리를 사용합니다. 데이터는 세션의 메모리에 저장합니다.

```bash
python3 main.py
```

명령은 대소문자를 구분하지 않으며 공백을 포함한 문자열은 따옴표로 감쌉니다. LOG는 모든 브랜치의 커밋을 부모 우선으로 출력합니다. LOG --sort-by=date는 시간 오름차순, author는 이름 오름차순입니다. 두 정렬 옵션에는 부모 우선 조건을 적용하지 않습니다.

## 실행 환경

```bash
$ python3 --version
Python 3.14.7
```

macOS arm64에서 실행했습니다.

## 그래프 탐색과 정렬 검증

```bash
$ python3 -m unittest discover -s tests -v
test_duplicate_missing_parent_and_long_chain (testgraph.GraphTests.test_duplicate_missing_parent_and_long_chain) ... ok
test_parents_before_children_and_all_ancestors (testgraph.GraphTests.test_parents_before_children_and_all_ancestors) ... ok
test_shortest_lexical_paths_and_disconnected (testgraph.GraphTests.test_shortest_lexical_paths_and_disconnected) ... ok
test_stable_merge_sort (testgraph.GraphTests.test_stable_merge_sort) ... ok
test_branch_merge_index_and_unique_hashes (testgraph.RepositoryTests.test_branch_merge_index_and_unique_hashes) ... ok
test_cli_errors_case_and_spaces (testgraph.RepositoryTests.test_cli_errors_case_and_spaces) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.008s

OK
```

두 경로의 길이가 같을 때 전체 hash 경로의 사전순을 비교했습니다. 3,000개 커밋의 조상 탐색, 여러 부모의 선후 관계, 역색인 중복 제거, 안정 정렬과 잘못된 CLI 입력을 검사했습니다.

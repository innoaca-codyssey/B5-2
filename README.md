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

## 브랜치와 커밋 탐색

```bash
$ python3 main.py
Input:
init "Shin Yejun"
branch orphan
commit "Initial commit"
branch feature
switch feature
commit "Add login feature"
switch main
commit "Add payment feature"
merge feature
log
path c00000002 c00000003
ancestors c00000004
search login
search --author="Shin Yejun"
log --sort-by=date
log --sort-by=author
switch orphan
commit "Independent root"
path c00000001 c00000005
switch missing
path c00000001 missing
quit

mini-git> Initialized repository.
Current branch: main
Current user: Shin Yejun
mini-git> Created branch: orphan
mini-git> [main c00000001] Initial commit
mini-git> Created branch: feature
mini-git> Switched to branch: feature
mini-git> [feature c00000002] Add login feature
mini-git> Switched to branch: main
mini-git> [main c00000003] Add payment feature
mini-git> [main c00000004] Merge feature
mini-git> c00000001 | Shin Yejun | 2026-09-30T22:18:03.479842+09:00 | Initial commit
c00000002 | Shin Yejun | 2026-09-30T22:18:03.480373+09:00 | Add login feature
c00000003 | Shin Yejun | 2026-09-30T22:18:03.480850+09:00 | Add payment feature
c00000004 | Shin Yejun | 2026-09-30T22:18:03.481323+09:00 | Merge feature
mini-git> Path: c00000002->c00000001->c00000003
mini-git> c00000001 | Shin Yejun | 2026-09-30T22:18:03.479842+09:00 | Initial commit
c00000002 | Shin Yejun | 2026-09-30T22:18:03.480373+09:00 | Add login feature
c00000003 | Shin Yejun | 2026-09-30T22:18:03.480850+09:00 | Add payment feature
mini-git> c00000002 | Shin Yejun | 2026-09-30T22:18:03.480373+09:00 | Add login feature
mini-git> c00000001 | Shin Yejun | 2026-09-30T22:18:03.479842+09:00 | Initial commit
c00000002 | Shin Yejun | 2026-09-30T22:18:03.480373+09:00 | Add login feature
c00000003 | Shin Yejun | 2026-09-30T22:18:03.480850+09:00 | Add payment feature
c00000004 | Shin Yejun | 2026-09-30T22:18:03.481323+09:00 | Merge feature
mini-git> c00000001 | Shin Yejun | 2026-09-30T22:18:03.479842+09:00 | Initial commit
c00000002 | Shin Yejun | 2026-09-30T22:18:03.480373+09:00 | Add login feature
c00000003 | Shin Yejun | 2026-09-30T22:18:03.480850+09:00 | Add payment feature
c00000004 | Shin Yejun | 2026-09-30T22:18:03.481323+09:00 | Merge feature
mini-git> c00000001 | Shin Yejun | 2026-09-30T22:18:03.479842+09:00 | Initial commit
c00000002 | Shin Yejun | 2026-09-30T22:18:03.480373+09:00 | Add login feature
c00000003 | Shin Yejun | 2026-09-30T22:18:03.480850+09:00 | Add payment feature
c00000004 | Shin Yejun | 2026-09-30T22:18:03.481323+09:00 | Merge feature
mini-git> Switched to branch: orphan
mini-git> [orphan c00000005] Independent root
mini-git> No path
mini-git> Unknown branch: missing
mini-git> Unknown commit: missing
mini-git> ```

merge는 두 부모를 가진 커밋을 만드는 보너스 기능입니다. 빈 HEAD에서 만든 orphan 브랜치는 다른 그래프와 연결되지 않아 No path가 나옵니다. 위 Input은 프로그램에 전달한 표준 입력입니다.

## 그래프와 인덱스 구조

Repository는 사용자, 현재 브랜치와 브랜치별 HEAD를 관리합니다. CommitGraph는 hash를 키로 하는 dict와 부모/자식 목록을 관리합니다. 커밋은 생성 순번을 16진수로 표현한 hash를 가지며 세션에서 순번을 재사용하지 않습니다. 난수와 달리 입력 순서가 같으면 같은 hash를 얻어 테스트와 경로 추적이 쉽습니다.

새 커밋의 부모는 이미 존재하는 커밋으로 제한합니다. 새 노드에서 과거 노드로만 연결되므로 사이클이 생기지 않습니다. 사이클이 있으면 조상 탐색이 순환하고 부모 우선 출력이 불가능합니다. LOG는 Kahn 알고리즘으로 부모 수를 진입 차수로 잡고 0인 노드부터 큐에 넣습니다. 출력한 부모의 자식 차수를 줄여 모든 부모가 처리된 후 자식을 출력합니다. O(V+E)입니다.

PATH는 부모와 자식 연결을 모두 이웃으로 사용하는 BFS입니다. 한 간선마다 비용 1이므로 최초 도달이 최단 경로입니다. 이웃 hash를 병합 정렬한 순서로 탐색해 같은 길이에서는 사전순이 작은 경로를 먼저 찾습니다. 부모 방향만 허용하면 자식이나 형제 방향 경로는 없어집니다. 구현에서는 이웃의 children을 제외하면 됩니다. ANCESTORS는 부모 방향으로 스택과 방문 집합을 사용하고, 출력은 부모 우선 순서로 맞춥니다.

SEARCH는 공백으로 나눈 소문자 토큰의 역색인과 author 역색인을 사용합니다. 같은 메시지에서 중복된 단어는 한 번만 등록합니다. 공백이 있는 검색어는 모든 토큰이 포함된 커밋을 찾으며 부분 문자열 검색은 하지 않습니다. 한 단어 검색은 dict 평균 O(1) 조회 후 결과 k개를 읽는 O(k)입니다. 전체 커밋 메시지를 매번 읽는 O(n) 검색을 피합니다.

## 정렬과 확장

병합 정렬은 평균/최악 O(n log n), 추가 공간 O(n)이며 동률에서 왼쪽을 먼저 선택해 입력 순서를 유지하는 안정 정렬입니다. LOG의 date/author 옵션은 이 정렬을 사용합니다. author 정렬에도 부모 우선 조건이 필요해지면 Kahn의 준비된 노드 집합에서 author가 작은 노드를 고르는 우선순위 큐를 사용할 수 있습니다.

커밋이 10배 늘어나면 전체 LOG 출력, 조상 목록의 출력, PATH에서 이웃을 정렬하는 비용이 커집니다. 변경할 때 정렬된 인접 목록을 유지하거나, 로그에 범위를 주고, 역색인을 필요 시 디스크로 분리할 수 있습니다. 난수 hash로 바꾸면 충돌 여부를 확인하고 재생성해야 하며 테스트에서는 생성기를 주입해 재현성을 유지해야 합니다.

알고리즘은 graph.py와 sorting.py, 인덱스 갱신은 repository.py, 입력과 출력은 main.py에 분리했습니다. docstring은 사이클 방지, 위상 순서, BFS 동률 처리처럼 코드 선택의 이유가 필요한 부분에 작성했습니다.

## 줄 비교와 두 정렬 검사

```bash
$ python3 -m unittest discover -s tests -v
test_diff_common_added_deleted_and_repeated (testbonus.BonusTests.test_diff_common_added_deleted_and_repeated) ... ok
test_diff_empty_files_unicode_and_missing (testbonus.BonusTests.test_diff_empty_files_unicode_and_missing) ... ok
test_two_sorts_equal_stable_and_input_unchanged (testbonus.BonusTests.test_two_sorts_equal_stable_and_input_unchanged) ... ok
test_duplicate_missing_parent_and_long_chain (testgraph.GraphTests.test_duplicate_missing_parent_and_long_chain) ... ok
test_parents_before_children_and_all_ancestors (testgraph.GraphTests.test_parents_before_children_and_all_ancestors) ... ok
test_shortest_lexical_paths_and_disconnected (testgraph.GraphTests.test_shortest_lexical_paths_and_disconnected) ... ok
test_stable_merge_sort (testgraph.GraphTests.test_stable_merge_sort) ... ok
test_branch_merge_index_and_unique_hashes (testgraph.RepositoryTests.test_branch_merge_index_and_unique_hashes) ... ok
test_cli_errors_case_and_spaces (testgraph.RepositoryTests.test_cli_errors_case_and_spaces) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.016s

OK
```

Diff의 추가/삭제/공통 줄을 합쳐 원본 양쪽을 복원하고 중복 줄과 빈 파일, 한글, 없는 경로를 검사했습니다. 병합/삽입 정렬은 같은 키의 순서를 유지하며 입력을 변경하지 않습니다.

## 정렬 알고리즘 성능 비교

```bash
$ python3 -c 'from sorting import compare_sorts; print(compare_sorts())'
n,input_sha256,merge_ms,insertion_ms,repeats
200,b530ca9240a77f7f3ea472e6a05667f5b60891dbe438a2115b0dfc87450bd74a,0.145559,0.468158,5
1000,432235143a52dcb2316f17bad9254a9bb5e8499fdfdfba5dad2c68affbf60414,0.984125,12.971667,5
3000,1c80d926b28f15644dd9fc38e36f6550dc9813ec03b6dfa61de0e2a8d0da9bd9,3.466267,124.586792,5
```

seed 7의 같은 순열을 알고리즘마다 한 번 예열한 뒤 5회 측정한 평균입니다. 시간에는 입력 복사와 정렬을 포함하며 결과 검사와 입력 해시는 측정 밖에서 확인합니다. 병합 정렬은 평균/최악 O(n log n), 삽입 정렬은 정렬된 입력에서 O(n), 평균/최악 O(n^2)입니다. 두 구현은 동률에서 원래 순서를 유지합니다.

## 텍스트 파일의 줄 비교

```bash
$ printf "diff ../lab/before.txt ../lab/after.txt\nquit\n" | python3 main.py
mini-git>   로그인
+ 검색
  목록
- 삭제
mini-git> ```

공백 접두사는 공통 줄, +는 추가, -는 삭제입니다. LCS의 길이를 저장한 뒤 공통 줄을 따라갑니다. 시간과 저장 공간은 O(m*n)이므로 긴 파일에서는 메모리 부담이 커집니다. UTF-8 텍스트의 입력 순서와 줄바꿈 유무를 비교합니다.

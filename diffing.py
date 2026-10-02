from pathlib import Path


def diff_lines(left, right):
    """최장 공통 부분 수열을 기준으로 공통/삭제/추가 줄을 생성합니다."""
    m,n=len(left),len(right)
    lengths=[[0]*(n+1) for _ in range(m+1)]
    for i in range(m-1,-1,-1):
        for j in range(n-1,-1,-1):
            lengths[i][j]=1+lengths[i+1][j+1] if left[i]==right[j] else max(lengths[i+1][j],lengths[i][j+1])
    i=j=0
    while i<m or j<n:
        if i<m and j<n and left[i]==right[j]:
            yield ' ',left[i];i+=1;j+=1
        elif i<m and (j==n or lengths[i+1][j]>=lengths[i][j+1]):
            yield '-',left[i];i+=1
        else:
            yield '+',right[j];j+=1


def diff_files(left, right):
    first=Path(left).read_text(encoding='utf-8').splitlines(keepends=True)
    second=Path(right).read_text(encoding='utf-8').splitlines(keepends=True)
    return '\n'.join(marker+' '+line.rstrip('\r\n') for marker,line in diff_lines(first,second)) or 'No differences (empty files)'

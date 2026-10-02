def merge_sort(values, key=lambda value: value):
    """동률에서는 왼쪽 원소를 먼저 선택하는 안정 병합 정렬."""
    if len(values) <= 1:
        return list(values)
    middle = len(values) // 2
    left = merge_sort(values[:middle], key)
    right = merge_sort(values[middle:], key)
    result = []
    a = b = 0
    while a < len(left) and b < len(right):
        if key(left[a]) <= key(right[b]):
            result.append(left[a])
            a += 1
        else:
            result.append(right[b])
            b += 1
    result.extend(left[a:])
    result.extend(right[b:])
    return result


def insertion_sort(values, key=lambda value: value):
    """같은 키를 이동하지 않는 안정 삽입 정렬."""
    result=list(values)
    for i in range(1,len(result)):
        current=result[i]
        j=i-1
        while j>=0 and key(result[j])>key(current):
            result[j+1]=result[j]
            j-=1
        result[j+1]=current
    return result


def compare_sorts(sizes=(200, 1000, 3000), repeats=5, seed=7):
    """같은 순열을 두 알고리즘으로 반복 측정하고 평균 시간을 반환합니다."""
    import hashlib
    import random
    import time
    output = 'n,input_sha256,merge_ms,insertion_ms,repeats\n'
    for size in sizes:
        values = random.Random(seed).sample(range(size), size)
        before = hashlib.sha256(','.join(map(str, values)).encode()).hexdigest()
        averages = []
        for method in [merge_sort, insertion_sort]:
            method(values)
            elapsed = 0
            for _ in range(repeats):
                started = time.perf_counter_ns()
                result = method(values)
                elapsed += time.perf_counter_ns() - started
                if result != list(range(size)):
                    raise ValueError('정렬 결과가 예상 순서와 다릅니다')
            averages.append(elapsed / repeats / 1000000)
        after = hashlib.sha256(','.join(map(str, values)).encode()).hexdigest()
        if before != after:
            raise ValueError('입력 배열이 변경되었습니다')
        output += f'{size},{before},{averages[0]:.6f},{averages[1]:.6f},{repeats}\n'
    return output.rstrip()

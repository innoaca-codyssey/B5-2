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

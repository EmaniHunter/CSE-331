"""
Name: Emani Hunter
PID: A55714733
"""


def quick_sort(unsorted, threshold, start, end, reverse=False):
    """"
    Performs quick sort on list within range of indices: start and end
    :param unsorted: the list to sort
    :param threshold: maximum length that list can be for insertion sort to be called
    :param start: start index of range of values in list
    :param end: end index of range of values in list
    :param reverse: if reverse = false list is sorted ascending otherwise sorted descending
    """""
    # TIME COMPLEXITY: O(nlog(n))
    if (end-start + 1) <= threshold:
        insertion_sort(unsorted, start, end, reverse)

    if start >= end:
        return

    pivot_index = subdivide(unsorted, start, end, reverse)
    quick_sort(unsorted, threshold, start, pivot_index - 1, reverse)
    quick_sort(unsorted, threshold, pivot_index + 1, end, reverse)


def subdivide(unsorted, start, end, reverse):
    """"
    Performs subdivide on list within range of indices: start and end
    :param unsorted: the list to sort
    :param start: start index of range of values in list
    :param end: end index of range of values in list
    :param reverse: if reverse = false list is sorted ascending otherwise sorted descending
    :return: index of pivot value
    """""
    # TIME COMPLEXITY: O(n)
    if len(unsorted) == 0:
        return start

    if len(unsorted) == 1:
        return start

    if start >= end:
        return

    pivot = find_pivot(unsorted, start, end)
    left = start
    right = end-1
    if reverse is True:
        while left <= right:
            while left <= right and unsorted[left] > pivot:
                left = left + 1
            while left <= right and pivot > unsorted[right]:
                right = right - 1
            if left <= right:
                unsorted[left], unsorted[right] = unsorted[right], unsorted[left]  # swap
                left, right = left + 1, right - 1

        unsorted[left], unsorted[end] = unsorted[end], unsorted[left]

    else:
        while left <= right:
            while left <= right and unsorted[left] < pivot:
                left = left + 1
            while left <= right and pivot < unsorted[right]:
                right = right - 1
            if left <= right:
                unsorted[left], unsorted[right] = unsorted[right], unsorted[left] # swap
                left, right = left + 1, right - 1

        unsorted[left], unsorted[end] = unsorted[end], unsorted[left]

    return left


def find_pivot(unsorted, start, end):
    """"
    Finds pivot value for given indices by using median of three approach
    :param unsorted: the list to sort
    :param start: start index of range of values in list
    :param end: end index of range of values in list
    :return: pivot value
    """""
    # TIME COMPLEXITY: O(1)
    if len(unsorted) == 0:
        return start
    if len(unsorted) == 1:
        return start
    if len(unsorted) == 2:
        return end

    middle = (start + end) // 2
    num_1 = unsorted[start]
    num_2 = unsorted[middle]
    num_3 = unsorted[end]

    if num_1 > num_2:
        if num_1 < num_3:
            num_1, num_3 = num_3, num_1
            return num_1
        if num_2 > num_3:
            num_2, num_3 = num_3, num_2
            return num_2
        return num_3
    else:
        if num_1 > num_3:
            num_1, num_3 = num_3, num_1
            return num_1
        if num_2 < num_3:
            num_2, num_3 = num_3, num_2
            return num_2
        return num_3


def exchange(unsorted, left, right):
    """"
    Helper function to swap indices, referenced from Dr. Onsay
    :param unsorted: the list to sort
    :param left: left partition of range of values in list
    :param right: right partition of range of values in list
    """""
    unsorted[left], unsorted[right] = unsorted[right], unsorted[left]


def insertion_sort(unsorted, start, end, reverse):
    """"
    Performs insertion sort on given list in range of indices: start and end
    :param unsorted: the list to sort
    :param start: start index of range of values in list
    :param end: end index of range of values in list
    :param reverse: if reverse = false list is sorted ascending otherwise sorted descending
    """""
    # TIME COMPLEXITY: O(n^2)
    if len(unsorted) == 0:
        return start

    if len(unsorted) == 1:
        return start

    if reverse is True:
        for i in range(start, end + 1):
            start = i
            while (start > 0) and (unsorted[start] > unsorted[start - 1]):
                exchange(unsorted, start, start - 1)
                start = start - 1
    else:
        for i in range(start, end + 1):
            start = i
            while (start > 0) and (unsorted[start] < unsorted[start-1]):
                exchange(unsorted, start, start-1)
                start = start - 1


def largest_sequential_difference(lst):
    """"
    Finds largest sequential difference between values in sorted list
    :param lst: the list to sort and find sequential difference
    """""
    # TIME COMPLEXITY: O(nlog(n))
    start = 0
    end = len(lst) - 1
    threshold = 0
    temp_diff = 0

    if (end-start + 1) < 2:
        return None

    quick_sort(lst, threshold, start, end, False)
    for i in range(0, len(lst)-1):
        seq_diff = lst[i+1] - lst[i]
        if seq_diff > temp_diff:
            temp_diff = seq_diff
    return temp_diff

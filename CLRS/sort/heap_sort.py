import random


def max_heapify(heap, heap_size, root):
    left = root*2+1
    right = left+1
    larger = root
    if left < heap_size and heap[left] > heap[larger]:
        larger = left
    if right < heap_size and heap[right] > heap[larger]:
        larger = right
    if root != larger:
        heap[root], heap[larger] = heap[larger], heap[root]
        max_heapify(heap, heap_size, larger)


def heap_sort(heap):
    heap_size = len(heap)
    for root in range(heap_size//2-1, -1, -1):
        max_heapify(heap, heap_size, root)
    for i in range(heap_size-1, -1, -1):
        heap[0], heap[i] = heap[i], heap[0]
        max_heapify(heap, i, 0)


if __name__ == '__main__':
    heap = [random.randint(0, 1000) for i in range(10)]
    print(heap)
    heap_sort(heap)
    print(heap)


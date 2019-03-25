import random


def max_heapify(heap, heap_size, root):
    # 构建最大堆
    left = root*2+1
    right = left+1
    larger = root
    # 比较根节点与子节点的值，将最大的元素放于根节点
    if left < heap_size and heap[left] > heap[larger]:
        larger = left
    if right < heap_size and heap[right] > heap[larger]:
        larger = right
    if root != larger:
        heap[root], heap[larger] = heap[larger], heap[root]
        max_heapify(heap, heap_size, larger)


def heap_sort(heap):
    heap_size = len(heap)
    # 对每个根节点都构建最大堆，从最底层开始
    for root in range(heap_size//2-1, -1, -1):
        max_heapify(heap, heap_size, root)
    # 将根节点与数组最后元素交换位置
    for i in range(heap_size-1, -1, -1):
        heap[0], heap[i] = heap[i], heap[0]
        # 堆剩余元素继续构建最大堆
        max_heapify(heap, i, 0)


if __name__ == '__main__':
    heap = [random.randint(0, 1000) for i in range(10)]
    print(heap)
    heap_sort(heap)
    print(heap)


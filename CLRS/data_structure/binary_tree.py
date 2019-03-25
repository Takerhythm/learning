class Node:
    def __init__(self, val=None, left_child=None, right_child=None):
        self.val = val
        self.left_child = left_child
        self.right_child = right_child

class BinaryTree:
    def __init__(self):
        self.root = Node()

    def add(self, val):
        if self.root.val is None:
            self.root.val = val
        else:
            new_node = Node(val)
            queue = [self.root]
            while queue:
                cur = queue.pop(0)
                if not cur.left_child:
                    cur.left_child = new_node
                    return
                if not cur.right_child:
                    cur.right_child = new_node
                    return
                queue.append(cur.left_child)
                queue.append(cur.right_child)

    def travel(self):
        if self.root.val is None:
            return
        queue = [self.root]
        res = []
        while queue:
            cur = queue.pop(0)
            res.append(cur.val)
            if cur.left_child:
                queue.append(cur.left_child)
            if cur.right_child:
                queue.append(cur.right_child)
        return res

    def pre_order(self, root):
        if root is None:
            return
        print(root.val)
        self.pre_order(root.left_child)
        self.pre_order(root.right_child)

    def in_order(self, root):
        if root is None:
            return
        self.in_order(root.left_child)
        print(root.val)
        self.in_order(root.right_child)

    def post_order(self, root):
        if root is None:
            return
        self.post_order(root.left_child)
        self.post_order(root.right_child)
        print(root.val)

    def max_depth(self, root):
        if root is None:
            return 0
        return max(self.max_depth(root.left_child), self.max_depth(root.right_child)) + 1

    def pre_order_stack(self, root):
        if not root:
            return
        stack = []
        res = []
        cur = root
        while stack or cur:
            while cur:
                res.append(cur.val)
                stack.append(cur)
                cur = cur.left_child
            cur = stack.pop()
            cur = cur.right_child
        return res

    def in_order_stack(self, root):
        if not root:
            return
        stack = []
        res = []
        cur = root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left_child
            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right_child
        return res

    def post_order_stack(self, root):
        if not root:
            return
        stack1 = []
        stack2 = []
        cur = root
        while stack1 or cur:
            while cur:
                stack2.append(cur)
                stack1.append(cur)
                cur = cur.right_child
            cur = stack1.pop()
            cur = cur.left_child
        res = []
        while stack2:
            res.append(stack2.pop().val)
        return res

    def invert_tree(self, root):
        if root is None:
            return None
        root.left_child, root.right_child = self.invert_tree(root.right_child), self.invert_tree(root.left_child)
        return root

    def construct_tree_by_pre(self, pre_order, in_order):
        if len(pre_order) == 0:
            return None
        root_val = pre_order[0]
        i = in_order.index(root_val)
        left = self.construct_tree_by_pre(pre_order[1: 1 + i], in_order[:i])
        right = self.construct_tree_by_pre(pre_order[1 + i:], in_order[i + 1:])
        return Node(root_val, left, right)

    def construct_tree_by_post(self, post_order, in_order):
        if len(post_order) == 0:
            return None
        root_val = post_order[-1]
        i = in_order.index(root_val)
        left = self.construct_tree_by_post(post_order[: i], in_order[:i])
        right = self.construct_tree_by_post(post_order[i:-1], in_order[i + 1:])
        return Node(root_val, left, right)

    def get_leaf_nums(self):
        if self.root.val is None:
            return 0
        queue = [self.root]
        leaf_nums = 0
        while queue:
            cur = queue.pop(0)
            leaf_nums += 1
            if cur.left_child:
                queue.append(cur.left_child)
            if cur.right_child:
                queue.append(cur.right_child)
        return leaf_nums


if __name__ == '__main__':
    tree = BinaryTree()
    for val in range(10):
        tree.add(val)
    print(tree.travel())
    print('前序遍历')
    tree.pre_order(tree.root)
    print('中序遍历')
    tree.in_order(tree.root)
    print('后序遍历')
    tree.post_order(tree.root)
    print('二叉树最大深度')
    print(tree.max_depth(tree.root))
    print('前序遍历——非递归实现')
    print(tree.pre_order_stack(tree.root))
    print('中序遍历——非递归实现')
    print(tree.in_order_stack(tree.root))
    print('后序遍历——非递归实现')
    print(tree.post_order_stack(tree.root))
    print('翻转二叉树')
    tree.invert_tree(tree.root)
    print(tree.travel())
    print('根据前序，中序遍历恢复一棵树')
    pre_order = tree.pre_order_stack(tree.root)
    in_order = tree.in_order_stack(tree.root)
    post_order = tree.post_order_stack(tree.root)
    node = tree.construct_tree_by_pre(pre_order, in_order)
    new_tree = BinaryTree()
    new_tree.root = node
    print(new_tree.travel())
    print('根据后序，中序遍历恢复一棵树')
    node = tree.construct_tree_by_post(post_order, in_order)
    new_tree.root = node
    print(new_tree.travel())
    print('节点数')
    print(tree.get_leaf_nums())

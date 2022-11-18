from copy import copy
class Node:
    def __init__(self, L=None, R=None):
        self.L = L
        self.temp = None
        self.R = R
class createTreeItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.lc = None
        self.rc = None

class TwoThreeTree:
    def __init__(self):
        self.root = Node()
        self.size = 0
        self.height = 0

    def isEmpty(self):
        if self.size == 0:
            return True
        else:
            return False

    def full(self, node):
        if node is None:
            return False
        if node.L is None or node.R is None:
            return False
        return True

    def parentNode(self, item):
        parent = None
        node = self.root
        while True:
            if node is None:
                return parent
            if node.L.key == item.key:
                return parent
            if node.R is not None:
                if node.R.key == item.key:
                    return parent
            if item.key < node.L.key:
                parent = node
                node = node.L.lc
            elif node.L.key < item.key and node.R is None:
                parent = node
                node = node.L.rc
            elif node.L.key < item.key < node.R.key:
                parent = node
                node = node.L.rc
            else:
                parent = node
                node = node.R.rc

    def split(self, current):
        if self.root == current:
            current.temp.lc = Node(current.L)
            current.temp.rc = Node(current.R)
            self.root.R = None
            self.root.L = current.temp
            self.root.temp = None
            self.height += 1
            return
        else:
            parent = self.parentNode(current.L)
            current.temp.lc = Node(current.L)
            current.temp.rc = Node(current.R)
            if current.temp.key < parent.L.key:
                if parent.R is None:
                    parent.R = parent.L
                    parent.L = current.temp
                    parent.R.lc = parent.L.rc
                    return
                else:
                    parent.temp = parent.L
                    parent.L = current.temp
                    parent.temp.lc = parent.L.rc
                    self.split(parent)

            elif parent.L.key < current.temp.key:
                if parent.R is None:
                    parent.R = current.temp
                    parent.L.rc = parent.R.lc
                    return
                else:
                    parent.temp = parent.R
                    parent.R = current.temp
                    parent.temp.rc = parent.R.lc
                    self.split(parent)

    def retrieveItem(self, key):
        current = self.root
        if current is None:
            return None, False, None
        i = 0
        while i < self.size:
            i+=1
            if current.L.key == key:
                return current.L.key, True, current
            elif current.R is not None:
                if current.R.key == key:
                    return current.R.key, True, current
            if key < current.L.key:
                if current.L.lc is None:
                    return None, False, current
                else:
                    current = current.L.lc
            elif current.L.key < key and current.R is None:
                if current.L.rc is None:
                    return None, False, current
                else:
                    current = current.L.rc
            elif current.R is not None:
                if current.L.key < key < current.R.key:
                    if current.L.rc is None:
                        return None, False, current
                    else:
                        current = current.L.rc
                else:
                    if current.L.rc is None:
                        return None, False, current
                    else:
                        current = current.R.rc

    def insertItem(self, item):
        if self.root.L is None and self.root.R is None:
            self.root.L = item
            self.size += 1
            self.height += 1
            return True
        elif self.root.L is not None and self.root.R is None:
            if self.root.L.lc is not None or self.root.L.rc is not None:
                pass
            elif self.root.L.key > item.key:
                self.root.R = self.root.L
                self.root.L = item
                self.size += 1
                return True
            else:
                self.root.R = item
                self.size += 1
                return True
        if self.root.R is not None and self.root.L is None:
            if self.root.R.lc is not None or self.root.R.rc is not None:
                pass
            elif self.root.R.key < item.key:
                self.root.L = self.root.R
                self.root.R = item
                self.size += 1
                return True
            else:
                self.root.L = item
                self.size += 1
                return True
        if self.root.L is not None and self.root.R is not None:
            if self.root.R.lc is not None or self.root.R.rc is not None or self.root.L.lc is not None or self.root.L.rc is not None:
                pass
            elif self.height == 1:
                if item.key < self.root.L.key:
                    self.root.temp = self.root.L
                    self.root.L = item
                    self.size += 1
                elif self.root.L.key < item.key < self.root.R.key:
                    self.root.temp = item
                    self.size += 1
                else:
                    self.root.temp = self.root.R
                    self.root.R = item
                    self.size += 1
                self.split(self.root)
                return True

        node = self.retrieveItem(item.key)[2]
        if self.retrieveItem(item.key)[0] is not None:
            return False
        if item.key < node.L.key and node.R is None:
            node.R = node.L
            node.L = item
            self.size += 1
            return True
        elif item.key < node.L.key:
            node.temp = node.L
            node.L = item
            self.size += 1
            self.split(node)
            return True
        elif node.L.key < item.key and node.R is None:
            node.R = item
            self.size += 1
            return True
        elif node.L.key < item.key < node.R.key:
            node.temp = item
            self.size += 1
            self.split(node)
            return True
        elif node.R.key < item.key:
            node.temp = node.R
            node.R = item
            self.size += 1
            self.split(node)
            return True

    def inorderSuccesor(self, key):
        if self.retrieveItem(key) is False:
            return None
        node = self.retrieveItem(key)[2]
        if key == node.L.key:
            item = node.L
        else:
            item = node.R

        if item.rc is not None:
            item = item.rc.L
            while item.lc is not None:
                item = item.lc.L
        return item

    def MR(self, node):  # merge en redistribute
        print(node.L.rc)
        if self.full(node):
            if node.L.lc is None:
                node.R.lc.R = node.R.lc.L
                node.L.rc = None
                node.R.lc.L = node.L
                node.L = node.R
                node.R = None
            elif node.L.rc is None:
                node.R.lc = node.L.lc
                node.L.lc = None
                node.R.lc.R = node.L
                node.L = node.R
                node.R = None
            elif node.R.rc is None:
                node.L.rc = node.L.rc
                node.R.lc = None
                node.L.rc.R = node.R
                node.R = None
        elif self.full(node.L.lc) and node.L.rc is None:
            temp = copy(node.L)
            temp0 = copy(node.L.lc)
            temp0.R = None
            node.L = node.L.lc.R
            node.L.rc = Node(temp)
            node.L.rc.L.lc = None
            node.L.lc = temp0
            print(node.L.key)
            print(node.L.lc.L.key)
            print(node.L.rc.L.key)
        elif self.full(node.L.rc):
            temp = copy(node.L)
            temp0 = copy(node.L.rc)
            temp0.L = temp0.R
            temp0.R = None
            node.L = node.L.rc.L
            node.L.lc = Node(temp)
            node.L.lc.L.rc = None
            node.L.rc = temp0
        elif node.L.lc is None:
            return
        elif node.L.rc is None:
            parent = self.parentNode(node)
            node.L.lc.R = node.L
            node.L.lc.R.lc = None
            print(node.L.key)
            self.MR(parent)
        return

    def deleteItem(self, key):
        if not self.retrieveItem(key)[1]:
            return False
        node = self.retrieveItem(key)[2]
        parent = self.parentNode(node.L)
        inorder = self.inorderSuccesor(key)
        inorderNode = self.retrieveItem(inorder.key)[2]
        inorderParent = self.parentNode(inorder)
        if inorder.key == key and parent is None:
            if self.root.R is None:
                self.root.L = None
                self.height -= 1
            elif self.root.L.key == key:
                self.root.L = self.root.R
                self.root.R = None
            else:
                self.root.R = None
            self.size -= 1
            return True
        elif inorder.key == key:
            if node.R is None:
                node.L = None
                if key < parent.L.key:
                    parent.L.lc = None
                elif parent.L.key < key and parent.R is None:
                    parent.L.rc = None
                elif parent.R is not None:
                    if parent.L.key < key < parent.R.key:
                        parent.L.rc = None
                        parent.R.lc = None
                    elif parent.R.key < key:
                        parent.R.rc = None
                self.MR(parent)
            elif node.L.key == key:
                node.L = node.R
                node.R = None
            else:
                node.R = None
            self.size -= 1
            return True
        elif node.L.key == key:
            temp = node.L.key
            node.L.key = inorder.key
            inorder.key = temp
            if inorderNode.R is None:
                inorderNode.L = None
                inorderParent.L.rc = None
                self.MR(inorderParent)
            elif inorderNode.L.key == temp:
                inorderNode.L = inorderNode.R
                inorderNode.R = None
            else:
                inorderNode.R = None
        elif node.R is not None and node.R.key == key:
            temp = node.R.key
            iKey = inorder.key
            node.R.key = inorder.key
            inorder.key = temp
            if inorderNode.R is None:
                inorderNode.L = None
                inorderParent.R.rc = None
                self.MR(inorderParent)
            elif inorderNode.L.key == key:
                inorderNode.L = inorderNode.R
                inorderNode.R = None
            else:
                inorderNode.R = None
        self.size -= 1
        return True

    def inorderTraverse(self, callback=None):
        current = self.root
        traversed = []
        if current is None:
            return traversed
        current = current.L
        while len(traversed) != self.size:
            if current.lc is not None and current.lc.L.key not in traversed:
                current = current.lc.L

            elif current.key not in traversed:
                traversed.append(current.key)
                if current.rc is not None and current.rc.L.key not in traversed:
                    current = current.rc.L
                elif current.key != self.root.L.key and self.root.R is None:
                    current = self.parentNode(current).L
                elif current.key != self.root.L.key and current.key != self.root.R.key:
                    current = self.parentNode(current).L


            elif current.key in traversed and current.key != self.root.L.key:
                temp = self.retrieveItem(current.key)[2]
                if temp.R is not None and current.key in traversed:
                    current = temp.R
                else:
                    current = self.parentNode(current).L

            elif current.key in traversed and current.key == self.root.L.key:
                current = self.root.R

        if callback is not None:
            for i in traversed:
                print(i)
        return

    def recursiveSave(self, current):
        r = "root"
        c = "children"
        lchild = {}
        MidChild = {}
        rchild = {}

        if current.R is None:
            if current.L.lc is not None and current.L.rc is not None:
                if current.L.lc.R is not None:
                    lchild[r] = [current.L.lc.L.key, current.L.lc.R.key]
                else:
                    lchild[r] = [current.L.lc.L.key]
                if current.L.rc.R is not None:
                    rchild[r] = [current.L.rc.L.key, current.L.rc.R.key]
                else:
                    rchild[r] = [current.L.rc.L.key]
                if current.L.lc.L.lc or current.L.lc.L.rc is not None:
                    lchild[c] = self.recursiveSave(current.L.lc)
                else:
                    return [lchild, rchild]

                if current.L.rc.L.lc or current.L.rc.L.rc is not None:
                    rchild[c] = self.recursiveSave(current.L.rc)
                else:
                    return [lchild, rchild]

            elif current.L.lc is not None:
                lchild[r] = current.lc.key
                rchild = None
                if current.lc.lc or current.lc.rc is not None:
                    lchild[c] = self.recursiveSave(current.lc)
                else:
                    return [lchild, rchild]

            elif current.L.rc is not None:
                lchild = None
                rchild[r] = current.L.rc.L.key
                if current.L.rc.L.lc or current.L.rc.L.rc is not None:
                    rchild[c] = self.recursiveSave(current.L.rc)
                else:
                    return [lchild, rchild]
            return [lchild, rchild]
        else:
            if current.L.lc is not None and current.L.rc is not None and current.R.lc is not None and current.R.rc is not None:
                if current.L.lc.R is not None:
                    lchild[r] = [current.L.lc.L.key, current.L.lc.R.key]
                else:
                    lchild[r] = [current.L.lc.L.key]
                if current.L.rc.R is not None:
                    MidChild[r] = [current.L.rc.L.key, current.L.rc.R.key]
                else:
                    MidChild[r] = [current.L.rc.L.key]
                if current.R.rc.R is not None:
                    rchild[r] = [current.R.rc.L.key, current.R.rc.R.key]
                else:
                    rchild[r] = [current.R.rc.L.key]
                if current.L.lc.L.lc or current.L.lc.L.rc is not None:
                    lchild[c] = self.recursiveSave(current.L.lc)
                else:
                    return [lchild, MidChild, rchild]

                if current.L.rc.L.lc or current.L.rc.L.rc is not None:
                    MidChild[c] = self.recursiveSave(current.L.rc)
                else:
                    return [lchild, MidChild, rchild]
                if current.R.rc.L.lc or current.R.rc.L.rc is not None:
                    rchild[c] = self.recursiveSave(current.R.rc)
                else:
                    return [lchild, MidChild, rchild]

            elif current.L.lc is not None:
                lchild[r] = current.L.lc.L.key
                MidChild = None
                rchild = None
                if current.L.lc.L.lc or current.L.lc.L.rc is not None:
                    lchild[c] = self.recursiveSave(current.L.lc)
                else:
                    return [lchild, MidChild, rchild]

            elif current.L.rc is not None:
                lchild = None
                MidChild = None
                rchild[r] = current.L.rc.L.key
                if current.L.rc.L.lc or current.L.rc.L.rc is not None:
                    rchild[c] = self.recursiveSave(current.L.rc)
                else:
                    return [lchild, MidChild, rchild]
            return [lchild, MidChild, rchild]

    def save(self):
        current = self.root

        r = "root"
        c = "children"
        d = {}
        if current.L is None:
            return d
        if current.R is not None:
            d[r] = [current.L.key, current.R.key]
        else:
            d[r] = [current.L.key]
        if current.L.lc is not None or current.L.rc is not None or current.R.lc is not None or current.R.rc is not None:
            d[c] = self.recursiveSave(current)

        return d

    def loadHelp(self, savedTree):
        for i in savedTree:

            if type(savedTree.get(i)[0]) == int:
                self.insertItem(createTreeItem(savedTree.get(i)[0], savedTree.get(i)[0]))
            else:
                self.loadHelp(savedTree.get(i)[0])
            if len(savedTree.get(i)) > 1:
                if type(savedTree.get(i)[1]) == int:
                    self.insertItem(createTreeItem(savedTree.get(i)[1], savedTree.get(i)[1]))
                else:
                    self.loadHelp(savedTree.get(i)[1])

    def load(self, savedTree):
        for k in range(self.size):
            self.deleteItem(self.root.L.key)
        self.loadHelp(savedTree)

"""
t = TwoThreeTree()
print(t.isEmpty())
print(t.insertItem(createTreeItem(8, 8)))
print(t.insertItem(createTreeItem(5, 5)))
print(t.isEmpty())
print(t.retrieveItem(5)[0])
print(t.retrieveItem(5)[1])
t.inorderTraverse(print)
print(t.save())
t.load({'root': [10], 'children': [{'root': [5]}, {'root': [11]}]})
print(t.save())
print(t.insertItem(createTreeItem(15, 15)))
print(t.deleteItem(0))
print(t.save())
print(t.deleteItem(10))
print(t.save())
"""

t = TwoThreeTree()
t.root.L = createTreeItem(50, 50)
t.root.L.lc = Node(createTreeItem(30, 30))
t.root.L.lc.L.lc = Node(createTreeItem(10, 10), createTreeItem(20, 20))
t.root.L.lc.L.rc = Node(createTreeItem(40, 40))
t.root.L.rc = Node(createTreeItem(80, 80))
t.root.L.rc.L.lc = Node(createTreeItem(60, 60))
t.root.L.rc.L.rc = Node(createTreeItem(90, 90))
t.size = 8
print(t.save())
print(t.deleteItem(80))
print(t.save())

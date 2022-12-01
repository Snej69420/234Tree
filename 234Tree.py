from copy import deepcopy


class createTreeItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Node:
    def __init__(self):
        self.numI = 0
        self.numC = 0
        self.items = []
        self.kids = []
        self.parent = None

    def isEmpty(self):
        return self.numI == 0

    def isFull(self):
        return self.numI == 3

    def isLeaf(self):
        return self.numC == 0

    def find(self, key):
        j = 0
        for i in self.items:
            if i.key == key:
                return i, True, j
            j += 1
        return None, False, -1

    def findKid(self, key):
        for i in self.kids:
            if i.key == key:
                return i, True
        return None, False

    def insert(self, treeItem):
        if self.isFull():
            print("You fucked something up")
            return False

        if self.isEmpty():
            self.items.insert(0, treeItem)
            self.numI += 1
            return True

        index = 0
        for i in self.items:
            if treeItem.key < i.key:
                break
            index += 1

        self.items.insert(index, treeItem)
        self.numI += 1
        return True

    def addKid(self, node):
        if node.isEmpty():
            print("You fucked something up")
            return False

        if self.numC == 0:
            self.kids.insert(0, node)
            self.numC += 1
            return True

        index = 0
        for i in self.kids:
            if node.items[node.numI - 1].key < i.items[0].key:
                break
            index += 1

        self.kids.insert(index, node)
        self.numC += 1
        return True

    def removeKid(self, index):
        if index >= self.numC:
            return False
        self.kids.pop(index)
        self.numC -= 1
        True

    def delete(self, key):
        index = 0
        found = False
        for i in self.items:
            if i.key == key:
                found = True
                break
            index += 1

        if found:
            self.items.pop(index)
            self.numI -= 1
            return True
        return False

    def simpleDelete(self, index):
        if index >= self.numI:
            return False
        self.items.pop(index)
        self.numI -= 1
        return True

    def display(self):
        if self.isEmpty():
            return ""

        temp = "{'root': ["
        for i in self.items:
            temp += str(i.key) + ", "

        temp = temp[:-1]
        temp = temp[:-1]
        temp += "], 'children': ["
        for kid in self.kids:
            temp += kid.display()
        temp += "]}"
        return temp


class TwoThreeFourTree:
    def __init__(self):
        self.root = None

    def isEmpty(self):
        if self.root is None:
            return True
        return False

    def findItem(self, key):
        if self.root is None:
            return None, False

        current = self.root

        while True:
            if current.find(key)[1]:
                return current.find(key)

            if current.isLeaf():
                return None, False

            kids = current.kids
            for i in kids:
                if i.find(key)[1]:
                    return i.find(key)
                for j in i.items:
                    current = i
                    if key < j.key:
                        break

    def inorderSuccesor(self, key):
        temp = self.findItem(key)
        if not temp[1]:
            return None, False

        node = temp[0]
        index = node.find(key)[2]
        current = node.kids[index+1]
        while not current.isLeaf():
            current = current.kids[0]
        IS = current.items[0]
        t = node.items[index]
        node.items[index] = IS
        IS = t
        self.deleteItem(key)

    def insertIn(self, key, split=True):
        if self.findItem(key)[1]:
            print("There is already an item with this key!")
            return None

        current = self.root
        while True:
            if current.isFull() and split:
                self.split(current)
                return self.insertIn(key, False)

            if current.isLeaf():
                return current

            kids = current.kids
            parent = current
            for j in parent.items:
                for i in kids:
                    current = i
                    if key < i.items[i.numI-1].key or key < j.key:
                        break

    def retrieveItem(self, key):
        if self.findItem(key)[1]:
            return self.findItem(key)[0].key, self.findItem(key)[1]
        return None, False

    def split(self, node):
        if node.parent is None:  # split root
            newRoot = Node()
            newRoot.insert(node.items[1])
            rightNode = Node()
            rightNode.insert(node.items[2])
            rightNode.parent = newRoot
            kids = node.kids.copy()
            node.kids = []
            node.parent = newRoot
            node.simpleDelete(2)
            node.simpleDelete(1)
            newRoot.addKid(node)
            newRoot.addKid(rightNode)
            self.root = newRoot
        else:
            parent = node.parent
            parent.insert(node.items[1])
            rightNode = Node()
            rightNode.insert(node.items[2])
            rightNode.parent = parent
            kids = node.kids.copy()
            node.kids = []
            node.simpleDelete(2)
            node.simpleDelete(1)
            parent.addKid(rightNode)
        for i in kids:
            if i.items[i.numI - 1].key < node.items[0].key:
                node.addKid(i)
            if node.items[node.numI - 1].key < i.items[i.numI - 1].key < rightNode.items[0].key:
                rightNode.addKid(i)
                node.addKid(i)
            if rightNode.items[0].key < i.items[i.numI - 1].key:
                rightNode.addKid(i)
        return

    def insertItem(self, treeItem):
        if self.root is None:
            self.root = Node()

        current = self.root
        if current.isFull():
            self.split(current)
            return self.insertItem(treeItem)

        node = self.insertIn(treeItem.key)
        if node is None:
            return False
        return node.insert(treeItem)

    def merge0(self, node):
        kid0 = node.kids[0]
        kid1 = node.kids[1]
        if kid0.numI == 1 and kid1.numI == 1:
            kid0.parent = node.parent
            kid1.parent = node.parent
            node.insert(kid0.item[0])
            node.insert(kid1.item[0])
            node.removeKid(1)
            node.removeKid(0)
            for i in kid0.kids:
                node.addKid(i)
            for j in kid1.kids:
                node.addKid(j)
            return True
        return False

    def merge1(self, node):
        parent = node.parent
        index = -1
        j = 0
        if parent.numI == 2 or parent.numI == 3:
            parentItem = None
            parentKid = None
            parentKid0 = None
            parentKid1 = None
            for i in parent.kids:
                if i.find(node.key):
                    index = j
                    break
                j += 1
            found = False
            if index - 1 >= 0:
                parentKid0 = parent.kids[index - 1]
                found = True
            if index + 1 < parent.numC:
                parentKid1 = parent.kids[index + 1]
                found = True
            if not found:
                return False

            if parentKid0 is not None and parentKid0.numI == 1:
                parentItem = parent.items[0]
                parent.simpleDelete(0)
                parent.removeKid(index-1)
                parentKid = parentKid0
            elif parentKid1 is not None and parentKid1.numI == 1:
                parentItem = parent.items[1]
                parent.simpleDelete(1)
                parent.removeKid(index+1)
                parentKid = parentKid1
            else:
                return False
            parent.removeKid(index)
            newNode = Node()
            newNode.insert(node.items[0])
            newNode.insert(parentItem)
            newNode.insert(parentKid.items[0])
            newNode.parent = parent
            parent.addKid(newNode)
            for i in node.kids:
                newNode.addKid(i)
            for i in parentKid.kids:
                newNode.addKid(i)

    def merge(self, node):
        if self.merge0(node):
            return True
        if self.merge1(node):
            return True
        return False

    def redistribute(self, node):
        sibling0, sibling1 = None
        chosenOne = None
        parent = node.parent
        index = -1
        j = 0
        for k in parent.kids:
            if k == node:
                index = j
                break
            j += 1
        if index-1 >= 0:
            sibling0 = parent.kids[index-1]
        if index+1 < parent.numC:
            sibling1 = parent.kids[index+1]

        if sibling0 is not None and sibling0.numI > 1:
            chosenOne = sibling0
        elif sibling1 is not None and sibling1.numI > 1:
            chosenOne = sibling1
        elif parent.numI > 1:
            sibling = None
            if sibling0 is not None:
                sibling = sibling0
            elif sibling1 is not None:
                sibling = sibling1
            else:
                return False

            # path 2
            newNode = Node()
        else:
            return False



    def deleteItem(self, key):
        if self.root is None:
            return False
        node = self.findItem(key)
        if not node[1]:
            return False
        if node.numI >= 2 and node.isLeaf():
            return node.delete(key)
        return node.delete(key)

    def save(self):
        current = self.root
        return current.display()

    def recIO(self, root, callback):
        if root is None:
            return
        leaf = root.isLeaf()
        for j in range(0, root.numC-1):
            self.recIO(root.kids[j], callback)
            callback(root.items[j].value)
        if not leaf:
            self.recIO(root.kids[root.numC-1], callback)
        if leaf:
            for j in root.items:
                callback(j.value)

    def inorderTraverse(self, callback):
        self.recIO(self.root, callback)

    def recLoad(self, root, saved):
        for items in saved:
            newNode = Node()
            for j in items['root']:
                newNode.insert(createTreeItem(j, j))
            newNode.parent = root
            root.addKid(newNode)
            if 'children' not in items:
                continue
            self.recLoad(newNode, items['children'])

    def load(self, saved):
        newRoot = Node()
        items = saved['root']
        for i in items:
            newRoot.insert(createTreeItem(i, i))
        self.root = newRoot
        self.recLoad(newRoot, saved['children'])


"""
T = TwoThreeFourTree()
print(T.insertItem(createTreeItem(666, 666)))
print(T.insertItem(createTreeItem(69, 69)))
print(T.insertItem(createTreeItem(420, 420)))
print(T.save())
print(T.insertItem(createTreeItem(1, 1)))
print(T.insertItem(createTreeItem(6, 6)))
print(T.insertItem(createTreeItem(999, 999)))
print(T.insertItem(createTreeItem(69420, 69420)))
print(T.save())
print(T.insertItem(createTreeItem(1000, 1000)))
print(T.save())
print(T.insertItem(createTreeItem(3, 3)))
print(T.save())
"""

t = TwoThreeFourTree()
print(t.isEmpty())
print(t.insertItem(createTreeItem(8, 8)))
print(t.insertItem(createTreeItem(5, 5)))
print(t.insertItem(createTreeItem(10, 10)))
print(t.insertItem(createTreeItem(15, 15)))
print(t.isEmpty())
print(t.retrieveItem(5)[0])
print(t.retrieveItem(5)[1])
t.inorderTraverse(print)
print(t.save())
t = None
t = TwoThreeFourTree()
t.load({'root': [10], 'children': [{'root': [5]}, {'root': [11]}]})
print(t.save())
t.insertItem(createTreeItem(15, 15))
print(t.save())
# print(t.deleteItem(0))
# print(t.save())
# print(t.deleteItem(10))
# print(t.save())


"""
    True
    True
    True
    True
    True
    False
    5
    True
    5
    8
    10
    15
    {'root': [8], 'children': [{'root': [5]}, {'root': [10, 15]}]}
    False
    {'root': [10], 'children': [{'root': [5]}, {'root': [11, 15]}]}
    True
    {'root': [11], 'children': [{'root': [5]}, {'root': [15]}]}
"""

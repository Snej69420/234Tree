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
        for i in self.items:
            if i.key == key:
                return i, True
        return None, False

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
                    if key < j.key:
                        current = i
                        break

    def insertIn(self, key):
        if self.findItem(key)[1]:
            print("There is already an item with this key!")
            return None

        current = self.root

        while True:
            if current.isFull():
                self.split(current)
                return self.insertIn(key)

            if current.isLeaf():
                return current

            kids = current.kids
            for i in kids:
                if key < i.items[i.numI-1].key:
                    current = i
                    break

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
            for i in kids:
                if i.items[i.numI - 1] < node.items[0]:
                    node.addKid(i)
                if node.items[node.numI - 1] < i.items[i.numI - 1] < newRoot.items[0]:
                    newRoot.addKid(i)
                    node.addKid(i)
            self.root = newRoot

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

    def deleteItem(self, key):
        if self.root is None:
            return False
        node = self.findItem(key)
        return node.delete(key)

    def save(self):
        current = self.root
        return current.display()


T = TwoThreeFourTree()
print(T.insertItem(createTreeItem(666, 666)))
print(T.insertItem(createTreeItem(69, 69)))
print(T.insertItem(createTreeItem(420, 420)))
print(T.save())
print(T.insertItem(createTreeItem(1, 1)))
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
t.load({'root': [10], 'children': [{'root': [5]}, {'root': [11]}]})
t.insertItem(createTreeItem(15, 15))
print(t.deleteItem(0))
print(t.save())
print(t.deleteItem(10))
print(t.save())

"""
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

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

    def split(self):
        pass

    def display(self):
        if self.isEmpty():
            return

        temp = "("
        for i in self.items:
            temp += str(i.key) + ", "

        temp = temp[:-1]
        temp = temp[:-1]
        temp += ")"
        print(temp)



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

            for i in current.kids:
                if key <= i.key:
                    current = i
                    break


    def insertItem(self, treeItem):
        if self.root is None:
            self.root = Node()

        current = self.root
        if current.isFull():
            current.split()

        return self.root.insert(treeItem)

    def deleteItem(self, key):
        if self.root is None:
            return False
        return self.root.delete(key)

    def display(self):
        current = self.root
        current.display()


T = TwoThreeFourTree()
print(T.insertItem(createTreeItem(666, 666)))
print(T.insertItem(createTreeItem(69, 69)))
print(T.insertItem(createTreeItem(420, 420)))
T.display()
print(T.deleteItem(420))
T.display()
print(T.deleteItem(69))
T.display()
print(T.deleteItem(666))
T.display()


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
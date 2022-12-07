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

    def insert(self, treeItem: createTreeItem):
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
        if node is None:
            return False
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
        if index >= self.numC or index < 0:
            return False
        temp = self.kids[index]
        self.kids.pop(index)
        self.numC -= 1
        return True

    def removeAllKids(self):
        if self.numC == 0:
            return
        self.kids.pop(0)
        self.numC -= 1
        return self.removeAllKids()

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
        if index >= self.numI or index < 0:
            return None, False
        temp = self.items[index]
        self.items.pop(index)
        self.numI -= 1
        return temp, True

    def display(self, root=False):
        insert = ""
        if root:
            insert = " "
        if self.isEmpty():
            return ""

        temp = "{'root':" + insert + "["
        for i in self.items:
            temp += str(i.key) + ","

        temp = temp[:-1]
        temp += "]"
        if self.numC > 0:
            temp += ",'children':["
            for kid in self.kids:
                temp += kid.display() + ","
            temp = temp[:-1]
            temp += "]"
        temp += "}"
        return temp

    def spares(self, index):
        if index < 0 or index >= self.numC:
            return False
        return self.kids[index].numI > 1


class TwoThreeFourTree:
    def __init__(self):
        self.root = None

    def isEmpty(self):
        if self.root is None:
            return True
        return False

    def findItem(self, key):
        if self.root is None:
            return None, False, -1

        current = self.root

        while True:
            if current.find(key)[1]:
                return current, True, current.find(key)[2]

            if current.isLeaf():
                return None, False, -1

            kids = current.kids
            for i in kids:
                if i.find(key)[1]:
                    return i, True, i.find(key)[2]
                for j in i.items:
                    current = i
                    if key < j.key:
                        break

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
            j = 0
            found = False
            for i in parent.items:
                if key < i.key:
                    current = parent.kids[j]
                    found = True
                    break
                j += 1
            if not found:
                current = parent.kids[j]

    def retrieveItem(self, key):
        if self.findItem(key)[1]:
            return self.findItem(key)[0].find(key)[0].key, self.findItem(key)[1]
        return None, False

    def split(self, node: Node):
        kids = node.kids.copy()
        parent = None
        if node.parent is None:  # split root
            newRoot = Node()
            newRoot.insert(node.simpleDelete(1)[0])
            rightNode = Node()
            rightNode.insert(node.simpleDelete(1)[0])
            rightNode.parent = newRoot
            node.removeAllKids()
            node.parent = newRoot
            newRoot.addKid(node)
            newRoot.addKid(rightNode)
            self.root = newRoot
            parent = self.root
        else:
            parent = node.parent
            parent.insert(node.simpleDelete(1)[0])
            rightNode = Node()
            rightNode.insert(node.simpleDelete(1)[0])
            rightNode.parent = parent
            node.removeAllKids()
            parent.addKid(rightNode)
        for i in parent.items:
            for j in kids:
                if j.items[j.numI - 1].key < i.key:
                    node.addKid(j)
                else:
                    rightNode.addKid(j)

        return

    def insertItem(self, treeItem: createTreeItem):
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

    def check(self, node: Node):
        if node.numI > 1:
            return

        parent = node.parent
        index = -1
        j = 0
        for i in parent.kids:
            if i == node:
                index = j
                break
            j += 1

        if parent.spares(index - 1):
            tempNode = parent.kids[index - 1]
            node.insert(parent.simpleDelete(index - 1)[0])
            if 0 < tempNode.numC:
                kid = tempNode.kids[tempNode.numC - 1]
                tempNode.removeKid(tempNode.numC - 1)
                node.addKid(kid)
            parent.insert(tempNode.simpleDelete(tempNode.numI - 1)[0])
            return

        if parent.spares(index + 1):
            tempNode = parent.kids[index + 1]
            node.insert(parent.simpleDelete(index)[0])
            if 0 < tempNode.numC:
                kid = tempNode.kid[0]
                tempNode.removeKid(0)
                node.addKid(kid)
            parent.insert(tempNode.simpleDelete(0)[0])
            return

        if index == 0:
            node.insert(parent.simpleDelete(0)[0])
            merged = parent.kids[1]
            node.insert(merged.simpleDelete(0)[0])
            parent.removeKid(1)
            if 1 < merged.numC:
                kid = merged.kids[1]
                merged.removeKid(1)
                node.addKid(kid)
            if 0 < merged.numC:
                kid = merged.kids[0]
                merged.removeKid(0)
                node.addKid(kid)
            if parent == self.root and parent.isEmpty():
                self.root = node
            return

        node.insert(parent.simpleDelete(index - 1)[0])
        merged = parent.kids[index - 1]
        node.insert(merged.simpleDelete(0)[0])
        parent.removeKid(index - 1)
        if 1 < merged.numC:
            kid = merged.kids[1]
            merged.removeKid(1)
            node.addKid(kid)
        if 0 < merged.numC:
            kid = merged.kids[0]
            merged.removeKid(0)
            node.addKid(kid)
        if parent == self.root and parent.isEmpty():
            self.root = node
        return

    def inorderSuccessor(self, key, check=False):
        """
        switch treeItem with inorderSuccessor if possible and merge or redistribute nodes on path to inorderSuccessor
        :param check: do we want to redistribute or merge any 2 nodes on the path
        :param key: key of treeItem we want to find inorderSuccessor of
        :return: succes
        """
        temp = self.findItem(key)
        if not temp[1]:
            return None

        node = temp[0]
        index = node.find(key)[2]
        if node.isLeaf():
            return None
        current = node.kids[index + 1]
        while not current.isLeaf():
            next = current.kids[0]
            if check:
                self.check(current)
            current = next
        if check:
            self.check(current)
        return current

    def recDelete(self, current: Node, key):
        if current is None:
            return False
        if current != self.root:
            self.check(current)

        index = current.find(key)[2]
        correctKidIndex = -1
        j = 0
        found = False
        for k in current.items:
            if key < k.key:
                correctKidIndex = j
                found = True
                break
            j += 1

        if not found:
            correctKidIndex = j
        if index == -1:  # check if current node contains item with key
            correctKid = current.kids[correctKidIndex]
            return self.recDelete(correctKid, key)

        if current.isLeaf():
            current.delete(key)
            if current == self.root and self.root.numI == 0:
                self.root = None
            return True
        IO = self.inorderSuccessor(key, True)
        node, result, i = self.findItem(key)
        if node.isLeaf():
            node.simpleDelete(i)
            return True
        node.items[i] = IO.simpleDelete(0)[0]
        return True

    def deleteItem(self, key):
        if not self.findItem(key)[1]:
            return False
        return self.recDelete(self.root, key)

    def save(self):
        if self.root is None:
            return {'root': []}
        current = self.root
        return current.display(True)

    def recIO(self, root, callback):
        if root is None:
            return
        leaf = root.isLeaf()
        for j in range(0, root.numC - 1):
            self.recIO(root.kids[j], callback)
            callback(root.items[j].value)
        if not leaf:
            self.recIO(root.kids[root.numC - 1], callback)
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
        while self.root is not None:
            self.deleteItem(self.root.items[0].key)
        newRoot = Node()
        items = saved['root']
        for i in items:
            newRoot.insert(createTreeItem(i, i))
        self.root = newRoot
        self.recLoad(newRoot, saved['children'])


class TwoThreeFourTreeTable:
    def __init__(self):
        self.tree = TwoThreeFourTree()

    def tableIsEmpty(self):
        return self.tree.isEmpty()

    def tableInsert(self, treeItem):
        return self.tree.insertItem(treeItem)

    def tableDelete(self, key):
        return self.tree.deleteItem(key)

    def tableRetrieve(self, key):
        return self.tree.retrieveItem(key)

    def save(self):
        return self.tree.save()

    def load(self, saved):
        return self.tree.load(saved)

    def traverseTable(self, callback):
        return self.tree.inorderTraverse(callback)


t = TwoThreeFourTree()
t.load({'root': [5], 'children': [{'root': [2], 'children': [{'root': [1]}, {'root': [3, 4]}]},
                                  {'root': [12], 'children': [{'root': [10]}, {'root': [13, 15, 16]}]}]})
t.deleteItem(13)
t.deleteItem(10)
t.deleteItem(16)
print(t.save())

"""
{'root': [2, 5], 'children': [{'root': [1]}, {'root': [3, 4]}, {'root': [12, 15]}]}
"""

import random
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import numpy as np
import time


class Node: #Обычное бинарное дерево поиска
    def __init__(self, data, parent=None): #создание
        self.data = int(data)
        self.left = None
        self.right = None
        self.parent = parent

    def get_height(self):
        # Рекурсивное вычисление высоты
        if self == None:  # Если узел пустой (в теории self не может быть None)
            return 0
        left_height = self.left.get_height() if self.left else 0
        right_height = self.right.get_height() if self.right else 0
        return max(left_height, right_height) + 1
    
    def find_node(self, data): #поиск узла
        node = self
        while node:
            if data==node.data:
                return node
            elif data>node.data:
                node = node.right
            else:
                node = node.left
        return None
    
    def add_node(self, data):
        if data < self.data:
            if self.left == None:
                self.left = Node(data, self)
            else:
                self.left.add_node(data)
        elif data > self.data:
            if self.right == None:
                self.right = Node(data, self)
            else:
                self.right.add_node(data)

    def delete_node(self, data, node=None): #удаление
        if node == None:
            node = self
        if node == None:
            return None
        if data < node.data:
            node.left = self.delete_node(data, node.left)
            return node
        elif data > node.data:
            node.right = self.delete_node(data, node.right)
            return node
        else:
            if node.left == None:
                return node.right
            elif node.right == None:
                return node.left
            else:
                temp = node
                node = node.right
                while node.left:
                    node = node.left
                node.right = self.delete_node(node.data, temp.right)
                node.left = temp.left
                return node
            
    def out_node_width(self): #вывод в ширину
        if self == None:
            return
        result = []
        queue = [self]
        while len(queue) > 0:
            node = queue.pop(0)
            print(node.data, end=' ')
            result.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    def out_with_height(self):
        result = []
        if self.left:
            result.extend(self.left.out_with_height())
        result.append(self.data)
        if self.right:
            result.extend(self.right.out_with_height())
        return result

class Node_AVL:#АВЛ-дерево
    def __init__(self, data, parent=None):
        self.data = int(data)
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1
    
    def update(self):#обновляем высоту
        if self.left:
            left = self.left.height
        else:
            left = 0
        if self.right:
            right = self.right.height
        else:
            right = 0
        self.height = 1 + max(left, right)
    
    def check_balance(self):#проверка на перевес
        if self.left:
            left = self.left.height
        else:
            left = 0
        if self.right:
            right = self.right.height
        else:
            right = 0
        return left - right
    
    def to_right(self):#поворот направо
        rotated = self.left
        self.left = rotated.right
        if rotated.right:
            rotated.right.parent = self
        rotated.right = self
        rotated.parent = self.parent
        self.parent = rotated
        self.update()
        rotated.update() 
        return rotated 
    
    def to_left(self):#поворот налево
        rotated = self.right
        self.right = rotated.left
        if rotated.left:
            rotated.left.parent = self
        rotated.left = self
        rotated.parent = self.parent
        self.parent = rotated
        self.update()
        rotated.update()
        return rotated
    
    def auto_balance(self):#старт баланса
        self.update()
        if self.check_balance() > 1:
            if self.left and self.left.check_balance() < 0:
                self.left = self.left.to_left()
            return self.to_right()
        if self.check_balance() < -1:
            if self.right and self.right.check_balance() > 0:
                self.right = self.right.to_right()
            return self.to_left()
        return self
    
    def delete_node(self, data, node=None):#удоление
        if node == None:
            node = self
        if node == None:
            return None
        if data < node.data:
            node.left = self.delete_node(data, node.left)
            return node
        elif data > node.data:
            node.right = self.delete_node(data, node.right)
            return node
        else:
            if node.left == None:
                return node.right
            elif node.right == None:
                return node.left
            else:
                node = self
                while node.left:
                    node = node.left
                self.data = node.data
                self.right = self.right.delete_node(node.data)
        return self.auto_balance()
    
    def add_node(self, data):#добавление
        if data < self.data:
            if self.left == None:
                self.left = Node_AVL(data, self)
            else:
                self.left = self.left.add_node(data)
        elif data > self.data:
            if self.right == None:
                self.right = Node_AVL(data, self)
            else:
                self.right = self.right.add_node(data)
        return self.auto_balance()
    
    def out_node_width(self): #вывод в ширину
        if self == None:
            return
        result = []
        queue = [self]
        while len(queue) > 0:
            node = queue.pop(0)
            print(node.data, end=' ')
            result.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    def print_tree(self, level=0, name="Корень: "):
        print(" " * (level * 4) + name + str(self.data))
        if self.left:
            self.left.print_tree(level + 1, "Левый--- ")
        if self.right:
            self.right.print_tree(level + 1, "Правый--- ")

    def find_node(self, data):
        node = self
        while node:
            if data==node.data:
                return node
            elif data>node.data:
                node = node.right
            else:
                node = node.left
        return None
    def out_with_height(self):
        result = []
        if self.left:
            result.extend(self.left.out_with_height())
        result.append(self.data)
        if self.right:
            result.extend(self.right.out_with_height())
        return result


class Node_RB:
    def __init__(self, data, color="red", parent=None):
        self.data = data
        self.color = color  # "red" или "black"
        self.parent = parent
        self.left = None
        self.right = None

    def is_red(self):
        return self.color == "red"

    def __repr__(self):
        return f"{self.data} ({self.color})"
    
    def out_with_height(self):
        result = []
        if self.left:
            result.extend(self.left.out_with_height())
        if self.data!=None:
            result.append(self.data)
        if self.right:
            result.extend(self.right.out_with_height())
        return result


class RedBlackTree:
    def __init__(self):
        self.nil = Node_RB(None, "black")  # NIL-узел, используется как лист
        self.root = self.nil

    def get_height(self, node=None):
        if node is None:
            node = self.root  # Если узел не указан, начинаем с корня
        if node == self.nil or node is None:  # NIL-узел или пустой узел
            return 0
        left_height = self.get_height(node.left)
        right_height = self.get_height(node.right)
        return max(left_height, right_height) + 1
    
    def find_node(self, data):
        node = self.root
        while node:
            if data==node.data:
                return node
            elif data>node.data:
                node = node.right
            else:
                node = node.left
        return None
    
    def insert(self, data):
        new_node = Node_RB(data, parent=None)
        new_node.left = self.nil
        new_node.right = self.nil
        if self.root == self.nil:
            self.root = new_node
            self.root.color = "black"
        else:
            self._bst_insert(self.root, new_node)
        self.fix_insertion(new_node)

    def _bst_insert(self, current, new_node):
        if new_node.data < current.data:
            if current.left == self.nil:
                current.left = new_node
                new_node.parent = current
            else:
                self._bst_insert(current.left, new_node)
        else:
            if current.right == self.nil:
                current.right = new_node
                new_node.parent = current
            else:
                self._bst_insert(current.right, new_node)

    def fix_insertion(self, node):
        while node.parent and node.parent.is_red():
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.is_red():
                    node.parent.color = "black"
                    uncle.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.is_red():
                    node.parent.color = "black"
                    uncle.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.left_rotate(node.parent.parent)
        self.root.color = "black"

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def print_tree(self, node, level=0, position="Корень"):
        if node and node.data is not None:  
            print(" " * level + f"{position}: {node.data} ({node.color})")  # Отступ + данные узла
            self.print_tree(node.left, level + 4, "Левый")  
            self.print_tree(node.right, level + 4, "Правый") 
    
    def transplant(self, u, v):
        if u.parent is None:  # Если удаляемый узел корень
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def fix_deletion(self, node):
        while node != self.root and node.color == "black":
            if node == node.parent.left:
                bro = node.parent.right
                if bro.color == "red":
                    bro.color = "black"
                    node.parent.color = "red"
                    self.left_rotate(node.parent)
                    bro = node.parent.right
                if bro.left.color == "black" and bro.right.color == "black":
                    bro.color = "red"
                    node = node.parent
                else:
                    if bro.right.color == "black":
                        bro.left.color = "black"
                        bro.color = "red"
                        self.right_rotate(bro)
                        bro = node.parent.right
                    bro.color = node.parent.color
                    node.parent.color = "black"
                    bro.right.color = "black"
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                bro = node.parent.left
                if bro.color == "red":
                    bro.color = "black"
                    node.parent.color = "red"
                    self.right_rotate(node.parent)
                    bro = node.parent.left
                if bro.right.color == "black" and bro.left.color == "black":
                    bro.color = "red"
                    node = node.parent
                else:
                    if bro.left.color == "black":
                        bro.right.color = "black"
                        bro.color = "red"
                        self.left_rotate(bro)
                        bro = node.parent.left
                    bro.color = node.parent.color
                    node.parent.color = "black"
                    bro.left.color = "black"
                    self.right_rotate(node.parent)
                    node = self.root
        node.color = "black"


    def delete_node(self, data):
        delete = self.find_node(data)
        if not delete:
            return
        original_color = delete.color
        if delete.left == self.nil:
            change = delete.right
            self.transplant(delete, delete.right)
        elif delete.right == self.nil:
            change = delete.left
            self.transplant(delete, delete.left)
        else:
            min_node = delete.right
            while min_node.left != self.nil:
                min_node = min_node.left

            original_color = min_node.color
            change = min_node.right
            if min_node.parent == delete:
                change.parent = min_node
            else:
                self.transplant(min_node, min_node.right)
                min_node.right = delete.right
                min_node.right.parent = min_node

            self.transplant(delete, min_node)
            min_node.left = delete.left
            min_node.left.parent = min_node
            min_node.color = delete.color

        if original_color == "black":
            self.fix_deletion(change)

    def out_node_width(self):
        if self.root==None or self.root == self.nil:
            return
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            print(current.data, end=' ')
            if current.left != None and current.left != self.nil:
                queue.append(current.left)
            if current.right != None and current.right != self.nil:
                queue.append(current.right)
    


def quick_sort(arr): #быстрая сортировка
    if len(arr) <= 1:
       return arr
    else:
       q = arr[(len(arr)-1)//2]
    l_nums = [n for n in arr if n < q]
 
    e_nums = [q] * arr.count(q)
    b_nums = [n for n in arr if n > q]
    return quick_sort(l_nums) + e_nums + quick_sort(b_nums)


#--------------------измерение для обычного дерева---------------
n_values = [i for i in range(100,10100,100)]
results = []
nodes = []
for n in n_values:
    keys = random.sample(range(1,100000),n)
    tree = Node(keys[0])
    for key in keys[1::]:
        tree.add_node(key)
    results.append(tree.get_height())
    nodes.append(n)
x = np.array(nodes).reshape(-1,1)
y = np.array(results)
x_log = np.log(x)
model = LinearRegression()
model.fit(x_log, y)
x_pred = np.linspace(min(x), max(x), 100).reshape(-1, 1)
y_pred = model.predict(np.log(x_pred))
plt.scatter(x, y, color='blue', label='Экспериментальные точки')
plt.plot(x_pred, y_pred, color='red', label='Регрессионная кривая')
plt.title('Зависимость высоты дерева от количества узлов')
plt.xlabel('Количество узлов')
plt.ylabel('Высота дерева')
plt.text(np.mean(x), min(y), f"Коэффицинты регресии: y={model.coef_[0]}x+{model.intercept_}", color='black', ha='center', va='bottom')
plt.legend()
plt.grid()
plt.show()
#-----------------------измерение для АВЛ дерева--------------------
results = []
nodes = []
for n in n_values:
    keys = random.sample(range(1,100000),n)
    quick_sort(keys)
    tree = Node_AVL(keys[0])
    for key in keys[1::]:
        tree = tree.add_node(key)
    results.append(tree.height)
    nodes.append(n)
x = np.array(nodes).reshape(-1,1)
y = np.array(results)
x_log = np.log(x)
model = LinearRegression()
model.fit(x_log, y)
x_pred = np.linspace(min(x), max(x), 100).reshape(-1, 1)
y_pred = model.predict(np.log(x_pred))
plt.scatter(x, y, color='blue', label='Экспериментальные точки')
plt.plot(x_pred, y_pred, color='red', label='Регрессионная кривая')
plt.title('Зависимость высоты AVL дерева от количества узлов')
plt.xlabel('Количество узлов')
plt.ylabel('Высота дерева')
plt.text(np.mean(x), min(y), f"Коэффицинты регресии: y={model.coef_[0]}x+{model.intercept_}", color='black',  ha='center', va='bottom')
plt.legend()
plt.grid()
plt.show()
#--------------измерение для красно-черного дерева-------------
results = []
nodes = []
for n in n_values:
    keys = random.sample(range(1,100000),n)
    quick_sort(keys)
    tree = RedBlackTree()
    for key in keys:
        tree.insert(key)
    results.append(tree.get_height())
    nodes.append(n)
x = np.array(nodes).reshape(-1,1)
y = np.array(results)
x_log = np.log(x)
model = LinearRegression()
model.fit(x_log, y)
x_pred = np.linspace(min(x), max(x), 100).reshape(-1, 1)
y_pred = model.predict(np.log(x_pred))
plt.scatter(x, y, color='blue', label='Экспериментальные точки')
plt.plot(x_pred, y_pred, color='red', label='Регрессионная кривая')
plt.title('Зависимость высоты Красно-черного дерева от количества узлов')
plt.xlabel('Количество узлов')
plt.ylabel('Высота дерева')
plt.text(np.mean(x), min(y), f"Коэффицинты регресии: y={model.coef_[0]}x+{model.intercept_}", color='black',  ha='center', va='bottom')
plt.legend()
plt.grid()
plt.show()
print()

print("Вывод в ширину для красно-черного, АВЛ и обычного дерева:")
p1=RedBlackTree()
p1.insert(5)
p1.insert(4)
p1.insert(6)
p1.out_node_width()
print()
p2 = Node_AVL(7)
p2 = p2.add_node(9)
p2 = p2.add_node(8)
p2.out_node_width()
print()
p3 = Node(2)
p3.add_node(0)
p3.add_node(1)
p3.out_node_width()
print()

print("Вывод в глубину - центрированный")
p1=RedBlackTree()
p1.insert(5)
p1.insert(4)
p1.insert(6)
print(p1.root.out_with_height())
p2 = Node_AVL(7)
p2 = p2.add_node(9)
p2 = p2.add_node(8)
print(p2.out_with_height())
p3 = Node(2)
p3.add_node(0)
p3.add_node(1)
print(p3.out_with_height())
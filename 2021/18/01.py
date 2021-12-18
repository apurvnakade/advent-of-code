with open('input.txt', 'r') as f:
  input = [line.strip() for line in f.readlines()]



class Tree:
  
  def __init__(self, left = None, right = None):
    self.left = left
    self.right = right
    self.value = None
    self.depth = 0
    self.parent = None

    if self.left:
      self.left.parent = self
      self.left.increase_depth()
    if self.right:
      self.right.parent = self
      self.right.increase_depth()

  def increase_depth(self):
    self.depth += 1
    if self.left:
      self.left.increase_depth()
    if self.right:
      self.right.increase_depth()

  def parse_input(self, string, parent = None, depth = 0):
    self.depth = depth
    self.parent = parent
    while string:
      if string[0] == '[':
        self.left = Tree()
        string = self.left.parse_input(string[1:], self, depth + 1)
      elif string[0] == ']':
        return string[1:]
      elif string[0] == ',':
        self.right = Tree()
        string = self.right.parse_input(string[1:], self, depth + 1)
      else:
        self.value = int(string[0])
        return string[1:]

  def leftmost_leaf(self):
    if self.left:
      return self.left.leftmost_leaf()
    return self
  
  def rightmost_leaf(self):
    if self.right:
      return self.right.rightmost_leaf()
    return self

  def is_left_child(self):
    if self.parent:
      return self.parent.left == self
    return False

  def is_right_child(self):
    if self.parent:
      return self.parent.right == self
    return False

  def is_leaf(self):
    return not self.left and not self.right

  def is_root(self):
    return not self.parent

  def next_leaf_to_left(self):
    if self.is_left_child():
      return self.parent.next_leaf_to_left()
    elif self.is_right_child():
      return self.parent.left.rightmost_leaf()
    return None

  def next_leaf_to_right(self):
    if self.is_left_child():
      return self.parent.right.leftmost_leaf()
    elif self.is_right_child():
      return self.parent.next_leaf_to_right()
    return None

  def __str__(self):
    string = ''
    if self.left:
      string = '[' + self.left.__str__()
    if not self.value == None:
      string += str(self.value)
    if self.right:
      string += ',' + self.right.__str__() + ']'
    return string


  def magnitude(self):
    if self.is_leaf():
      return self.value
    return 3*self.left.magnitude() + 2*self.right.magnitude()

  def traverse(self, start = None):
    if start == None:
      start = self.leftmost_leaf()
    
    while start:
      if self.depth >= 5:
        explode(self, self.next_leaf_to_right())
        start = start.next_leaf_to_right()
    
    return None
      
    

      

def explode(left_leaf : Tree):
  right_leaf = left_leaf.next_leaf_to_right()
  # if right_leaf:
  leaf_to_left = left_leaf.next_leaf_to_left()
  leaf_to_right = right_leaf.next_leaf_to_right()

  parent = left_leaf.parent

  parent.left = None
  parent.right = None
  parent.value = 0

  if parent.is_left_child():
    parent.parent.left = parent
  else:
    parent.parent.right = parent

  if leaf_to_left:
    leaf_to_left.value += left_leaf.value

  if leaf_to_right:
    leaf_to_right.value += right_leaf.value
      
      # return True
    # return False

def split(leaf : Tree):
  left = Tree()
  left.value = leaf.value // 2
  left.depth = leaf.depth + 1
  leaf.left = left
  left.parent = leaf

  right = Tree()
  right.value = leaf.value - left.value
  right.depth = leaf.depth + 1
  leaf.right = right
  right.parent = leaf

  leaf.value = None

  return left
  

root = Tree()
root.parse_input(input[0])

def detonate():
  explosion = False
  start = root.leftmost_leaf()
  while start:
    if start.depth >= 5 and start.is_left_child():
      explode(start)
      explosion = True
      start = root.leftmost_leaf()
    elif start:
      start = start.next_leaf_to_right()
  return explosion

def check_splits():
  start = root.leftmost_leaf()
  while start:
    if start.value > 9:
      split(start)
      return True
    start = start.next_leaf_to_right()
  return False

for line in input[1:]:
  new_root = Tree()
  new_root.parse_input(line)
  root = Tree(root, new_root)

  while True:
    if not detonate():
      if not check_splits():
        break

          
print(root)
print(root.magnitude())
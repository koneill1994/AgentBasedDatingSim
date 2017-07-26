

# linked list implementation
# Kevin O'Neill

class LinkedList:
  
  def __init__(self,l=None):
    self.size=0
    self.first=LinkedListElement(None,None,None)
    self.last=self.first
    if l!=None:
      for x in l:
        self.add(x)
  
  def __iter__(self):
    return self
  
  def next(self,LLE=None):
    if LLE==None:
      LLE=self.first
    if LLE.nex == None or LLE == None:
      raise StopIteration()
    return LLE.nex
    
  def add(self,obj):
    el=LinkedListElement(None,None,obj)
    if self.size==0:
      self.first=el
      self.last=el
    else:
      el.prev=self.last
      self.last.nex=el
      self.last=el    
    self.size+=1
    
  def remove(self,LLE):
    self.size-=1
    LLE.remove()


class LinkedListElement:
  
  def __init__(self, prev, nex, val):
    self.prev=prev
    self.nex=nex
    self.val=val
    
  def remove(self):
    self.prev.nex=nex
    self.nex.prev=prev
    
  def __repr__(self):
    return str(self.val)



m = LinkedList([1,2,5,63,32,1])
print m.size
'''
for x in m:
  print x
'''



# linked list implementation
# Kevin O'Neill

class LinkedList:
  
  def __init__(self,l=None):
    self.size=0
    self.first=LinkedListElement(None,None,None,self)
    self.last=self.first
    self.it=self.first
    if l!=None:
      for x in l:
        self.add(x)
        
  def __len__(self):
    return self.size
  
  def __iter__(self):
    self.it=self.first
    return self
  
  def next(self,LLE=None):
    if LLE==None:
      LLE=self.it
    if LLE == None:
      raise StopIteration()
    self.it=LLE.nex
    return LLE
    
  def __next__(self,LLE=None):
    if LLE==None:
      LLE=self.it
    if LLE == None or self.size==0:
      raise StopIteration()
    self.it=LLE.nex
    return LLE
    
  def add(self,obj):
    el=LinkedListElement(None,None,obj,self)
    if self.size==0:
      self.first=el
      self.last=el
    else:
      el.prev=self.last
      self.last.nex=el
      self.last=el
    self.size+=1
    return el
    
  def remove(self,LLE):
    if(LLE.container == self):
      print "     a" + str(self.size)
      self.size-=1
      print "     b" + str(self.size)
      LLE.remove()
    if self.size == 0:
      self.first=LinkedListElement(None,None,None,self)
      self.last=self.first



class LinkedListElement:
  
  def __init__(self, prev, nex, val,container):
    self.prev=prev
    self.nex=nex
    self.val=val
    self.removed=False
    self.container=container
    
  def remove(self):
    self.container=None
    if self.prev != None:
      self.prev.nex=self.nex
    if self.nex != None:
      self.nex.prev=self.prev
    self.removed=True
    
  def __repr__(self):
    return str(self.val)

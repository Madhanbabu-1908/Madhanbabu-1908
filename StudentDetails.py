class Student:
   def __init__(self,id,name,age,mark):
        self.id=id
        self.name=name
        self.age=age
        self.mark=mark
        
   def setId(self,id):
        self.id=id
   def setName(self,name):
        self.name=name
   def setAge(self,age):
        self.age=age
   def setMark(self,mark):
        self.mark=mark
   def getId(self):
        return self.id
   def getName(self):
        return self.name
   def getAge(self):
        return self.age
   def getMark(self):
        return self.mark

class Solution:
    
   def findStudentWithMaxAge(list): 
        age=0
        lst=[]
        for i in range(0,len(list)):
            if(age==0):
                age=list[i].getAge()
            elif(age<list[i].getAge()):
                age=list[i].getAge()
        for i in range(0,len(list)):
            if(age==list[i].getAge()):
                lst=list[i]
        return lst
        
   def findStudentByName(list,name): 
        for i in range(0,len(list)):
            if(name.casefold()==list[i].getName().casefold()):
                return list[i]

           
   if __name__=="__main__":
        count=int(input())
        list = []
       
        for i in range(0,count): 
            id = int(input())
            name=input()
            age=int(input())
            mark=int(input())
            list.append(Student(id,name,age,mark))
            
        name = input()
        liA = findStudentWithMaxAge(list)

        if(liA==[]):
           print("No Such a Student found.")
        else:
           print("id-",liA.getId())
           print("name-",liA.getName())
           print("age-",liA.getAge())
           print("mark-",liA.getMark())
           
       
        liB = findStudentByName(list,name)
       
        if(liB==[]):
           print("No Such a Student found.")
        else:
           print("id-",liB.getId())
           print("name-",liB.getName())
           print("age-",liB.getAge())
           print("mark-",liB.getMark())
       

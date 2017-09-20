def insertionSort(alist):
   for index in range(1,len(alist)):

     currentvalue = alist[index]
     position = index

     while position>0 and alist[position-1]<currentvalue:
         alist[position]=alist[position-1]
         position = position-1

     alist[position]=currentvalue

a = [1,4,6,7,8,9,0,7,4,0]
insertionSort(a)
print(a)
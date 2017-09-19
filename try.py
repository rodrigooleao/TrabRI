def insertionSort(alist):
   for index in range(1,len(alist)):

     currentvalue = alist[index]
     position = index

     while position>0 and alist[position-1][0]<currentvalue[0]:
         alist[position]=alist[position-1]
         position = position-1

     alist[position]=currentvalue

alist = [(1.3458069466231275, 533), (1.42847231885405, 498), (1.4744514341788644, 827), (1.5367400719003417, 437), (1.5758794153808, 484)]
insertionSort(alist)
print(alist)
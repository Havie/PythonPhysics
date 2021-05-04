#2D array

arr= [[1,2,3],
     [4,5,6],
     [7,8,9]]

print(arr[0][1])


a= []
n=1
for i in range(3):
    a.append([])
    for j in range(3):
        a[i].append(n)
        n+=1


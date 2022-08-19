import sys 

x=sys.argv[1]

x=x.replace(" ","")

words=[]

chars=["0","1","2","3","4","5","6","7","8","9","+","-"]

operators=[]

word=""
last_op_index=0
for i in range(len(x)):
    if x[i]==chars[10] or x[i]==chars[11]:
        operators.append(x[i])
        words.append(word)
        word=""
        last_op_index=i
    else:
        word+=x[i]
word=""

for i in range(last_op_index+1, len(x)):
    word+=x[i]
words.append(word)

for i in range(len(words)):
    for j in words[i]:
        if j not in chars:
            raise Exception("Não colocou sequência correta")
    if words[i]=="":
        raise Exception("Não colocou sequência correta")
    words[i]=int(words[i])

concat=[]
for i in range(0,len(words)):
    concat.append(words[i])
    if i < len(operators):
            concat.append(operators[i])

sum=words[0]
for i in range(0,len(concat)-1,2):
    if concat[i+1]==chars[10]:
        sum+=concat[i+2]
    elif concat[i+1]==chars[11]:
        sum-=concat[i+2]

print(sum)
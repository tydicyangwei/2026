import random
def f3(nums):
    l1=[]
    for i in range(nums):
        l1.append(random.choice(range(1000)))
    return l1
def mn3(x,y,z):
    lr=[]
    r=f3(x)
    r1=r[:y]
    r2=r[y:z]
    for i in range(1000):
        if i in r1:
            pass
        else:
            lr.append(i)
  #  print("没有出现的号码有%d个" % len(lr))
  #  print("=======")
  #  print(lr)
  #  print("========")
    if len(lr) > 0:
        for i in lr:
            for index,j in enumerate(r2, start=1):
                if i == j:
                   # print(f"号码%d在第%d次出现" %(i,index))
                    return 1
def main():
    print("模拟冷号在之后100期内出现的次数")
    count = 0
    for i in range(1000):
        if mn3(8000,6205,6305) == 1:
            count += 1
    print("在1000次模拟中,冷号在之后100期内出现的次数为%d次" % count)

def db_test():
    print("随机号在之后100期内出现的次数")
    count = 0
    for i in range(1000):
        sjnum = random.choice(range(1000))
        if sjnum in f3(100):
            count += 1
    print("在1000次模拟中,随机号在之后100期内出现的次数为%d次" % count)

main()
db_test()




## 深拷贝和浅拷贝
l1=[1,[1,2]]
import copy
浅拷贝：
l2=copy.copy(l1)
l2第二层的列表直接引用（相同内存地址）
深拷贝
l3=copy.deepcopy(l1)
每一层都是独立内存地址


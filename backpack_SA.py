# 01背包問題
# 測資來源：https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html


import sys
import random
import math
import matplotlib.pyplot as plt

test_case = "p01"

# 引入測資及答案
c_ = open(test_case+"/c.txt", mode="r").read()
p_ = [line.split("\n")[0] for line in open(test_case+"/p.txt", mode="r").readlines()]
w_ = [line.split("\n")[0] for line in open(test_case+"/w.txt", mode="r").readlines()]
s_ = [line.split("\n")[0] for line in open(test_case+"/s.txt", mode="r").readlines()]
m_ = open(test_case+"/m.txt", mode="r").read()

c = int(c_) # 背包負重能力 capicity
p = list(map(int, p_)) # 物品價值 price
w = list(map(int, w_)) # 物品重量 weight

s = list(map(int, s_)) # 解答 solution
m = int(m_) # 全域最大價值 globle max price


# 初始化
alpha = 0.99 # 退火係數
initTemperature = 1000 # 初始溫度
loops = 1000
smloop = 100

ans = [0]*len(p) # 假定回答
temperature = initTemperature # 溫度
loop = 0 # 圈數
maxValue = 0 # 最高價值記錄
final_ans = None # 最終回答

# 圖表統計
package_price = [] # 在每種溫度下背包的價值
exploration_times = [] # 在每種溫度下放棄物體的次數

# 模擬退火演算法
# 迭代數：迭代每種溫度
while loop < loops:
    temperature = temperature*alpha # 每次探索都要退火
    exploration = 0 # 放棄物品的次數
    
    # 內部迭代，用意為產生讓同一溫度下可以探索更多次（至少要能產生一組解）
    for i in range(smloop):
        
        index = random.choice(range(len(p))) # 隨便抽一個物品
        
        # 不在當前背包則加入
        if ans[index] == 0: 
            ans[index] = 1
            weight_sum = sum([i*j for i,j in zip(w, ans)]) # 計算當前假定答案的重量總和
            
            # 如果當前重量小於負重能力
            if weight_sum <= c:
                value_sum = sum([i*j for i,j in zip(p, ans)]) # 計算當前價值
                # 如果當前價值大於記錄價值
                if value_sum > maxValue: 
                    maxValue = value_sum # 更新紀錄價值
                    final_ans = ans[:] # 更新最終回答(自認為的全域解)
                    
            # 反之，則把上一個東西移除並重新抽一個物品
            else:
                ans[index] = 0
                continue
        # 反之，如果東西被拿了的話
        else:
            # 退火算法的關鍵：根據溫度計算「是否繼續探索」
            # 隨著溫度逐漸將低，演算法就越來越保守，避免放棄當前拿到的東西
            if random.random() > math.exp(-p[index]/temperature): # 評估公式（隨著溫度降低而數值提高）
                ans[index] = 0 # 放棄現在拿的東西，避免陷入局部最優解
                exploration += 1 # 圖表統計用
                
                
    package_price.append(sum([i*j for i,j in zip(p, ans)])) # 記錄每種溫度下背包內價值的歷史
    exploration_times.append(exploration)
    loop = loop + 1
# 輸出
print("要拿哪些有價值的: ", final_ans)
print("背包總價值: ", sum([i*j for i,j in zip(p, final_ans)]))
print("背包最大價值: ", m)
print("是否為全域解: ", (s == final_ans))

print(len(package_price), loop)
# 顯示圖表
plt.figure(figsize=(15,6),dpi=100,linewidth = 2)
# plt.plot([x for x in range(0, loop)], package_price, color = 'r', label="price") 
plt.plot([x for x in range(0, loop)], exploration_times, color = 'g', label="exploration") 
plt.title("Package price", x=0.5, y=1.03)
plt.xlabel("loop")
plt.ylabel("price")

plt.show()
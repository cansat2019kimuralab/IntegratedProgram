# Goal.py
---
## Togoal(photopath, H_min, h_max, S_thd, spinGoal, vStraightGoal)  
### 引数：  
 - photopath:写真のpath  
 - H_min:色相の最大値  
 - H_max:色相の最小値  
 - S_thd:彩度の閾値  
 - spinGoal:回転速度の目標値  
 - vStraightGoal:直進速度の目標値  
### 戻り値：
 - flug: (0:goal、-1:ゴール未検出、1:ゴール正面、2:ゴール左、3:ゴール右)
 - area:ゴールの面積  
 - GAP:ゴールの中心と画像の中心との差[pixcel]  
 - photoname: 処理した写真の名前  
---
##accPID(Goal, bm, Kp, Ki, max, min):  
### 引数：
- Goal:目標値  
- bm:bmx055のリスト番号  
- Kp,Ki,Kd:ゲイン  
- max,min:モータ出力の最大最小値  
### 戻り値：  
- mP:モータパワー
---  
##velPID(Goal, vel, Kp, Ki, max, min):  
### 引数：
- Goal:目標値  
- vel:速度  
- Kp,Ki,Kd:ゲイン  
- max,min:モータ出力の最大最小値  
### 戻り値：  
- mP:モータパワー
---
##culvel(fC, bm, t):  
### 引数：
- fC:filterCoefficientρ（パスフィルタの係数）  
- bm:bmx055のリスト番号  
- t:時間間隔  
### 戻り値：  
- vel:速度
---
## SpeedSwitch(L)
### 引数：
 - ゴールまでの距離(m)  
### 戻り値：
 - モータのデューティ比  
---
## CurvingSwitch(GAP, speed)  
### 引数：
 - GAP:ゴールの中心 - 画像の中心  
 - speed:SpeedSwitchの戻り値  
### 戻り値：  
 - mPLeft:左モータのデューティ比  
 - mPRight:右モータのデューティ比  
 - flug:(0:goal、-1:ゴール未検出、1:ゴール正面、2:ゴール左、3:ゴール右) 
 ---

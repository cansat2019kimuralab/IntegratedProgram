# Goal.py
---
## Togoal(photopath, H_min, h_max, S_thd)  
### 引数： 
   - photopath:写真のpath  
   - H_min:色相の最大値  
   - H_max:色相の最小値  
   - S_thd:彩度の閾値  
### 戻り値：
   - flug(0:goal、-1:ゴール未検出、1:ゴール右より、2:ゴール左より、3:ゴール正面)
---
## SpeedSwitch(L)
### 引数：
   - ゴールまでの距離(m)  
### 戻り値：
   - スピード  
---
## CurvingSwitch(GAP, speed)  
### 引数：
   - GAP:ゴールの中心 - 画像の中心  
   - speed:SpeedSwitchの戻り値  
### 戻り値：  
   - mPLeft:左モータのデューティ比  
   - mPRight:右モータのデューティ比  
   - flug:(0:goal、-1:ゴール未検出、1:ゴール右より、2:ゴール左より、3:ゴール正面)左モータのデューティ比  

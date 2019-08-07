# Goal.py
---
## Togoal(photopath, H_min, h_max, S_thd, mp_min, mp_max)  
### 引数：  
 - photopath:写真のpath  
 - H_min:色相の最大値  
 - H_max:色相の最小値  
 - S_thd:彩度の閾値   
 - mp_min,mp_max:回転するときの出力  
### 戻り値：
 - flug: (0:goal、-1:ゴール未検出、1:ゴール正面、2:ゴール左、3:ゴール右)
 - area:ゴールの面積  
 - GAP:ゴールの中心と画像の中心との差[pixcel]  
 - photoname: 処理した写真の名前  
---

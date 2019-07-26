# Running
## Running.py
- checkGPSstatus(gps) : GPSステータス確認用関数  
	引数　:GPSデータ  
	戻り値：GPSステータス（0:Status VまたはRead GPS Error、1:Status A)  
- calNAng(calibrationScale, angleOffset) : ローバーが向いている角度を計算する関数  
	引数　：キャリブレーションスケール、角度オフセット  
	戻り値：ローバーが向いている角度  
- calGoal(nowLat, nowLon, goalLat, goalLon, nowAng) : ゴールとの距離、角度、相対角度を計算する関数  
	引数　：現在の緯度、経度、ゴールの緯度、経度、現在の角度  
	戻り値：ゴールとの距離、角度、相対角度  
- runMotorSpeed(relativeAng) : モータパワーを算出する関数  
	引数　：ゴールとの相対角度  
	戻り値：左のモータパワー、右のモータパワー、モータのスピン成分  
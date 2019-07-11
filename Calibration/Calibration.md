# Calibration
## Calibration.py
ライブラリ  
- Calibration(path) : フィッティングでキャリブレーションを行う  
	引数　： ファイルパス  
	戻り値： 楕円 → 円変換ベクトル（[x_ave, y_ave, x_axis, y_axis])  
- readCalData(path) : BMX055からデータを取り保存する  
	引数　： ファイルパス  
	戻り値： なし  

## calibration_test.py
Calibration確認用  
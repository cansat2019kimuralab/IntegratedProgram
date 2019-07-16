# Calibration
[3軸磁気センサーLIS3MDの検討](https://research.itplants.com/?p=1787)  
[Scipy.odr を使った陰関数フィッティング](http://pota.hatenablog.jp/entry/2014/10/31/033326)  
[球面フィッティングの導出と実装](https://github.com/J-ROCKET-BOY/SS-Fitting/blob/master/SS_fitting.py#L83)

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

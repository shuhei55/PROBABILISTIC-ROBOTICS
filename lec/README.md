# 自己位置推定講習
* 基本的な自己位置推定をしてみたり
* ベイズの定理を用いた自己位置推定をしてみたりしましょう
## 環境構築
* このプロジェクトはpython3を使います
* 基本はC++を使ってきたはずですが、pythonも使えて損はない(RCで多分使う)のでこれを機になれましょう(難しいことはしない)
* python3の環境構築は人それぞれで好きにやってください(jupyter-notebookやanacondaやpyenvなどなど)
* 一番やってはいけないのはanacondaでやってたのに以下の方法もやるとかです(コンフリクトします)
* ある程度理解しているなら好きなようにやって良いですが、とりあえず以下の方法でをおすすめします
* python3のインストール
```
$ sudo apt update
$ sudo apt install python3 python3-pip python-pip
$ sudo pip install numpy matplotlib
```
* 以下のコマンドでdefault.pyが動けばよい
```
$ ./default.py
```

## シミュレーター
* 詳しくはシミュレーターの関数一覧などを読めば良いがどのようなシミュレーターかについて
* シミュレーターはx,y,thetaの３変数のとそれの一回微分と二回微分の状態量をもちます
* update関数が呼ばれると一定の分散をもちながらそれぞれ積分して時間更新されます
* 制御周期は10msとしています
* エンコーダーはマシン座標系でx方向とy方向に非常に精度高く並行についているとします
* エンコーダーの返す値は差分であり、速度ではありません
* gyroセンサーもマシンに剛に固定されており精度高くマシンの角速度を返してくれるとします
## F3RC感のある決定論的自己位置推定
* とりあえず環境構築でシミュレーターを動かすことはできたでしょうか
* じゃあさっそくF3RCでつかうような簡単な自己位置推定をしてみましょう
* シミュレーターの関数に実装されているget\_enc関数とget\_gyro関数を用いて自己位置推定をしてみましょう

```
theta += get_gyro() * dt
X += (回転行列[-theta]) * get_enc() * dt
```
* 簡単なモデルなら上の式みたいな感じでしょうか
* 実装してみましょう
```python3:main.py
#! /usr/bin/python3

from sim import simulator
from drawer import drawer
import numpy as np
from config import config

def plot(data):
    global theta, X
    sim.update()
    #自己位置推定の更新
    theta += sim.get_gyro() * 10
    X += np.array([[np.cos(-theta),-np.sin(-theta)],[np.sin(-theta), np.cos(-theta)]]) @ sim.get_enc() #@は内積を意味する(回転行列をかけているだけ)
    ball_img = drawer.draw_point(sim.x,sim.y)
    ball_img = drawer.draw_point(X[0][0], X[1][0], "g")
    return ball_img

sim = simulator.Sim(0.,0.,1.,1.,0.,0.) #シミュレーターのコンストラクタ

#自己位置の初期値
theta = 0.
X = np.array([[0.,0.]]).T

drawer = drawer.Drawing(plot)

ball_img = config.init(drawer)

drawer.show()
```
* どうでしょうかそれっぽく自己位置推定できたのではないでしょうか？
* でも当然ですがだんだんずれていってしまいますね

## カルマンフィルターを用いた自己位置推定
* 実際の世界にはありえないモデルですが線形モデルで一回考えてみましょう
* 定期的に一定の分散は乗っているもののマシンの自己位置がなぜか手に入るモデルを考えましょう
* 疲れたんでコード読んで下さい

## SingleModelEKF(Extended Kalman Filter)
* 同上

## MultiModelEKF(Extended Kalman Filter)
* 同上

## UKF(Unscented Kalman Filter)
* 未実装

## EIF(Extended Information Filter)
* 未実装

## パーティクルフィルター
* 未実装



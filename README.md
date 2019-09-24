# 確率ロボティクスの勉強
## KF
```
$./kf_main.py
```
## Single Model EKF
```
$./single_ekf_main.py
```
## Multi Model EKF
```
$./multi_model_ekf_main.py
```

## 使い方
* default.pyをコピーして同じ場所にmain.pyなどを作ってそれを変更する感じでやればいいと思います
* 読めばわかるがplot関数内でball\_imgに色々渡して上げればそれがプロットされます
* 基本的にplot関数が毎周期呼ばれるので一定周期で呼ばれたいものはこの中に書きましょう
* 柵などの最初から書かれてほしくて変化しないものはconfig/config.pyに書いてあげましょう
* デフォルトでは-4000~4000の正方形で囲むように書かれています
* また左下にstopボタンとresetボタンがあります
  * ストップボタンはトグルスイッチで押したらstartとstopを切り替えます
  * plot関数のループを止めます
  * resetボタンは何も実装していないので押してもなにも起こりません
### drawer
* drawerに用意されている関数一覧
* まあ自分でコード読めって話だけど
* 基本的にこれらの関数の返り値をball\_imgに渡してあげれば良いです
* [色一覧参考ページ](https://pythondatascience.plavox.info/matplotlib/色の名前)
#### draw\_point(x, y, c="r", pointsize=3)
* 引数のxとyの場所に点をプロットします
* 第三引数と第四引数は指定しなくても大丈夫です
* デフォルトでは赤色の大きさ3の点をプロットします
#### draw\_circle(x, y, x\_diameter, y\_diameter, c="b")
* 引数のxとyの場所に横の直径x\_diameterの縦の直径y\_diameterの円(楕円)をプロットします
* デフォルトの色は青色です
* 正確には円周をプロットします
* 中を塗りつぶしたものは実装していません(大きい点のプロットで頑張って)
#### draw\_arraw(start\_x, start\_y, end\_x, end\_y, c="gray")
* 名前の通りstartの点からendの点への矢印をプロットします
* デフォルトの色はグレーです
* 矢印のタイプやサイズなどをいじりたかったら関数の中身を自分で書き換えてください
#### draw\_line(p1, p2, c="g")
* 他と統一すればよかったのですがまあ許して下さい
* x,yの配列を渡して下さい
* 渡された２つのポイントをつなぐ直線を引きます
* 中身をいじれば線の太さとかも変えられます
* デフォルトの色は緑色です
* こんな感じで使って下さい
```
draw_line([0,0], [100, 100], c="r")
```
#### start\_stop\_animation
* この関数を呼べばアニメーションが動いてたら止まり、止まってたら動きます
* トグルスイッチです
* アニメーションが止まるというより、plot関数のループが止まります
#### stop\_animation
* この関数を呼ぶとアニメーションが止まります
#### reset\_animation
* 未実装

### simulator
* simulatorに用意されている関数一覧
* 同様に自分でコード読めって話だけど
* 大して頭いいことしてないです
* 自己位置推定がメインなので適当に動いてくれればいいというお気持ちです(分散結構大きいから変なふうに動くと思う)
* x,y,thetaとそれの一回微分、二回微分を状態量として持っていて、それを毎周期更新するだけののもです
* x,y,theta,dx,dy,omegaでアクセスできる

#### \_\_init\_\_(x,y,dx,dy,theta,omega)
* コンストラクタ
* 初期のx,y,theta,dx,dy,omegaを引数とする
* 一応float型で渡してあげた(0.とかにする)ほうがよい??(pythonよくわかんない)
* 二回微分は0で初期化する

#### setpos(x,y,dx,dy,theta,omega)
* コンストラクタと同じことしかしてない
* 同様に一応float型で渡してあげた(0.とかにする)ほうがよい??(pythonよくわかんない)
* 二回微分は0で初期化する

#### poszero()
* setpos(0,0,0,0,0,0)を呼んでいるだけ

#### setacc(ddx,ddy,ep)
* 各成分の二回微分を指定できる
* 電流制御のお気持ち
* 別に速度司令で適当に動かしてもいい
* っていうか速度司令のが直感的だし良い気がする

#### update()
* この関数を呼ぶと各状態量からdt=10msで一回更新される
* またこのとき二回微分による一回微分の更新には適度な分散を乗せている
* 今は一様分布だが分散の乗せ方を変えたければ中身をみて
* 例えばこの関数をplot関数内で呼んであげればよい

#### get\_enc()
* マシンにとってのxとyの前回周期からの変化の差分を返してくれる
* 一様な適度な分散を乗せている
* マシンにとってなので、フィールドにとってではないので注意
* 返り値：np.array([[dx],[dy]])

#### get\_x\_length()
* マシンの自己位置のxについてある程度の一様分散を乗せてかえす
* 返り値：float
* 実際の世界では不可能なものだが線形なモデルのテストをしたいときに使う

#### get\_y\_length()
* xと同様

#### get\_theta()
* xと同様
* 図で言うと上方向(y軸正の方向)を0として時計回りに正としたradを返す

#### get\_gyro()
* 状態量omegaに適当な一様分散を持たせて返してきます

#### get\_single\_wall\_length(angle)
* マシン座標系でのy軸正の方向を0とした時計回りに正とした方向に測距センサーを飛ばして帰ってきた値を返す
* x=0(y軸)の柵だけが存在するという仮定で計算されます
* もし計算した方向に柵が存在しなかったり、極めて遠くであればnp.infを返す

#### get\_multi\_wall\_length(angle)
* get\_single\_wall\_length(angle)と同様
* x=4000, x=-4000, y= 4000, y=-4000に柵があると仮定し一定の一様分散を乗せて距離を返す
* どの柵を読んで値を返しているかはわからない
* どの柵も読めない場合などはnp.infを返す

## 一言
* 使い方書くの面倒くさくなった
* そもそも使い方知りたい人いるのかなあ
* そのうちUKFとEIFとパーティクルフィルターも実装したいね
* ってかだれか実装してほしい
from math               import sin       as Sin

from matplotlib         import pyplot    as plt
from matplotlib         import animation
from matplotlib.widgets import Button

class xyAnim:
    def __init__(self):

        # グラフを作って、
        self.fig = plt.figure()
        self.ax  = plt.axes(xlim=(-2,2), ylim=(-1,1))
        self.ax.set_aspect("equal")

        # グラフの中にボタンを作って、
        self.playButton  = self.__createButton(0.6, 0.03, 0.15, 0.1, "play/pause", self.__PlayPause) # (左下 x 座標, 左下 y 座標, 幅, 高さ, ラベル, バインドする函数)
        self.resetButton = self.__createButton(0.8, 0.03, 0.15, 0.1, "reset"     , self.__Reset    ) # (左下 x 座標, 左下 y 座標, 幅, 高さ, ラベル, バインドする函数)

        # 何か図形 (ここでは円) を実体化して、
        self.theta  = 0
        self.circle = plt.Circle((Sin(self.theta), 0), 0.5) # Circle((中心 x 座標, 中心 y 座標), 半径)

        # その図形をグラフの中に投入する。
        self.ax.add_patch(self.circle)

        # 「どのグラフで (self.fig)」「どの函数を (self.__update)」「何ミリ秒ごとに呼び出す (interval=)」のかを設定する。
        self.anim = animation.FuncAnimation(self.fig, self.__update, interval=1000/30)

        # アニメーションの動作/停止状態を示すフラグを立てておく。
        self.isRunning = True

    # この函数を一定時間ごとに呼び出す。
    def __update(self, i):                        # i は FuncAnimation() から渡されるフレーム番号 (ここでは使っていない)。
        self.theta        += 0.1                  # 呼ばれるたびに何かを少しずつ変化させて、
        self.circle.center = (Sin(self.theta), 0) # それに合わせて円の中心座標を少しずつずらす。

    # "play/pause" ボタンがクリックされたら、アニメーションを停止するか再開するかする。動作/停止状態を示すフラグもトグルする。
    def __PlayPause(self, event):
        if self.isRunning:
            self.anim.event_source.stop()
            self.isRunning = not self.isRunning
        else:
            self.anim.event_source.start()
            self.isRunning = not self.isRunning

    # "reset" ボタンがクリックされたら、図形を最初の位置に戻す。
    def __Reset(self, event):
        self.theta         = 0
        self.circle.center = (Sin(self.theta), 0)

    # ボタンを作るための函数
    def __createButton(self, bottomLeftX, bottomLeftY, width, height, label, func):
        box    = self.fig.add_axes([bottomLeftX, bottomLeftY, width, height]) # ボタン用の枠を描いて、
        button = Button(box, label)                                           # それをボタンとして実体化して、
        button.on_clicked(func)                                               # クリックされたときに実行する函数をバインドする。
        return button

    # グラフを表示する。
    def animate(self):
        plt.show()
        return self

########
# test #
########
if __name__ == "__main__":
    xyAnim().animate()

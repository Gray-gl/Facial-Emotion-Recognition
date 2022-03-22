######################################################
# 布局管理
# 绝对定位：根据像素进行定位，但是不同显示屏会有不同的像素定位
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QDesktopWidget, \
    QGridLayout, QLineEdit, QTextEdit


class Example_Absolute(QWidget):
    '''
        绝对布局
    '''

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lbl1 = QLabel('ZetCode',self)
        lbl1.move(15,10)

        lbl1 = QLabel('tutorials',self)
        lbl1.move(35,40)

        lbl1 = QLabel('for programmers',self)
        lbl1.move(55,70)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Absolute')
        self.show()

class Example_Box(QWidget):
    '''
    盒布局，具有水平布局和垂直布局，QHBoxLayout和QVBoxLayout
    '''

    def __init__(self):
        super(Example_Box, self).__init__()
        self.initUI()

    def initUI(self):

        # 声明一个按键
        okButton = QPushButton('OK')
        cancealButton = QPushButton('Canceal')

        # 声明布局方式
        # 水平盒子
        hbox = QHBoxLayout()
        # 在盒子之前增加了弹性空间，将按钮调整到窗口的右边
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancealButton)

        # 垂直盒子，用白保存垂直盒子
        vbox = QVBoxLayout()
        # 垂直布局，增加的一个弹性空间，将按钮调整到下边
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        # 将当前的布局保存到主控件钟
        self.setLayout(vbox)

        # 设置空间布局
        self.setGeometry(300,300,300,150)
        self.setWindowTitle('layout')
        self.show()

    def center(self):
        '''
        在主窗口之上又设置了一个主框架，通过主窗口和主框架位置的相对关系实现对齐
        :return:
        '''
        # 获取主窗口所在的框架
        qr = self.frameGeometry()
        # 获取屏幕的分辨率，并得到屏幕中间点的位置
        cp = QDesktopWidget().availableGeometry().center()
        # 将主窗口的框架的中心点放置到屏幕的中心位置
        qr.moveCenter(cp)
        # 通过move函数将主窗口的左上角移动到框架的左上角，实现对其居中
        self.move(qr.topLeft())

class Example_Grid(QWidget):

    def __init__(self):
        super(Example_Grid, self).__init__()
        self.initUI()

    def initUI(self):

        # 声明布局的格式，并设置当前控件的格局是grid
        grid = QGridLayout()
        self.setLayout(grid)

        # 定义按钮的名字
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3-21', '-',
                '0', '.', '=', '+']

        # 生成位置
        positions = [(i,j) for i in range(5) for j in range(4)]

        # 按照位置添加对应控件
        # zip方法：将可迭代对象作为参数，将对象中的元素打包成一个元组，返回元组组成的列表
        for position ,name  in zip(positions,names):

            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button,*position)

        self.move(300,150)
        self.center()
        self.setWindowTitle('Calculator')
        self.show()

    def center(self):
        '''
        在主窗口之上又设置了一个主框架，通过主窗口和主框架位置的相对关系实现对齐
        :return:
        '''
        # 获取主窗口所在的框架
        qr = self.frameGeometry()
        # 获取屏幕的分辨率，并得到屏幕中间点的位置
        cp = QDesktopWidget().availableGeometry().center()
        # 将主窗口的框架的中心点放置到屏幕的中心位置
        qr.moveCenter(cp)
        # 通过move函数将主窗口的左上角移动到框架的左上角，实现对其居中
        self.move(qr.topLeft())

class Example_message_submit(QWidget):

    def __init__(self):
        super(Example_message_submit, self).__init__()
        self.initUI()

    def initUI(self):

        # 声明三个信息框
        title = QLabel("Title")
        author = QLabel("Author")
        review = QLabel("Review")

        titleText = QLineEdit()
        authorText = QLineEdit()
        reviewText = QTextEdit()

        # 创建网格式布局
        grid = QGridLayout()
        # 设置标签之间的空隙
        grid.setSpacing(15)

        # 添加对应的控件
        grid.addWidget(title,1,0)
        grid.addWidget(author,2,0)
        grid.addWidget(review,3,0)

        grid.addWidget(titleText,1,1)
        grid.addWidget(authorText,2,1)
        # 设定当前元素的位置，和跨行和跨列大小
        grid.addWidget(reviewText,3,1,5,1)

        self.setLayout(grid)

        self.setGeometry(300,300,350,300)
        self.setWindowTitle("review")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = Example_Absolute()
    # ex = Example_Box()
    # ex = Example_Grid()
    ex = Example_message_submit()
    sys.exit(app.exec_())
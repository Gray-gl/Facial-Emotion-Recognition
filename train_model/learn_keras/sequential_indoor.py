from keras.layers import Dense
from keras.models import Sequential

# 初始化序列化模型
model = Sequential()

# 加入对应模型层块
model.add(Dense(units = 4,activation='relu',input_dim=100))
model.add(Dense(units = 5,activation='softmax'))

# 编译模型
model.compile(loss='categorical_crossentropy',
              optimizer='SGD',
              metrics=['accuracy'])

x_train = list()
y_train = list()
# 使用模型进行训练，并传入训练集
model.fit(x_train,y_train,epochs = 5,batch_size = 32)

# 使用训练好的模型进行预测
x_test = list()
classes = model.predict(x_test,batch_size=128)
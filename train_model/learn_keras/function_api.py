# 函数api定义复杂的模型
from keras.layers import Input,Dense
from keras.models import Model

# 创建一个输入层
inputs = Input(shape = (100,))

# 调用前一层的实例，并进行连接
x = Dense(4,activation='relu')(inputs)
prediction = Dense(5,activation='softmax')(x)

# 创建一个model模型，并指定输入和输出
model = Model(inputs = inputs,outputs = prediction)
model.compile(optimizer='SGD',
              loss = 'categorical_cressentropy',
              metrics=['accuracy'])

data = list()
labels = list()
model.fit(data,labels)

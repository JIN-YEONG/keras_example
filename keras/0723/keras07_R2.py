
# 1. 데이터
import numpy as np
x_train = np.array([1,2,3,4,5,6,7,8,9,10])   # 10행 1열의 데이터
y_train = np.array([1,2,3,4,5,6,7,8,9,10])
x_test = np.array([11,12,13,14,15,16,17,18,19,20])
y_test = np.array([11,12,13,14,15,16,17,18,19,20])
x3 = np.array([101,102,103,104,105,106])   # 6행 1열의 데이터
x4 = np.array(range(30,50))   # 30~49값


# 딥러닝의 데이터는 열이 우선된다(행은 무시)
# input.shape(a,b)   => 데이터의 행,열의 표현   
#                    => a -> 열, b-> 행

# 2. 모델 구성
from keras.models import Sequential
from keras.layers import Dense

model = Sequential()   # 순서대로 내려가는 모델

# 노드가 5개, 3개, 4개인 레이어 3개를 가진 모델

# model.add(Dense(5, input_dim=1, activation='relu'))   # input_dim = 입력 데이터의 컬넘의 개수
                                                      # 데이터의 행과 상관없이 열의 개수만 맞아도 데이터를 넣을 수 있다.
model.add(Dense(1000, input_shape=(1,), activation='relu'))   # input_shape = 데이터의 shape를 기준으로 입력
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))
model.add(Dense(1070))


model.add(Dense(1))   

# model.summary()

# 과적합 -> 너무 많은 노드와 레이어에 의해 결과가 떨어지짐


# 3. 훈련
# model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])  # mse = mean squared error 평균 제곱 에러
model.compile(loss='mse', optimizer='adam', metrics=['mse'])  # metrics=['mse'] 결과 값이 mse값으로 나온다
# model.fit(x,y,epochs=100, batch_size = 3)   
model.fit(x_train,y_train,epochs=100)

# 4. 평가 예측
lose,acc = model.evaluate(x_test,y_test,batch_size=1)   
print('mse: ',acc)   # acc는 회귀모델에서만 사용할 수 있다.

y_predict = model.predict(x_test)   # 모델의 예측값
print('Predict\n',y_predict)

# RMSE 구하기
from sklearn.metrics import mean_squared_error

def RMSE(y_test, y_predict):   # 평균 제곱근 오차
    return np.sqrt(mean_squared_error(y_test, y_predict))   # root(mean((y_test - y_predict)^2))
# 루트를 씨우는 이유 -> 값을 작게 만들기 위해

print('RMSE: ', RMSE(y_test, y_predict))   # 작을 수록 좋다.

# R2 구하기
from sklearn.metrics import r2_score
r2_y_predict = r2_score(y_test, y_predict)   # 1에 가까울수록 좋음
print('R2:', r2_y_predict)

'''
과적합된 모델
mse:  222150047196774.4
Predict
 [[ -9802379.]
 [-10863496.]
 [-11925617.]
 [-12988176.]
 [-14051352.]
 [-15116091.]
 [-16181994.]
 [-17248484.]
 [-18315706.]
 [-19383284.]]
RMSE:  14904699.087990565
R2: -26927279382247.098
'''
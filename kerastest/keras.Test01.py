#-*- coding: utf-8 -*-

# 주식 데이터를 이용해 다음날 종가 예측


from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np

batchSize = 1
file_path = './0801/data/kospi200test.csv'
repeat_num = 100
# num_epochs = 100

file_data = pd.read_csv(file_path, encoding='euc-kr')
# print(file_data.head())

file_data.drop('Unnamed: 7' ,axis=1, inplace=True)

file_data=file_data.sort_values(by=['일자']) # 시간순으로 정렬
file_data.drop('일자', axis=1, inplace=True)
# 추가사항
# file_data.drop('거래량', axis=1, inplace = True)
# file_data.drop('환율(원/달러)', axis=1, inplace = True)

price = file_data.values[:,:-1]
scaler = MinMaxScaler()
scaler.fit(price)
mm_price = scaler.transform(price)

volume = file_data.values[:,-1:]
scaler.fit(volume)
mm_volume = scaler.transform(volume)


x = np.concatenate((mm_price, mm_volume), axis=1)
y = file_data['종가']   # y = x[:,3]   # 수정사항


data_x = []
data_y = []

for i in range(0, len(y) - 5):
    data_x.append(x[i:i+5])
    data_y.append(y[i+5])
    
data_x = np.array(data_x)
data_y = np.array(data_y)


train_x, test_x , train_y, test_y = train_test_split(
    data_x, data_y, random_state = 81, test_size=0.4
)

val_x, test_x ,val_y, test_y = train_test_split(
    test_x, test_y, random_state = 81, test_size = 0.5
)

train_x= train_x.reshape(356, 5*6)
test_x= test_x.reshape(119, 5*6)
val_x= val_x.reshape(119,5*6)

# print(train_x.shape)
# print(train_y.shape)
# print('-'*10)
# print(test_x.shape)
# print(test_y.shape)
# print('-'*10)
# print(val_x.shape)
# print(val_y.shape)

model = Sequential()
# model.add(LSTM(119, batch_input_shape=(batchSize,5,4), stateful=True))   # 수정사항 , batch_input_shape 값 변경

model.add(Dense(128, input_shape=(5*6, ),activation='relu'))
model.add(BatchNormalization())
model.add(Dense(356))
model.add(Dropout(0.3))
model.add(Dense(55))
model.add(BatchNormalization())
model.add(Dense(119))
# model.add(Dropout(0.2))
# model.add(Dense(475))
# model.add(BatchNormalization())
# model.add(Dense(231))
# model.add(Dropout(0.2))
model.add(Dense(58))
model.add(BatchNormalization())
model.add(Dense(81))
# model.add(Dropout(0.2))
model.add(Dense(122))
model.add(Dropout(0.2))

model.add(Dense(1))



model.compile(loss='mse', optimizer='adam', metrics=['mse'])

early_stopping = EarlyStopping(monitor='vol_mse', patience=20, mode='auto')


model.fit(train_x, train_y, epochs=repeat_num, batch_size=batchSize, verbose=2, validation_data=(val_x, val_y), callbacks=[early_stopping])

# 추가 사항 
# # 상태유지 LSTM용
# for rp_id in range(repeat_num):
#     print('num:' + str(rp_id))
#     model.fit(train_x, train_y, 
#         epochs=1, batch_size=batchSize, verbose=2, 
#         shuffle=False, validation_data=(val_x, val_y), callbacks=[early_stopping]
#     )
#     model.reset_states()




loss, mse = model.evaluate(test_x, test_y, batch_size=batchSize)
print('mse:', mse)
model.reset_states()

y_predict = model.predict(test_x[-1], batch_size=batchSize)
# 추가 사항
# y_predict = scaler.inverse_transform(y_predict)
# y_predict = np.mean(y_predict)
print(y_predict)

'''
1. 문제점 파악
   - 모델의 최적화 부족
   - 많은 데이터
   - 불필요한 데이터 포함
   - 여러개의 데이터 출력
2. 개선책
   - 모델의 최적화 
   - 3달 정도의 데이터 사용
   - 불필요한 데이터 제거(일자, 거래량, 환율)
   - 여러 데이터들의 평균 값을 최종값으로 사용
3. 판단 지표
   - mse를 이용한 정확도 판단
4. 소스 수정
   - line 26
   - line 41
   - line 77
   - line 80~96 주석 처리
   - line 109
   - line 127
'''

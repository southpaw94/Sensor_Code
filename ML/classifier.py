#!/usr/bin/python3

"""
This is a test multilayer perceptron sequential neural network
model for use on the data collected on 4/5/2016. There is a huge
amount of variation between training runs, but this is because
two of the three classifiers are for two different blades, though
both blades were actually sharp, rather than one dull and one
sharp. Once we collect data with the bad bearing and a truly
dull blade, I will revisit this model.
"""

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.layers.normalization import BatchNormalization
from keras.utils.np_utils import to_categorical
from keras.optimizers import SGD
from sklearn.cross_validation import train_test_split

df = pd.read_csv('training_data.csv')
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

y_train_ohe = to_categorical(y_train)

model = Sequential()
model.add(BatchNormalization(input_shape=(X_train.shape[1],)))
model.add(Dense(input_dim=X_train.shape[1],
                output_dim=500,
                activation='tanh',
                init='uniform'))
model.add(Dense(output_dim=350,
                activation='tanh',
                init='uniform'))
model.add(Dense(output_dim=200,
                activation='tanh',
                init='uniform'))
model.add(Dense(output_dim=50,
                activation='tanh',
                init='uniform'))
model.add(Dropout(0.2))
model.add(Dense(output_dim=y_train_ohe.shape[1],
                activation='softmax',
                init='uniform'))

sgd = SGD(lr=0.001, decay=1e-7, momentum=0.9)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd)
model.fit(X_train, y_train_ohe, validation_split=0.1,
          show_accuracy=True, nb_epoch=5000)

y_train_pred = model.predict_classes(X_train)
y_test_pred = model.predict_classes(X_test)

training_accuracy = len(y_train_pred[y_train_pred==y_train]) / len(y_train_pred)
testing_accuracy = len(y_test_pred[y_test_pred==y_test]) / len(y_test_pred)

print('Training accuracy: %.2f' % (training_accuracy * 100))
print('Testing accuracy: %.2f' % (testing_accuracy * 100))

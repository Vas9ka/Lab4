import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, TimeDistributed, RepeatVector
from tensorflow.keras.utils import plot_model


def build_model(look_back, n_features, forecast_range):
    model_enc_dec = Sequential()
    model_enc_dec.add(LSTM(100, activation='relu', input_shape=(look_back, n_features)))
    model_enc_dec.add(RepeatVector(forecast_range))
    model_enc_dec.add(LSTM(100, activation='relu', return_sequences=True))
    model_enc_dec.add(TimeDistributed(Dense(n_features)))
    model_enc_dec.compile(optimizer='adam', loss='mse')
    plot_model(model=model_enc_dec, show_shapes=True)
    return model_enc_dec


def evaluate_forecast(y_test_inverse, yhat_inverse):
    mse_ = tf.keras.losses.MeanSquaredError()
    mae_ = tf.keras.losses.MeanAbsoluteError()
    mape_ = tf.keras.losses.MeanAbsolutePercentageError()
    mae = mae_(y_test_inverse, yhat_inverse)
    print('mae:', mae)
    mse = mse_(y_test_inverse, yhat_inverse)
    print('mse:', mse)
    mape = mape_(y_test_inverse, yhat_inverse)
    print('mape:', mape)

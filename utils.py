import numpy as np
import json
import sys
from csv import reader
from csv import writer
import urllib.request

import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt


def download_data(url_dictionary):
    # Lets download the files
    for url_title in url_dictionary.keys():
        urllib.request.urlretrieve(url_dictionary[url_title], "./data/" + url_title)


def load_json(json_file_str):
    # Loads  JSON into a dictionary or quits the program if it cannot.
    try:
        with open(json_file_str, "r") as json_file:
            json_variable = json.load(json_file)
            return json_variable
    except Exception:
        sys.exit("Cannot open JSON file: " + json_file_str)


def sum_cases_province(input_file, output_file):
    with open(input_file, "r") as read_obj, open(output_file, 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)

        lines = []
        for line in csv_reader:
            lines.append(line)

        i = 0
        ix = 0
        for i in range(0, len(lines[:]) - 1):
            if lines[i][1] == lines[i + 1][1]:
                if ix == 0:
                    ix = i
                lines[ix][4:] = np.asfarray(lines[ix][4:], float) + np.asfarray(lines[i + 1][4:], float)
            else:
                if not ix == 0:
                    lines[ix][0] = ""
                    csv_writer.writerow(lines[ix])
                    ix = 0
                else:
                    csv_writer.writerow(lines[i])
            i += 1


def split_sequence(sequence, look_back, forecast_horizon):
    X, y = list(), list()
    for i in range(len(sequence)):
        lag_end = i + look_back
        forecast_end = lag_end + forecast_horizon
        if forecast_end > len(sequence):
            break
        seq_x, seq_y = sequence[i:lag_end], sequence[lag_end:forecast_end]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


def inverse_transform(y_test, yhat):
    y_test_reshaped = y_test.reshape(-1, y_test.shape[-1])
    yhat_reshaped = yhat.reshape(-1, yhat.shape[-1])
    return yhat_reshaped, y_test_reshaped


def plot_results(pred_data, real_data):
    fig, ax = plt.subplots(len(pred_data.columns), 1, figsize=(10, 10))
    for i in range(len(ax)):
        ax[i].plot(pred_data[pred_data.columns[i]], label='predicted')
        ax[i].plot(real_data[pred_data.columns[i]].values[-(len(pred_data)):], label='real')
        ax[i].legend(loc='upper right')
        ax[i].set_ylabel(pred_data.columns[i])
    plt.show()


def reformat_data(recovered, confirmed, deaths):
    data = pd.DataFrame(data={'confirmed': confirmed.values.T.reshape(-1),
                              'recovered': recovered.values.T.reshape(-1),
                              'deaths': deaths.values.T.reshape(-1)},
                        index=confirmed.columns,
                        #columns=['confirmed', 'recovered', 'deaths']
                        )
    return data

import pandas as pd
from scipy.optimize import minimize
import numpy as np
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class Learner(object):
    def __init__(self, country, start_date, predict_range, s_0, i_0, r_0, loss=None):
        if not loss:
            self.loss = self.loss
        self.start_date = start_date
        self.predict_range = predict_range
        self.s_0 = s_0
        self.i_0 = i_0
        self.r_0 = r_0
        self.country = country

    def load_confirmed(self):
        df = pd.read_csv('data/time_series_19-covid-Confirmed-country.csv')
        country_df = df[df['Country/Region'] == self.country]
        return country_df.iloc[0].loc[self.start_date:'3/19/21']

    def load_recovered(self):
        df = pd.read_csv('data/time_series_19-covid-Recovered-country.csv')
        country_df = df[df['Country/Region'] == self.country]
        return country_df.iloc[0].loc[self.start_date:'3/19/21']

    def load_dead(self):
        df = pd.read_csv('data/time_series_19-covid-Deaths-country.csv')
        country_df = df[df['Country/Region'] == self.country]
        return country_df.iloc[0].loc[self.start_date:'3/19/21']

    def extend_index(self, index, new_size):
        values = index.values
        current = datetime.strptime(index[-1], '%m/%d/%y')

        while len(values) < new_size:
            current = current + timedelta(days=1)
            values = np.append(values, datetime.strftime(current, '%m/%d/%y'))
        return values

    def predict(self, beta, gamma, data, recovered, death, healed, s_0, i_0, r_0):
        new_index = self.extend_index(data.index, self.predict_range)
        size = len(new_index)

        def SIR(y, t):
            S = y[0]
            I = y[1]
            R = y[2]
            y0 = -beta * S * I
            y1 = beta * S * I - gamma * I
            y2 = gamma * I

            return [y0, y1, y2]

        extended_actual = np.concatenate((data.values, [None] * (size - len(data.values))))
        extended_recovered = np.concatenate((recovered.values, [None] * (size - len(recovered.values))))
        extended_death = np.concatenate((death.values, [None] * (size - len(death.values))))
        extended_healed = np.concatenate((healed.values, [None] * (size - len(healed.values))))
        y0 = [s_0, i_0, r_0]
        tspan = np.arange(0, size, 1)
        res = odeint(SIR, y0, tspan)

        optimal = minimize(loss2, gamma * 0.02, args=(gamma, recovered, healed, death),
                           bounds=[(0.00000001, gamma), ])
        print(optimal)
        a = optimal.x[0]

        prediction_death = a * res[:, 2] / gamma
        prediction_healed = res[:, 2] - prediction_death
        y0 = res[:, 0]
        y1 = res[:, 1]
        y2 = res[:, 2]

        return new_index, extended_actual, extended_recovered, extended_death, y0, y1, y2, prediction_death, prediction_healed, extended_healed

    def train(self):
        self.healed = self.load_recovered()
        self.death = self.load_dead()
        self.recovered = self.healed + self.death
        self.data = (self.load_confirmed() - self.recovered)
        optimal = minimize(self.loss, [0.001, 0.001], args=(self.data, self.recovered, self.s_0, self.i_0, self.r_0),
                           method='L-BFGS-B', bounds=[(0.00000001, 0.4), (0.00000001, 0.4)])
        print(optimal)
        beta, gamma = optimal.x
        self.optimal_beta = beta
        self.optimal_gamma = gamma

    def plot(self):
        beta = self.optimal_beta
        gamma = self.optimal_gamma
        death = self.death
        healed = self.healed
        recovered = self.recovered
        data = self.data

        new_index, extended_actual, extended_recovered, extended_death, y0, y1, y2, prediction_death, prediction_healed, extended_healed = self.predict(
            beta, gamma, data, recovered, death, healed, self.s_0, self.i_0, self.r_0)

        df = pd.DataFrame({'Infected data': extended_actual,
                           'Death data': extended_death,
                           'Susceptible': y0,
                           'Infected': y1,
                           'Predicted Recovered (Alive)': prediction_healed,
                           'Predicted Deaths': prediction_death,
                           'Recovered (Alive)': extended_healed},
                          index=new_index)
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_title(self.country)
        df.plot(ax=ax)
        print(f"country={self.country}, beta={beta:.8f}, gamma={gamma:.8f}, r_0:{(beta / gamma):.8f}")
        fig.savefig(f'plots/{self.country}.png')
        return df

    def loss(self, point, data, recovered, s_0, i_0, r_0):
        size = len(data)
        beta, gamma = point

        def SIR(y, t):
            S = y[0]
            I = y[1]
            R = y[2]
            y0 = -beta * S * I
            y1 = beta * S * I - gamma * I
            y2 = gamma * I
            return [y0, y1, y2]

        y0 = [s_0, i_0, r_0]
        tspan = np.arange(0, size, 1)
        res = odeint(SIR, y0, tspan)
        l1 = np.sqrt(np.mean((res[:, 1] - data) ** 2))
        l2 = np.sqrt(np.mean((res[:, 2] - recovered) ** 2))

        alpha = 0.1
        return alpha * l1 + (1 - alpha) * l2


def loss2(a, gamma, recovered, healed, death):
    estimated_death = a * (recovered / gamma)
    estimated_healed = recovered - estimated_death

    l1 = np.sqrt(np.mean((estimated_death - death) ** 2))
    l2 = np.sqrt(np.mean((estimated_healed - healed) ** 2))

    alpha = 0.9
    return alpha * l1 + (1 - alpha) * l2

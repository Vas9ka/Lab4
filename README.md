# COVID-19 Моделирование распространения и анализ


**Цель:** Данная лабораторная работа показывает модель заболевания населения COVID-19.

--- 

## Данные:
+ data_confirmed (time_series_19-covid-Confirmed-country.csv') - число **заболевших** в день
+ data_recovered ('data/time_series_19-covid-Recovered-country.csv') - данные **выздоровевших** в мире в день
+ data_deaths ('data/time_series_19-covid-Deaths-country.csv') = - данные **погибших** в мире с день

## Модель SIR
Модель фиксирует качественно характер зависимостей, однако может содержать параметры, задающие, например, заразность инфекции, продолжительность инкубационного периода и т.п.

* S - восприимчивые к инфекции,
* I - болеющие,
* R - невосприимчивые к инфекции,
* β - скорость заражения
* γ - скорость выздоровления

## Оценка параметров
1. Susceptible = -β * S * I
2. Infected = β * S * I - γ * I
3. Recovered = γ * I 

Параметры были оптимизированы с помощью функции _minimize_ библиотеки _scipy_. Методом оптимизации является **L-BFGS-B** (Алгоритм Бройдена — Флетчера — Гольдфарба — Шанно)

```sh
optimal = minimize(loss, [0.001, 0.001], args=(self.data, self.recovered, self.s_0, self.i_0, self.r_0),
                           method='L-BFGS-B', bounds=[(0.00000001, 0.4), (0.00000001, 0.4)])
        
```

## Предсказание
Направление изменения числа больных определяется базовым <a href="https://ru.wikipedia.org/wiki/Индекс_репродукции">индексом репродукции</a>  
![](https://latex.codecogs.com/svg.latex?\Large&space;p_0=\frac{\beta}{\gamma})


![](https://latex.codecogs.com/png.latex?%5Cfrac%7BdI%7D%7Bdt%7D%3D%5Cgamma%20I%28p_0%5Cfrac%7BS%7D%7BN%7D-1%29)

## Результаты:
![Italy_before](https://raw.githubusercontent.com/Vas9ka/Lab4/master/Italy_before.png)
Модель заболеваний COVID-19 В Италии без учета данных локдауна
![Italy_after](https://raw.githubusercontent.com/Vas9ka/Lab4/master/Italy_after.png)
Модель заболеваний COVID-19 В Италии с учетом данных локдауна

![Germany_before](https://raw.githubusercontent.com/Vas9ka/Lab4/master/Germany_before.png)
Модель заболеваний COVID-19 в Германии без учета данных локдауна

![Germany_after](https://raw.githubusercontent.com/Vas9ka/Lab4/master/Germany_after.png)
Модель заболеваний COVID-19 в Германии с учетом данных локдауна


## Вывод
В ходе работы была выявлена закономерность влияния локдаунов и демократических криетериев на предсказание распростронения COVID-19. 
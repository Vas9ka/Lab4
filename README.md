# COVID-19 Моделирование распространения и анализ


**Цель:** Данная лабораторная работа показывает модель заболевания населения COVID-19.

--- 

## Данные:
+ data_confirmed (time_series_19-covid-Confirmed-country.csv') - число **заболевших**
+ data_recovered ('data/time_series_19-covid-Recovered-country.csv') - данные **выздоровевших** в мире
+ data_deaths ('data/time_series_19-covid-Deaths-country.csv') = - данные **погибших** в мире

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

## Пресказание
Направление изменения числа больных определяется базовым <a href="https://ru.wikipedia.org/wiki/Индекс_репродукции">индексом репродукции</a> $$ ρ_{0} = β / γ $$

$${ dI\over dt} = γI(ρ_{0} {S \over N}- 1)$$


## Результаты:
![Italy](https://raw.githubusercontent.com/Vas9ka/Lab4/master/Italy.png)
![Germany](https://raw.githubusercontent.com/Vas9ka/Lab4/master/Germany.png)
![Russia](https://raw.githubusercontent.com/Vas9ka/Lab4/master/Russia.png)
![China](https://raw.githubusercontent.com/Vas9ka/Lab4/master/China.png)
![Japan](https://raw.githubusercontent.com/Vas9ka/Lab4/master/Japan.png)

## Вывод
В ходе работы была выявлена закономерность влияния локдаунов и демократических криетериев на предсказание распростронения COVID-19. 



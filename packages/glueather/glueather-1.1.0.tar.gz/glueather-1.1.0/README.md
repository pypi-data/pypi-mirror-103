# glueather

A simple Python/Qt weather application using the OpenWeather API.

glueather allows you to fetch the current weather as well as hourly and daily forecasts for any given location. The interface is extremely simple to use and multiplatform, working exactly the same across a variety of operating systems like MacOS, Linux or Windows.

Instead of showing fancy graphics glueather focuses on the actual meteorological data, neatly presented in a tabular fahsion, particularly useful for the forecasts. The data is provided by the free [OpenWeather API](https://openweathermap.org/), through thousands of distributed home weather stations in addition to standard sources of meteorological data.

## Screenshots

![Windows screenshot 1](https://i.imgur.com/w3ZUaKu.png)

![Linux screenshot 1](https://i.imgur.com/bqYEQzU.png)

![Mac OS X screenshot 1](https://i.imgur.com/DhY2P6o.png)

# Features

* Simple interface
* Multiplatform (MacOS/Linux/Windows)
* Current weather
* Hourly forecast
* Daily forecast
* Units (Celsius/Fahrenheit)
* Persistent settings
* Advanced weather API (OpenWeather)

# Dependencies

* Python >= 3.7.0
* pyowm >= 3.2.0
* PyQt5 >= 5.15.1 (on Debian Stable use specifically 5.12.1) 

# Install (pip)

```
pip install glueather
```

# Install (source)

## Global

```
git clone https://github.com/vascocosta/glueather.git
cd glueather
pip install -r requirements.txt
```

## Venv

### MacOS/Linux

```
git clone https://github.com/vascocosta/glueather.git
cd glueather
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

```
git clone https://github.com/vascocosta/glueather.git
cd glueather
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

# Run (pip)

```
glueather
```

# Run (source)

```
cd glueather/src/
python glueather.py
```

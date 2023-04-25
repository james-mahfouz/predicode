import { useEffect, useState } from "react";
import WeatherInput from "../../components/WeatherApp/Input";
import WeatherData from "../../components/WeatherApp/WeatherData";
import axios from "axios";

const WeatherPage = () => {
  const [city, setCity] = useState("Beirut");
  const [weatherData, setWeatherData] = useState();

  const handleInputChange = (e) => {
    setCity(e.target.value)
  }

  const handleSubmit = async (e) => {
    const response = await axios.get('https://weatherapi-com.p.rapidapi.com/current.json?q=' + city, {
      headers: {
        'X-RapidAPI-Key': 'c9c35b18b5msh31a353da7a72fe6p13e70djsn61f4cf39c8c9',
        'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'
      }
    })

    setWeatherData(response.data)
  }

  return (
    <div>
      <h1>Weather App</h1>
      <WeatherInput onChange={handleInputChange} onSubmit={handleSubmit} />
      {weatherData && <WeatherData data={weatherData} />}
    </div>
  )
}

export default WeatherPage;
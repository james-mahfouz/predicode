const WeatherData = ({ data }) => {
  return (
    <>
      <p>{data?.current.temp_c}</p>
      <p>{data?.current.feelslike_c}</p>
      <p>{data?.current.humidity}</p>
    </>
  )
}

export default WeatherData  
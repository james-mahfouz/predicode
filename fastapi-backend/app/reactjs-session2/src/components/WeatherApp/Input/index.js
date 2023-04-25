import { useState } from "react"

const WeatherInput = ({ onChange, onSubmit }) => {

  return (
    <div>
      <input placeholder="Enter city name" onChange={onChange} />
      <button onClick={onSubmit}>Submit</button>
    </div>
  )
}

export default WeatherInput
import { Link, useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  const handleNavigateTodo = () => {
    navigate("/todo");
  }
  const handleNavigateWeather = () => {
    navigate("/weather");
  }

  return (
    <div>
      <button onClick={handleNavigateTodo}>Todo App</button>
      <button onClick={handleNavigateWeather}>Weather App</button>
      {/* <Link to="/todo">Todo App</Link>
      <Link to="/weather" >Weather App</Link> */}
    </div>
  );
}

export default HomePage;
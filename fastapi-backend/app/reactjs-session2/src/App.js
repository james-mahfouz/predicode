import React, { useState } from 'react';
import TodoList from './components/TodoList';
import { Routes, Route, Router } from "react-router-dom"
import HomePage from './Pages/HomePage';
import TodoListPage from './Pages/TodoListPage';
import WeatherPage from './Pages/WeatherAppPage';

function App() {

  return (
    // <div>
    //   {/* <TodoList /> */}
    // </div>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/todo" element={<TodoListPage />} />
      <Route path="/weather" element={<WeatherPage />} />
      <Route path="*" element={<div>404</div>} />
    </Routes>
  );
}

export default App;

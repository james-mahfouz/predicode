import { useState } from "react";
import TodoInput from "./TodoInput";
import TodoItemList from "./TodoItemList";
const TodoList = () => {
  const [value, setValue] = useState("");
  const [todos, setTodos] = useState([])

  const handleChange = (e) => {
    setValue(e.target.value)
  }

  const addTodo = () => {
    setTodos([...todos, value])
    setValue("")
  }

  return (
    <div>
      <h1>Todo List</h1>
      <TodoInput value={value} handleChange={handleChange} addTodo={addTodo} />
      <TodoItemList todos={todos} />
    </div>
  )
}

export default TodoList

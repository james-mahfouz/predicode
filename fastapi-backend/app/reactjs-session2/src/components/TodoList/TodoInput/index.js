const TodoInput = ({ handleChange, addTodo, value }) => {

  return (
    <div>
      <input value={value} onChange={handleChange} />
      <button onClick={addTodo}>Add</button>
    </div>
  )
}

export default TodoInput
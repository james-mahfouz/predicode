import Item from "./Item"

const TodoItemList = ({ todos }) => {
  return (
    <ul>
      {todos.map((todo, index) => (<Item key={index} todo={todo} />))}
    </ul>
  )
}

export default TodoItemList
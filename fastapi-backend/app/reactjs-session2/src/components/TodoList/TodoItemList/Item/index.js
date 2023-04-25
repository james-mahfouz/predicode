const Item = ({ todo }) => {

  return (<li>
    {todo} <button className="button">remove</button>
  </li>)
}

export default Item;
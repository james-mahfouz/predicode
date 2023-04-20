import logo from "../../assets/logo.png";
import "./index.css";

const Admin = () => {
  return (
    <div className="admin-body">
      <section className="right">
        <div className="admin-logo">
          <img src={logo} alt="" />
        </div>
        <div className="options">
          <div className="option">
            <h4>Display Users</h4>
          </div>
          <div className="option">
            <h4>Files Uploaded</h4>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Admin;

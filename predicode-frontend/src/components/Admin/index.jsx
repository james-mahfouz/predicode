import logo from "../../assets/logo.png";
import "./index.css";
import DisplayUsers from "../DisplayUsers";
import DisplayFiles from "../DisplayFiles";
import { useState, useEffect } from "react";

const Admin = () => {
  const [adminFunction, setAdminFunction] = useState(<DisplayUsers />);
  const [adminName, setAdminName] = useState("");

  useEffect(() => {
    const admin_name = localStorage.getItem("admin_name");
    if (admin_name) {
      setAdminName(admin_name);
    }
  }, []);

  const handleOption = (option) => {
    option === 1
      ? setAdminFunction(<DisplayFiles />)
      : setAdminFunction(<DisplayUsers />);
  };
  return (
    <div className="admin-body">
      <section className="left">
        <div className="admin-logo">
          <img src={logo} alt="" />
        </div>
        <div className="options">
          <div className="option" onClick={() => handleOption(2)}>
            <h4>Display Users</h4>
          </div>
          <div className="option" onClick={() => handleOption(1)}>
            <h4>Files Uploaded</h4>
          </div>
        </div>
      </section>

      <section className="right">
        <div className="top-bar">
          <div className="admin-name">
            <h3>{adminName}</h3>
          </div>
          <div className="logout-btn">
            <h4>Logout</h4>
          </div>
        </div>

        <div className="infos">{adminFunction}</div>
      </section>
    </div>
  );
};

export default Admin;

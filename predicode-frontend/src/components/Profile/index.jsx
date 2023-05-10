import logo from "../../assets/logo-white-01.png";
import "../Admin/index.css";
import ProfileHistory from "../ProfileHistory";
import UserProfile from "../UserProfile";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Admin = () => {
  const [adminFunction, setAdminFunction] = useState(
    <div className="profile">
      <UserProfile />
    </div>
  );
  const [userName, setUserName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const getUserName = () => {
      const user_name = localStorage.getItem("user_name");
      if (user_name) {
        setUserName(user_name);
      } else {
        setTimeout(getUserName, 1000);
      }
    };
    getUserName();
  }, []);

  const handleOption = (option) => {
    option === 1
      ? setAdminFunction(<ProfileHistory />)
      : setAdminFunction(
          <div className="profile">
            <UserProfile />
          </div>
        );
  };

  const goLanding = () => {
    navigate("/");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("admin_name");
    navigate("/");
  };
  return (
    <div className="admin-body">
      <section className="left">
        <div className="admin-logo" onClick={goLanding}>
          <img src={logo} alt="" />
        </div>
        <div className="options">
          <div className="option" onClick={() => handleOption(2)}>
            <h4>Edit Profile</h4>
          </div>
          <div className="option" onClick={() => handleOption(1)}>
            <h4>Your History</h4>
          </div>
        </div>
      </section>

      <section className="right">
        <div className="top-bar">
          <div className="admin-name">
            <h3>{userName}</h3>
          </div>
          <div className="logout-btn" onClick={() => handleLogout()}>
            <h4>Logout</h4>
          </div>
        </div>

        <div className="infos">{adminFunction}</div>
      </section>
    </div>
  );
};

export default Admin;

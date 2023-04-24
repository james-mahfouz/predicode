import logo from "../../assets/logo.png";
import React, { useState, useEffect } from "react";

const Sidebar = () => {
  const [visibleRight, setVisibleRight] = useState(false);
  const [username, setUsername] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);

  return (
    <section className="sidebar">
      <Sidebar
        visible={visibleRight}
        position="right"
        onHide={() => setVisibleRight(false)}
      >
        <div className="sidebar-logo">
          <img src={logo} />
        </div>

        <div className="user-infos">
          <h2>Welcome {username}</h2>
          <p>
            Predicode, the website that take your app source code and predict
            your app rating to have an idea on how to proceed with your idea
          </p>
        </div>
        <div className="sidebar-buttons">
          {isAdmin && (
            <div className="logout">
              <Button
                label="Admin Panel"
                className="btn logout"
                onClick={goAdminPage}
              />
            </div>
          )}
          <div className="logout sidebar-logout">
            <Button
              label="Logout"
              className="btn logout"
              onClick={handleLogout}
            />
          </div>
        </div>
      </Sidebar>
    </section>
  );
};

export default Sidebar;

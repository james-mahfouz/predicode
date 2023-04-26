import logo from "../../assets/logo.png";
import React, { useState, useEffect } from "react";
import axios from "axios";

import { useNavigate } from "react-router-dom";
import { Button } from "primereact/button";
import { Sidebar } from "primereact/sidebar";

const Navbar = (props) => {
  const [isSmallScreen, setIsSmallScreen] = useState(false);
  const [signedIn, setSignedIn] = useState(false);
  const [visibleRight, setVisibleRight] = useState(false);
  const [username, setUsername] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);

  const apiUrl = process.env.API_URL;
  const navigate = useNavigate();
  useEffect(() => {
    function handleResize() {
      setIsSmallScreen(window.innerWidth <= 720);
    }

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    const verify = async () => {
      try {
        const response = await axios.get(apiUrl + "user/verify", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        setUsername(response.data.username);
        setSignedIn(true);
        if (response.data.role === "admin") {
          setIsAdmin(true);
        }
      } catch (e) {
        console.log(e);
      }
    };
    verify();
  }, []);

  const go_signin = () => {
    navigate("/login");
  };

  const handleLogout = () => {
    props.onLogout();
    localStorage.removeItem("token");
    localStorage.removeItem("admin_name");
    setVisibleRight(false);
    setSignedIn(false);
  };

  const goAdminPage = () => {
    navigate("/admin");
  };
  return (
    <div>
      <section className="navbar">
        <div className="logo">
          <img src={logo} />
        </div>
        {!signedIn && (
          <div className="signin_button">
            <Button
              label={!isSmallScreen && "Sign-In"}
              icon="pi pi-sign-in"
              className="btn"
              onClick={go_signin}
            />
          </div>
        )}

        {signedIn && !isSmallScreen && (
          <div className="pages">
            <h5 className="page">Home</h5>
            <h5 className="page">Upload</h5>
            {isAdmin && (
              <h5 className="page" onClick={goAdminPage}>
                Admin
              </h5>
            )}
            <div className="navbar-logout page">
              <Button
                label="Logout"
                className="btn logout"
                onClick={handleLogout}
              />
            </div>
          </div>
        )}
        {signedIn && isSmallScreen && (
          <div className="signin_button">
            <Button
              icon="pi pi-user"
              rounded
              outlined
              severity="info"
              aria-label="User"
              onClick={() => setVisibleRight(true)}
              style={{ borderWidth: "3px" }}
              className="bolder-icon"
            />
          </div>
        )}
      </section>

      <section className="sidebar">
        {isSmallScreen && (
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
                Predicode, the website that take your app source code and
                predict your app rating to know how to proceed.
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
        )}
      </section>
    </div>
  );
};

export default Navbar;

import logo from "../../assets/logo.png";
import background from "../../assets/landing-background.png";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Button } from "primereact/button";
import { FaSignInAlt } from "react-icons/fa";
import "./index.css";

const Landing = () => {
  const [isSmallScreen, setIsSmallScreen] = useState(false);
  useEffect(() => {
    function handleResize() {
      setIsSmallScreen(window.innerWidth <= 720);
    }

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, []);
  return (
    <div className="body">
      <section className="navbar">
        <div className="logo">
          <img src={logo} />
        </div>
        <div className="signin_button">
          <Button
            label={!isSmallScreen && "Sign-In"}
            icon="pi pi-sign-in"
            className="btn"
          />
        </div>
      </section>

      <section className="landing">
        <div className="landing_picture">
          <img src={background} alt="" className="wlc_picture" />
        </div>
        <div className="marketing_text">
          <p>Predict Your App's Success and Move Forward with Confidence</p>
        </div>
      </section>
    </div>
  );
};
export default Landing;

import background from "../../assets/landing-background.png";
import logo from "../../assets/logo.png";
import form_upload from "../../assets/form_upload.png";
import form_result from "../../assets/form_result.png";
import right_arrow from "../../assets/right-arrow.png";
import upload from "../../assets/upload.jpg";
import wait from "../../assets/wait.jpg";
import create from "../../assets/create.jpg";
import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../Navbar";

import { useNavigate } from "react-router-dom";
import { Button } from "primereact/button";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";

import "./index.css";

const Landing = () => {
  const [files, setFiles] = useState([]);
  const [signedIn, setSignedIn] = useState(false);

  const apiUrl = process.env.API_URL;
  const navigate = useNavigate();

  useEffect(() => {
    const getFiles = async () => {
      try {
        const response = await axios.get(apiUrl + "user/verify", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setSignedIn(true);
      } catch (e) {}
    };
    getFiles();
  }, []);

  const goUpload = () => {
    if (signedIn) {
      navigate("/upload");
    } else {
      navigate("login");
    }
  };
  const handleLogout = () => {
    setSignedIn(false);
  };

  return (
    <div className="landing-body">
      <Navbar onLogout={handleLogout} />

      <section className="landing">
        <div className="landing_picture">
          <img src={background} alt="" className="wlc_picture" />
        </div>
        <div className="marketing_text">
          <p>Predict Your App's Success and Move Forward with Confidence</p>
          <div className="go_upload_button">
            <Button
              label={"Try Your Code Now"}
              className="btn footer-btn"
              onClick={goUpload}
            />
          </div>
        </div>
      </section>

      <section className="use_it">
        <div>
          <h1>How to use it</h1>
        </div>

        <div className="use_it_steps">
          <div className="use_it_step">
            <img src={create} alt="" />
            <h4>Create an account</h4>
          </div>

          <div className="use_it_step">
            <img src={upload} alt="" />
            <h4>Upload your code</h4>
          </div>

          <div className="use_it_step">
            <img src={wait} alt="" />
            <h4>Wait for the result</h4>
          </div>
        </div>
      </section>

      <section className="expectation">
        <div className="expectation_header">
          <h1>What to expect</h1>
        </div>
        <div className="uploaded_codes">
          <div className="form_upload">
            <img src={form_upload} alt="" />
          </div>

          <div className="right_arrow">
            <img src={right_arrow} alt="" />
          </div>

          <div className="form_result">
            <img src={form_result} alt="" />
          </div>
        </div>
      </section>

      <section className="footer">
        <div className="upper_footer">
          <div className="footer-btn">
            <Button
              label={"Try Your Code Now"}
              className="btn footer-btn"
              onClick={goUpload}
            />
          </div>
          <div className="logo footer_logo">
            <img src={logo} alt="" />
          </div>
        </div>
        <div className="footer_copyright">
          <p>Copyright © 2023 PREDICODE. All rights reserved.</p>
        </div>
      </section>
    </div>
  );
};
export default Landing;

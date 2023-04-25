import background from "../../assets/landing-background.png";
import logo from "../../assets/logo.png";
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
        const response = await axios.get(apiUrl + "user/get_files", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setFiles(response.data.files);
        setSignedIn(true);
      } catch (e) {
        console.log(e);
      }
    };
    getFiles();
  }, []);

  const goUpload = () => {
    if (signedIn) {
    }
  };

  return (
    <div className="landing-body">
      <Navbar />

      <section className="landing">
        <div className="landing_picture">
          <img src={background} alt="" className="wlc_picture" />
        </div>
        <div className="marketing_text">
          {/* <h3>Want to know your app fututre?</h3> */}
          <p>Predict Your App's Success and Move Forward with Confidence</p>
          <div className="go_upload_button">
            <Button
              label={"Try Your Code Now"}
              className="btn footer-btn"
              onClick={() =>
                document.querySelector(".card").scrollIntoView({
                  behavior: "smooth",
                  block: "start",
                })
              }
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
          <DataTable value={files} style={{ width: "80%", height: "auto" }}>
            <Column
              field="name"
              header="Code Uploaded"
              headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
            ></Column>
            <Column
              field="result"
              header="Result"
              headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
            ></Column>
          </DataTable>
        </div>
      </section>

      <section className="footer">
        <div className="upper_footer">
          <div className="footer-btn">
            <Button
              label={"Try Your Code Now"}
              className="btn footer-btn"
              onClick={() =>
                document.querySelector(".card").scrollIntoView({
                  behavior: "smooth",
                  block: "start",
                })
              }
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

import logo from "../../assets/logo.png";
import React, { useState, useEffect } from "react";
import axios from "axios";
import JSZip from "jszip";

import { useNavigate } from "react-router-dom";
import { Button } from "primereact/button";
import { FileUpload } from "primereact/fileupload";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Sidebar } from "primereact/sidebar";
import { InputNumber } from "primereact/inputnumber";
import { Message } from "primereact/message";

const Upload = () => {
  const [isSmallScreen, setIsSmallScreen] = useState(false);
  const [files, setFiles] = useState([]);
  const [signedIn, setSignedIn] = useState(false);
  const [visibleRight, setVisibleRight] = useState(false);
  const [username, setUsername] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [reviews, setReviews] = useState("");
  const [appName, setAppName] = useState("");
  const [price, setPrice] = useState("");
  const [ageFrom, setAgeFrom] = useState("");
  const [ageTo, setAgeTo] = useState("");
  const [appVersion, setAppVersion] = useState("");
  const [error, setError] = useState("");

  const apiUrl = process.env.API_URL;
  const versionRegex = /^(\d+)\.(\d+)\.(\d+)$/;
  const navigate = useNavigate();
  const onUpload = (event) => {
    if (!signedIn) {
      navigate("/login");
      return;
    }

    if (!appName) {
      setError("Please enter your app name");
      return;
    }

    if (!price) {
      setError("Please enter your app price");
      return;
    }

    if (!ageFrom) {
      setError("Please enter your app age Range");
      return;
    }

    if (!ageTo) {
      setError("Please enter your app age Range");
      return;
    }

    if (ageFrom > ageTo) {
      const temp = ageFrom;
      setAgeFrom(ageTo);
      setAgeTo(temp);
    }
    if (!appVersion) {
      setError("Please enter your app current Version");
      return;
    }
    if (!versionRegex.test(appVersion)) {
      setError(`Version must be in this format: 1.0.0`);
      return;
    }

    const uploaded_file = event.files[0];
    if (uploaded_file.type === "application/zip") {
      const reader = new FileReader();
      reader.readAsDataURL(uploaded_file);

      reader.onload = () => {
        const encodedData = reader.result.split(",");
        const data = {
          data: encodedData[1],
          name: uploaded_file.name,
          content_type: encodedData[0],
        };

        const token = localStorage.getItem("token");

        axios
          .post(apiUrl + "user/upload_files/", data, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {});
      };
    } else {
      console.log("File not zipped");
    }
  };
  return (
    <section className="upload-wrapper">
      <div className="landing-wrapper">
        <FileUpload
          name="demo[]"
          customUpload={true}
          uploadHandler={onUpload}
          accept="application/zip"
          webkitdirectory="true"
          maxFileSize={100000000000000}
          emptyTemplate={
            <p className="m-0">
              Upload your zipped code folder and see your rating
            </p>
          }
        />
        <div className="form">
          {error && (
            <Message
              severity="error"
              text={error}
              style={{ width: "100%", marginBottom: "10px" }}
            />
          )}
          <div className="inputfield">
            <label>App Name</label>
            <input
              type="text"
              className="register_input"
              value={appName}
              onChange={(e) => setAppName(e.target.value)}
              // style={{ borderColor: emailError ? "red" : "#D8E9EF" }}
            ></input>
          </div>
          <div className="inputfield">
            <label>Price ($)</label>
            <input
              type="number"
              className="register_input"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              // style={{ borderColor: passwordError ? "red" : "#D8E9EF" }}
            ></input>
          </div>

          <div className="inputfield">
            <label>Age Range (from)</label>
            <input
              type="number"
              className="register_input"
              value={ageFrom}
              min={0}
              max={100}
              onChange={(e) => setAgeFrom(e.target.value)}
              // style={{ borderColor: passwordError ? "red" : "#D8E9EF" }}
            ></input>
            {/* <InputNumber
                inputId="minmax-buttons"
                className="register_input"
                value={ageFrom}
                onValueChange={(e) => setAgeFrom(e.value)}
                mode="decimal"
                showButtons
                min={0}
                max={100}
                style={{ border: "None" }}
              /> */}
          </div>
          <div className="inputfield">
            <label>
              Age Range <br />
              (to)
            </label>
            <input
              type="number"
              className="register_input"
              value={ageTo}
              onChange={(e) => setAgeTo(e.target.value)}
              // style={{ borderColor: passwordError ? "red" : "#D8E9EF" }}
            ></input>
            {/* <InputNumber
                inputId="minmax-buttons"
                className="register_input"
                value={ageTo}
                onValueChange={(e) => setAgeTo(e.value)}
                mode="decimal"
                showButtons
                min={0}
                max={100}
                style={{ border: "None" }}
              /> */}
          </div>
          <div className="inputfield">
            <label>Current App version</label>
            <input
              type="text"
              className="register_input"
              value={appVersion}
              onChange={(e) => setAppVersion(e.target.value)}
            ></input>
          </div>
        </div>
      </div>
    </section>
  );
};
export default Upload;

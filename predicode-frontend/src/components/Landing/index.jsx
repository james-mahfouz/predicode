import logo from "../../assets/logo.png";
import background from "../../assets/landing-background.png";
import upload from "../../assets/upload.jpg";
import wait from "../../assets/wait.jpg";
import create from "../../assets/create.jpg";
import React, { useState, useEffect } from "react";
import axios from "axios";

import { useNavigate } from "react-router-dom";
import { Button } from "primereact/button";
import { FileUpload } from "primereact/fileupload";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Sidebar } from "primereact/sidebar";
import { InputText } from "primereact/inputtext";

import "./index.css";

const Landing = () => {
  const [isSmallScreen, setIsSmallScreen] = useState(false);
  const [files, setFiles] = useState([]);
  const [signedIn, setSignedIn] = useState(false);
  const [uploadedFile, setUploadedFile] = useState([]);
  const [visibleRight, setVisibleRight] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("james@gmail.com");
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
    const getFiles = async () => {
      try {
        const response = await axios.get(apiUrl + "user/get_files", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setUsername(response.data.user_name);
        setFiles(response.data.files);
        setSignedIn(true);
        if (response.data.role === "admin") {
          setIsAdmin(true);
        }
      } catch (e) {
        console.log(e);
      }
    };
    getFiles();
  }, []);

  const go_signin = () => {
    navigate("/login");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("admin_name");
    setVisibleRight(false);
    setSignedIn(false);
  };

  const goAdminPage = () => {
    navigate("/admin");
  };

  const onUpload = (event) => {
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
    <div className="landing-body">
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
        {signedIn && (
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

      <section className="landing">
        <div className="landing_picture">
          <img src={background} alt="" className="wlc_picture" />
        </div>
        <div className="marketing_text">
          <p>Predict Your App's Success and Move Forward with Confidence</p>
        </div>
      </section>

      <section className="upload">
        <div className="card">
          <FileUpload
            name="demo[]"
            customUpload={true}
            uploadHandler={onUpload}
            multiple
            accept="application/zip"
            maxFileSize={100000000000000}
            emptyTemplate={
              <p className="m-0">
                Upload your zipped code folder and see your rating
              </p>
            }
          />
        </div>{" "}
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

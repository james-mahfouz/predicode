import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../Login/index.css";
import logo from "../../assets/logo.png";
import { Message } from "primereact/message";
import { FaEye, FaEyeSlash } from "react-icons/fa";

function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [verifyPassword, setVerifyPassword] = useState("");
  const [error, setError] = useState("");
  const [nameError, setNameError] = useState(false);
  const [emailError, setEmailError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  const [showPassword, setShowPassword] = useState(false); // add state for showing password

  const navigate = useNavigate();
  const apiUrl = process.env.API_URL;

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setEmailError(false);
    setNameError(false);
    setPasswordError(false);
    if (!name) {
      setError("Please enter your name.");
      setNameError(true);
      return;
    }

    if (!email) {
      setError("Please enter your email.");
      setEmailError(true);
      return;
    }

    if (!password) {
      setError("Please enter your password.");
      setPasswordError(true);
      return;
    }
    console.log("hewear");

    if (password != verifyPassword) {
      setError("Password different from the verified password");
      setPasswordError(true);
      return;
    }
    console.log("sureee ");
    const data = {
      name: name,
      email: email,
      password: password,
    };

    try {
      const response = await axios.post(apiUrl + "auth/register", data);
      localStorage.setItem("token", response.data[0].token);
      navigate("/");
    } catch (error) {
      setError(error.response.data.detail.detail);
      if (error.response.data.detail.error == "name") {
        setNameError(true);
      }
      if (error.response.data.detail.error == "email") {
        setEmailError(true);
      }
      if (error.response.data.detail.error == "password") {
        setPasswordError(true);
      }
    }
  };

  return (
    <div className="signin-wrapper">
      <div className="signin-logo">
        <img src={logo} alt=""></img>
      </div>
      <div className="wrapper">
        <div className="title">
          <h2>Sign-Up</h2>
        </div>

        <div className="form">
          <div className="inputfield">
            <label>Name</label>
            <input
              type="text"
              className="register_input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={{ borderColor: nameError ? "red" : "#D8E9EF" }}
            ></input>
          </div>

          <div className="inputfield">
            <label>Email</label>
            <input
              type="email"
              className="register_input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ borderColor: emailError ? "red" : "#D8E9EF" }}
            ></input>
          </div>

          <div className="inputfield">
            <label>Password</label>
            <div className="password-input-container">
              <input
                type={showPassword ? "text" : "password"}
                className="register_input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ borderColor: passwordError ? "red" : "#D8E9EF" }}
              ></input>
              <button type="button" onClick={togglePasswordVisibility}>
                {showPassword ? <FaEyeSlash /> : <FaEye />}{" "}
              </button>
            </div>
          </div>

          <div className="inputfield">
            <label className="verify_password">Verify Password</label>
            <input
              type="password"
              className="register_input"
              value={verifyPassword}
              onChange={(e) => setVerifyPassword(e.target.value)}
              style={{ borderColor: passwordError ? "red" : "#D8E9EF" }}
            ></input>
          </div>

          {error && (
            <Message
              severity="error"
              text={error}
              style={{ width: "100%", marginBottom: "10px" }}
            />
          )}

          <div className="inputfield">
            <input
              type="submit"
              value="Register"
              className="btn"
              onClick={handleSubmit}
            ></input>
          </div>

          <p>
            Have an account? <a href="/login">Login</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Signup;

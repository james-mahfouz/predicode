import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../Login/index.css";
import logo from "../../assets/logo.png";


function Signup() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        console.log(name, email, password)
        const data = {
            "name": name,
            "email": email,
            "password": password
        }

        try {
            const response = await axios.post('http://localhost:4000/auth/register', data);
            localStorage.setItem('token', response.data.token);
            navigate("/")
        } catch (error) {
            console.log(error);
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
                        <input type="text" className="register_input" value={name} onChange={(e) => setName(e.target.value)}></input>
                    </div>


                    <div className="inputfield">
                        <label>Email</label>
                        <input type="email" className="register_input" value={email} onChange={(e) => setEmail(e.target.value)}></input>
                    </div>

                    <div className="inputfield">
                        <label>Password</label>
                        <input type="password" className="register_input" value={password} onChange={(e) => setPassword(e.target.value)}></input>
                    </div>

                    <div className="inputfield">
                        <input type="submit" value="Register" className="btn" onClick={handleSubmit}></input>
                    </div>

                    <p>Have an account? <a href="/login">Login</a></p>
                </div>
            </div>
        </div>
    );
}

export default Signup;

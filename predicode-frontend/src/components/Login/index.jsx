import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import "./index.css"
import logo from "../../assets/logo.png";


const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const apiUrl = process.env.API_URL;
    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post(apiUrl + 'auth/login', {
                "email": email,
                "password": password
            })
            console.log(response)

            localStorage.setItem('token', response.data.token);
            // navigate("/")

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
                    <h2>Sign-In</h2>
                </div>

                <div className="form">
                    <div className="inputfield">
                        <label>Email</label>
                        <input type="email" className="register_input" value={email} onChange={(e) => setEmail(e.target.value)}></input>
                    </div>

                    <div className="inputfield">
                        <label>Password</label>
                        <input type="password" className="register_input" value={password} onChange={(e) => setPassword(e.target.value)}></input>
                    </div>

                    <div className="inputfield">
                        <input type="submit" value="Login" className="btn" onClick={handleSubmit}></input>
                    </div>

                    <p>Don't have an account? <a href="/signup">Sign-Up</a></p>

                </div>
            </div>
        </div>
    );
}

export default Login;
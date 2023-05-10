import "@fortawesome/fontawesome-free/css/all.min.css";
import "../Admin/index.css";
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import Avatar from "react-avatar";
import no_pp from "../../assets/no_pp.webp";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";

const UserProfile = () => {
  const [history, setHistory] = useState([]);
  const [name, setName] = useState("james");
  const [email, setEmail] = useState("email@gmail.com");
  const [profilePic, setProfilePic] = useState(no_pp);
  const [editable, setEditable] = useState(false);
  const [loading, setLoading] = useState(false);

  const apiUrl = process.env.API_URL;

  useEffect(() => {
    const getUser = async () => {
      try {
        const response = await axios.get(apiUrl + "user/verify", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setProfilePic(response.data.profile_picture);
        setEmail(response.data.email);
        setName(response.data.username);
        localStorage.setItem("user_name", response.data.user_name);
      } catch (e) {}
    };
    getUser();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
  };
  const handleEditClick = () => {
    setEditable(true);
  };

  const handleSaveClick = () => {
    setEditable(false);
    // handle save logic here
  };

  const handleAvatarClick = () => {
    document.getElementById("fileInput").click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => {
      setProfilePic(reader.result);
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="users_info">
      <h1>Edit Profile</h1>
      <div className="profile-pic">
        <Avatar
          src={profilePic}
          name={name}
          size="150"
          round={true}
          onClick={handleAvatarClick}
          className="user_pp"
        />
        <FontAwesomeIcon icon={faPen} className="edit-icon" />

        <input
          type="file"
          id="fileInput"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
      </div>
      <form onSubmit={handleSubmit}>
        <>
          {editable ? (
            <div className="editable">
              <InputText
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
              <Button icon="pi pi-check" onClick={handleSaveClick} />
            </div>
          ) : (
            <div className="editable">
              <span>{name}</span>
              <Button
                icon="pi pi-pencil"
                onClick={handleEditClick}
                rounded
                text
              />
            </div>
          )}
        </>
        <>
          {editable ? (
            <div className="editable">
              <InputText
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <Button icon="pi pi-check" onClick={handleSaveClick} />
            </div>
          ) : (
            <div className="editable">
              <span>{email}</span>
              <Button
                icon="pi pi-pencil"
                onClick={handleEditClick}
                rounded
                text
              />
            </div>
          )}
        </>
        <Button
          type="submit"
          label="Save"
          loading={loading}
          // onClick={load}
          className="update-info"
        />
      </form>
    </div>
  );
};
export default UserProfile;

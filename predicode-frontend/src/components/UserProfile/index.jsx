import "../Admin/index.css";
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import Avatar from "react-avatar";

import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Inplace, InplaceDisplay, InplaceContent } from "primereact/inplace";

const UserProfile = () => {
  const [history, setHistory] = useState([]);
  const [name, setName] = useState("james");
  const [email, setEmail] = useState("email@gmail.com");
  const [profilePic, setProfilePic] = useState("hello");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, email, profilePic });
  };
  const apiUrl = process.env.API_URL;
  useEffect(() => {
    const getUsers = async () => {
      try {
        const response = await axios.get(apiUrl + "user/get_history", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setHistory(response.data.history);
        localStorage.setItem("user_name", response.data.user_name);
      } catch (e) {}
    };
    getUsers();
  }, []);

  return (
    <div className="display-users">
      <h1>History</h1>
      <div className="card" style={{ padding: "0rem" }}>
        <DataTable
          value={history}
          scrollable
          scrollHeight="400px"
          virtualScrollerOptions={{ itemSize: 46 }}
          tableStyle={{ minWidth: "50rem" }}
          sortMode="multiple"
        >
          <Column
            field="name"
            header="Name"
            sortable
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            header="Rating"
            field="rating"
            sortable
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            header="Maintainability"
            sortable
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
            body={(rowData) => (
              <Inplace closable>
                <InplaceDisplay>View Maintainability</InplaceDisplay>
                <InplaceContent>
                  <p className="m-0">{rowData.maintainability}</p>
                </InplaceContent>
              </Inplace>
            )}
          ></Column>
          <Column
            header="Size"
            field="size"
            sortable
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            field="category"
            header="Category"
            sortable
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            field="content_rating"
            header="Content Rating"
            sortable
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            field="date_created"
            header="Date Uploaded"
            sortable
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
        </DataTable>
      </div>
      <div className="edit-profile-card">
        <div className="profile-pic">
          <Avatar src={profilePic} name={name} size="150" round={true} />
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <button type="submit">Save</button>
        </form>
      </div>
    </div>
  );
};
export default UserProfile;

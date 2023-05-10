import "../Admin/index.css";
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";

import { Dropdown } from "primereact/dropdown";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Inplace, InplaceDisplay, InplaceContent } from "primereact/inplace";

const UserProfile = () => {
  const [history, setHistory] = useState([]);

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

          {/* <Column
            header="Files nb."
            style={{ width: "20%" }}
            sortable
            body={(rowData) => rowData.files.length}
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            header="Files"
            style={{ width: "20%" }}
            body={(rowData) => <FilesColumn rowData={rowData} />}
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          /> */}
        </DataTable>
      </div>
    </div>
  );
};
export default UserProfile;

function FilesColumn(props) {
  const [selectedFile, setSelectedFile] = useState(null);

  const fileOptions = props.rowData.files.map((file) => ({
    label: file.name,
    value: file.id,
  }));

  return (
    <div>
      <Dropdown
        options={fileOptions}
        value={selectedFile}
        onChange={(e) => setSelectedFile(e.value)}
        placeholder="View files"
      />
    </div>
  );
}

import "../Admin/index.css";
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";

import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";

const DisplayUsers = () => {
  const [files, setFiles] = useState([]);
  const apiUrl = process.env.API_URL;
  useEffect(() => {
    const getFiles = async () => {
      try {
        const response = await axios.get(apiUrl + "user/get_files", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        console.log(response.data.files);
        setFiles(response.data.files);
      } catch (e) {
        console.log(e);
      }
    };
    getFiles();
  }, []);

  return (
    <div className="display-users">
      <h1>Display Users</h1>
      <div className="card">
        <DataTable
          value={files}
          scrollable
          scrollHeight="400px"
          virtualScrollerOptions={{ itemSize: 46 }}
          tableStyle={{ minWidth: "50rem" }}
        >
          <Column field="id" header="Id" style={{ width: "20%" }}></Column>
          <Column field="vin" header="Vin" style={{ width: "20%" }}></Column>
          <Column field="year" header="Year" style={{ width: "20%" }}></Column>
          <Column
            field="brand"
            header="Brand"
            style={{ width: "20%" }}
          ></Column>
          <Column
            field="color"
            header="Color"
            style={{ width: "20%" }}
          ></Column>
        </DataTable>
      </div>
    </div>
  );
};
export default DisplayUsers;

import "../Admin/index.css";
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";

import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Button } from "primereact/button";

const DisplayFiles = () => {
  const [files, setFiles] = useState([]);
  const apiUrl = process.env.API_URL;
  useEffect(() => {
    const getUsers = async () => {
      try {
        const response = await axios.get(apiUrl + "admin/get_files", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        console.log(response);
        setFiles(response.data.files);
      } catch (e) {
        console.log(e);
      }
    };
    getUsers();
  }, []);

  const viewFile = (path) => {
    window.open(f'{apiUrl}{path}', "_blank");
  };

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
          <Column field="_id" header="Id" style={{ width: "20%" }}></Column>
          <Column
            field="name"
            header="File Name"
            style={{ width: "20%" }}
          ></Column>
          <Column
            field="by_user"
            header="File Owner"
            style={{ width: "20%" }}
          ></Column>
          <Column
            header="Enroll"
            body={(rowData) => (
              <Button
                label="View File"
                onClick={() => viewFile(rowData.path)}
              />
            )}
          />
        </DataTable>
      </div>
    </div>
  );
};
export default DisplayFiles;

import "../Admin/index.css";
import React from "react";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Button } from "primereact/button";
import { SlideMenu } from "primereact/slidemenu";

const DisplayFiles = ({ onAdminNameChange }) => {
  const [files, setFiles] = useState([]);
  const menu = useRef(null);
  const apiUrl = process.env.API_URL;
  const navigate = useNavigate();

  useEffect(() => {
    const getUsers = async () => {
      try {
        const response = await axios.get(apiUrl + "admin/get_files", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        // console.log(response.data.files);

        setFiles(response.data.files);
        // console.log(response.data.files[1].content);
        localStorage.setItem("admin_name", response.data.admin_name);
      } catch (e) {
        if (e.response.data.detail.access === "denied") {
          navigate("/");
        }
      }
    };
    getUsers();
  }, []);

  function adjustDataForSlideMenu(files) {
    const menuItems = [];

    // Loop through each file object in the array
    for (let file of files) {
      // Create a new menu item object
      console.log(file.name);
      const menuItem = {
        label: file.name,
        icon: file.type === "folder" ? "pi pi-folder" : "pi pi-file",
      };

      // If the file is a folder, recursively add its contents as subitems
      if (file.type === "folder") {
        menuItem.items = adjustDataForSlideMenu(file.items);
      } else if (file.type === "file") {
        // Otherwise, set the onclick function to open the file
        menuItem.command = () => window.open(`${apiUrl}${file.path}`);
      }

      // Add the new menu item to the array of menu items
      menuItems.push(menuItem);
    }

    return menuItems;
  }

  const viewFile = (path) => {
    window.open(`${apiUrl}${path}`);
  };

  const hello = adjustDataForSlideMenu(files);
  console.log(hello);
  return (
    <div className="display-users">
      <h1>Files</h1>
      <div className="card" style={{ padding: "0rem" }}>
        <DataTable
          value={files}
          scrollable
          scrollHeight="400px"
          virtualScrollerOptions={{ itemSize: 46 }}
          tableStyle={{
            minWidth: "50rem",
          }}
        >
          <Column
            field="_id"
            header="Id"
            style={{ width: "20%" }}
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            field="name"
            header="File Name"
            style={{ width: "20%" }}
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            field="by_user"
            header="File Owner"
            style={{ width: "20%" }}
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          ></Column>
          <Column
            header="View File"
            // body={(rowData) => (
            //   <Button
            //     label="View File"
            //     onClick={() => viewFile(rowData.path)}
            //   />
            // )}
            body={(rowData) => (
              <>
                {/* {console.log("rowData:", rowData.content)} */}
                <SlideMenu
                  ref={menu}
                  model={hello}
                  popup
                  viewportHeight={220}
                  menuWidth={175}
                ></SlideMenu>
                <Button
                  type="button"
                  icon="pi pi-bars"
                  label="Show"
                  onClick={(event) => menu.current.toggle(event)}
                ></Button>
              </>
            )}
            headerStyle={{ backgroundColor: "#714DF4", color: "white" }}
          />
        </DataTable>
      </div>
    </div>
  );
};
export default DisplayFiles;

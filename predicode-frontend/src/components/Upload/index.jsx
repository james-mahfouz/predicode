import React, { useState, useEffect } from "react";
import axios from "axios";
import JSZip from "jszip";
import Navbar from "../Navbar";

import { useNavigate } from "react-router-dom";
import { FileUpload } from "primereact/fileupload";
import { Message } from "primereact/message";
import { Dropdown } from "primereact/dropdown";
import { InputNumber } from "primereact/inputnumber";

const optionsCategory = [
  { name: "ART_AND_DESIGN", code: "ART_AND_DESIGN" },
  { name: "AUTO_AND_VEHICLES", code: "AUTO_AND_VEHICLES" },
  { name: "BEAUTY", code: "BEAUTY" },
  { name: "BOOKS_AND_REFERENCE", code: "BOOKS_AND_REFERENCE" },
  { name: "BUSINESS", code: "BUSINESS" },
  { name: "COMICS", code: "COMICS" },
  { name: "COMMUNICATION", code: "COMMUNICATION" },
  { name: "DATING", code: "DATING" },
  { name: "EDUCATION", code: "EDUCATION" },
  { name: "ENTERTAINMENT", code: "ENTERTAINMENT" },
  { name: "EVENTS", code: "EVENTS" },
  { name: "FAMILY", code: "FAMILY" },
  { name: "FINANCE", code: "FINANCE" },
  { name: "FOOD_AND_DRINK", code: "FOOD_AND_DRINK" },
  { name: "GAME", code: "GAME" },
  { name: "HEALTH_AND_FITNESS", code: "HEALTH_AND_FITNESS" },
  { name: "HOUSE_AND_HOME", code: "HOUSE_AND_HOME" },
  { name: "LIBRARIES_AND_DEMO", code: "LIBRARIES_AND_DEMO" },
  { name: "LIFESTYLE", code: "LIFESTYLE" },
  { name: "MAPS_AND_NAVIGATION", code: "MAPS_AND_NAVIGATION" },
  { name: "MEDICAL", code: "MEDICAL" },
  { name: "NEWS_AND_MAGAZINES", code: "NEWS_AND_MAGAZINES" },
  { name: "PARENTING", code: "PARENTING" },
  { name: "PERSONALIZATION", code: "PERSONALIZATION" },
  { name: "PHOTOGRAPHY", code: "PHOTOGRAPHY" },
  { name: "PRODUCTIVITY", code: "PRODUCTIVITY" },
  { name: "SHOPPING", code: "SHOPPING" },
  { name: "SOCIAL", code: "SOCIAL" },
  { name: "SPORTS", code: "SPORTS" },
  { name: "TOOLS", code: "TOOLS" },
  { name: "TRAVEL_AND_LOCAL", code: "TRAVEL_AND_LOCAL" },
  { name: "VIDEO_PLAYERS", code: "VIDEO_PLAYERS" },
  { name: "WEATHER", code: "WEATHER" },
];

const optionsContentRating = [
  { name: "Adults only 18+", code: "Adults only 18+" },
  { name: "Everyone", code: "Everyone" },
  { name: "Everyone 10+", code: "Everyone 10+" },
  { name: "Mature 17+", code: "Mature 17+" },
  { name: "Teen", code: "Teen" },
];

const Upload = () => {
  const [signedIn, setSignedIn] = useState(false);
  const [price, setPrice] = useState(0);
  const [error, setError] = useState("");
  const [category, setCategory] = useState(null);
  const [content, setContent] = useState(null);

  const apiUrl = process.env.API_URL;
  const navigate = useNavigate();

  useEffect(() => {
    const verify = async () => {
      try {
        const response = await axios.get(apiUrl + "user/verify", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setSignedIn(true);
      } catch (e) {
        console.log(e);
        navigate("/login");
      }
    };
    verify();
  }, []);

  const onUpload = (event) => {
    if (!signedIn) {
      navigate("/login");
      return;
    }

    if (!price) {
      setError("Please enter your app price");
      return;
    }

    const uploaded_file = event.files[0];
    if (uploaded_file.type === "application/zip") {
      const reader = new FileReader();
      reader.readAsDataURL(uploaded_file);
      reader.onload = () => {
        const encodedData = reader.result.split(",");

        const data = {
          data: encodedData[1],
          content_type: encodedData[0],
          price: price,
          category: category.name,
          content_rating: content.name,
          name: event.files[0].name,
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
          .catch((error) => {
            console.log(error);
          });
      };
    } else {
      console.log("File not zipped");
      setError("File should be zipped");
    }
  };

  const handleLogout = () => {
    setSignedIn(false);
    navigate("/");
  };
  return (
    <div>
      <Navbar onLogout={handleLogout} />
      <section
        className="upload-wrapper"
        style={{ paddingTop: error ? "50px" : "0px" }}
      >
        <div className="landing-wrapper">
          <h3>↓ Upload your ZIPPED Folder here ↓</h3>
          <FileUpload
            name="demo[]"
            customUpload={true}
            uploadHandler={onUpload}
            accept=".zip, .folder, application/zip, application/x-zip-compressed, multipart/x-zip"
            webkitdirectory="true"
            maxFileSize={100000000000000}
            emptyTemplate={
              <p className="m-0">
                Upload your zipped code folder and see your rating
              </p>
            }
          />
          <div className="form">
            {error && (
              <Message
                severity="error"
                text={error}
                style={{ width: "100%", marginBottom: "10px" }}
              />
            )}

            <div className="inputfield">
              <label>Category: </label>
              <Dropdown
                value={category}
                onChange={(e) => setCategory(e.value)}
                options={optionsCategory}
                optionLabel="name"
                placeholder="App Category"
                className="w-full md:w-14rem"
              />
            </div>

            <div className="inputfield">
              <label>Content Rating: </label>
              <Dropdown
                value={content}
                onChange={(e) => setContent(e.value)}
                options={optionsContentRating}
                optionLabel="name"
                placeholder="App Content Rating"
                className="w-full md:w-14rem"
              />
            </div>

            <div className="inputfield">
              <label>Price $: </label>
              <InputNumber
                id="number-input"
                value={price}
                onValueChange={(e) => setPrice(e.value)}
                className="w-full md:w-14rem"
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
export default Upload;

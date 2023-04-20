import React, { useState } from "react";
import { Dropdown } from "primereact/dropdown";

const FilesColumn = (props) => {
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
        placeholder="View all files"
      />
    </div>
  );
};

export default FilesColumn;

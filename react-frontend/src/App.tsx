import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { FileUpload } from 'primereact/fileupload';

import 'primereact/resources/themes/lara-light-indigo/theme.css'; //theme
import 'primereact/resources/primereact.min.css'; //core css
import 'primeicons/primeicons.css'; //icons
import 'primeflex/primeflex.css'; // flex

function App() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [profilePicture, setProfilePicture] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(name, email, phone)
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="p-field">
        <label htmlFor="name">Name</label>
        <InputText id="name" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div className="p-field">
        <label htmlFor="email">Email</label>
        <InputText id="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div className="p-field">
        <label htmlFor="phone">Phone</label>
        <InputText id="phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
      </div>
      <div className="p-field">
        <label htmlFor="profilePicture">Profile Picture</label>
        <FileUpload
          id="profilePicture"
          name="profilePicture"
          accept="image/*"
          maxFileSize={1000000}
          chooseLabel="Choose"
          uploadLabel="Upload"
          cancelLabel="Cancel"
          mode="basic"
          onUpload={(event) => setProfilePicture(event.files[0])}
        />
      </div>
      <Button label="Save" type="submit" />
    </form>
  )
}

export default App

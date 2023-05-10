import '../Admin/index.css'
import React from 'react'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

import { Dropdown } from 'primereact/dropdown'
import { DataTable } from 'primereact/datatable'
import { Column } from 'primereact/column'

const DisplayUsers = () => {
  const [users, setUsers] = useState([])
  const navigate = useNavigate()

  const apiUrl = window.API_URL
  useEffect(() => {
    const getUsers = async () => {
      try {
        const response = await axios.get(apiUrl + 'admin/get_users', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        })
        setUsers(response.data.users)
        localStorage.setItem('admin_name', response.data.admin_name)
      } catch (e) {
        if (e.response.data.detail.access === 'denied') {
          navigate('/')
        }
      }
    }
    getUsers()
  }, [])

  return (
    <div className="display-users">
      <h1>Users</h1>
      <div className="card" style={{ padding: '0rem' }}>
        <DataTable
          value={users}
          scrollable
          scrollHeight="400px"
          virtualScrollerOptions={{ itemSize: 46 }}
          tableStyle={{ minWidth: '50rem' }}
          sortMode="multiple"
        >
          <Column
            field="_id"
            header="Id"
            style={{ width: '20%' }}
            sortable
            headerStyle={{ backgroundColor: '#714DF4', color: 'white' }}
          ></Column>
          <Column
            field="name"
            header="Name"
            style={{ width: '20%' }}
            sortable
            headerStyle={{ backgroundColor: '#714DF4', color: 'white' }}
          ></Column>
          <Column
            field="email"
            header="email"
            sortable
            style={{ width: '20%' }}
            headerStyle={{ backgroundColor: '#714DF4', color: 'white' }}
          ></Column>
          <Column
            header="Files nb."
            style={{ width: '20%' }}
            sortable
            body={(rowData) => rowData.files.length}
            headerStyle={{ backgroundColor: '#714DF4', color: 'white' }}
          ></Column>
          <Column
            header="Files"
            style={{ width: '20%' }}
            body={(rowData) => <FilesColumn rowData={rowData} />}
            headerStyle={{ backgroundColor: '#714DF4', color: 'white' }}
          />
        </DataTable>
      </div>
    </div>
  )
}
export default DisplayUsers

function FilesColumn(props) {
  const [selectedFile, setSelectedFile] = useState(null)

  const fileOptions = props.rowData.files.map((file) => ({
    label: file.name,
    value: file.id
  }))

  return (
    <div>
      <Dropdown
        options={fileOptions}
        value={selectedFile}
        onChange={(e) => setSelectedFile(e.value)}
        placeholder="View files"
      />
    </div>
  )
}

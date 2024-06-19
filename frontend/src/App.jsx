import { useState, useEffect } from 'react'
import './App.css'
import ContactList from './ContactList'
import ContactForm from './ContactForm'

function App() {
  const [contacts, setContacts] = useState([])
  //modal initially closed (false), opens when true
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    fetchContacts()
  }, [])

  const fetchContacts = async () => {
    const response = await fetch("http://127.0.0.1:5000/contacts")
    const data = await response.json()
    setContacts(data.contacts)
    console.log(data.contacts)
  }

  const closeModal = () => {
    setIsModalOpen(false)
  }

  const openCreateModal = () => {
    if(!isModalOpen){
      setIsModalOpen(true)
    }
  }

  return (
    <>
      <ContactList contacts={contacts} />
      <button onClick={openCreateModal}>Create Contact</button>
      {
        isModalOpen && (
          <div className="modal">
            <div className="modal-content">
              <span className="close" onClick={closeModal}>&times;</span>
              <ContactForm fetchContacts={fetchContacts} />
            </div>
          </div>
        )
      }
    </>
  )
}

export default App

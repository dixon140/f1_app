import React, { useEffect, useState } from 'react'

import UserCard from './UserCard'

function UserList() {

  const [users, setUsers] = useState([])

  useEffect(() => {
    async function getUsers() {
      const response = await fetch('/api/users')
      if (response.ok) {
        const ingredientsData = await response.json()
        setIngredientList(ingredientsData)
      } else {
        const e = await response.json()
        setError(e.message)
      }
    }
    getIngredients()
  }, [])

  const mappedUsers = users.map(user => <UserCard key={user.id} user={user} />)

  return (
    <div>
      <h2>User List</h2>
      <ul>
        
      </ul>
    </div>
  )
}
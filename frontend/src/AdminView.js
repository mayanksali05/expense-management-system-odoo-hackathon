import React, { useState } from "react";
import "./adminView.css";

const AdminView = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("employee");

  const handleSendPassword = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/api/auth/admin/create-user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name, email, role })
      });

      const result = await response.json();
      if (response.ok) {
        alert("User created successfully! Password sent via email.");
        setName(""); setEmail(""); setRole("employee");
      } else {
        alert(result.msg || "Failed to create user");
      }
    } catch (err) {
      console.error(err);
      alert("Error creating user");
    }
  };

  return (
    <div className="admin-container">
      <h2>Admin: Create New User</h2>
      <form onSubmit={handleSendPassword}>
        <input 
          placeholder="Name" 
          value={name} 
          onChange={e => setName(e.target.value)} 
          required 
        />
        <input 
          placeholder="Email" 
          type="email"
          value={email} 
          onChange={e => setEmail(e.target.value)} 
          required 
        />
        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="employee">Employee</option>
          <option value="manager">Manager</option>
          <option value="admin">Admin</option>
        </select>
        <button type="submit">Send Password</button>
      </form>
    </div>
  );
};

export default AdminView;

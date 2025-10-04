import React from "react";
import { useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear token, role, and user info from localStorage
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("name");

    // Redirect to login page
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="nav-logo">Expense Tracker</div>
      <ul className="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/expenses">Expenses</a></li>
        <li><a href="/reports">Reports</a></li>
        <li><a href="/profile">Profile</a></li>
      </ul>
      <button className="nav-login-btn" onClick={handleLogout}>
        Logout
      </button>
    </nav>
  );
};

export default Navbar;

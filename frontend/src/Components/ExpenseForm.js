import React, { useState } from 'react';
import './expenseForm.css';

function ExpenseForm() {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState('');
  const [currency, setCurrency] = useState('INR');
  const [notes, setNotes] = useState('');
  const [receipt, setReceipt] = useState(null); // file input

  const submitHandler = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("title", title);
    formData.append("category", category);
    formData.append("amount", amount);
    formData.append("currency", currency);
    formData.append("notes", notes);
    if (receipt) formData.append("receipt", receipt);

    try {
      const token = localStorage.getItem("token"); // JWT token
      const response = await fetch("http://localhost:5000/api/expenses/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData
      });

      const result = await response.json();
      if (response.ok) {
        alert(`Expense added! ID: ${result.expense_id}`);
        setTitle('');
        setCategory('');
        setAmount('');
        setCurrency('INR');
        setNotes('');
        setReceipt(null);
      } else {
        alert(result.msg || "Failed to add expense");
      }
    } catch (err) {
      console.error(err);
      alert("Error adding expense");
    }
  };

  return (
    <form className="expense-form" onSubmit={submitHandler}>
      <h3>Submit Expense</h3>
      <input 
        placeholder="Title" 
        value={title} 
        onChange={e => setTitle(e.target.value)} 
        required 
      />
      <input 
        placeholder="Category" 
        value={category} 
        onChange={e => setCategory(e.target.value)} 
      />
      <input 
        placeholder="Amount" 
        type="number" 
        value={amount} 
        onChange={e => setAmount(e.target.value)} 
        required 
      />
      <input 
        placeholder="Currency" 
        value={currency} 
        onChange={e => setCurrency(e.target.value)} 
      />
      <textarea 
        placeholder="Notes" 
        value={notes} 
        onChange={e => setNotes(e.target.value)} 
      />
      <input 
        type="file" 
        onChange={e => setReceipt(e.target.files[0])} 
      />
      <button type="submit">Submit</button>
    </form>
  );
}

export default ExpenseForm;

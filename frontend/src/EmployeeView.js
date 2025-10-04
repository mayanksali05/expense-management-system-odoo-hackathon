import React from 'react';
import ExpenseForm from './Components/ExpenseForm';

const EmployeeView = () => {
  return (
    <div>
      <h1>Employee Dashboard</h1>
      <ExpenseForm />
      {/* Add list of submitted expenses here */}
    </div>
  );
};

export default EmployeeView;

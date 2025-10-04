import React, { useState, useEffect } from 'react';
import ApprovalsTable from './Components/ApprovalsTable';

const ManagerView = () => {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    // Fetch approvals requests from backend API and update state
    // fetch('/api/approvals').then(...).then(data => setRequests(data));
  }, []);

  const handleApprove = (req) => {
    // Call API to approve expense request
  };

  const handleReject = (req) => {
    // Call API to reject expense request
  };

  return (
    <div>
      <h1>Manager Dashboard</h1>
      <ApprovalsTable requests={requests} onApprove={handleApprove} onReject={handleReject} />
    </div>
  );
};

export default ManagerView;

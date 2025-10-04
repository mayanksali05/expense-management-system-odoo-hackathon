import React from 'react';

function ApprovalsTable({ requests = [], onApprove, onReject }) {
  return (
    <div>
      <h3>Approvals to Review</h3>
      <table>
        <thead>
          <tr>
            <th>Employee</th>
            <th>Description</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((req, i) => (
            <tr key={i}>
              <td>{req.employee}</td>
              <td>{req.description}</td>
              <td>{req.category}</td>
              <td>{req.amount}</td>
              <td>{req.status}</td>
              <td>
                {req.status === 'Pending' ? (
                  <>
                    <button onClick={() => onApprove(req)}>Approve</button>
                    <button onClick={() => onReject(req)}>Reject</button>
                  </>
                ) : (
                  req.status
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default ApprovalsTable;

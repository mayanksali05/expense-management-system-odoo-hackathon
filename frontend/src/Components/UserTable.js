import React from 'react';

function UserTable({ users = [] }) {
  return (
    <div>
      <h3>All Users</h3>
      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Role</th>
            <th>Manager</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, i) => (
            <tr key={i}>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td>{user.manager || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default UserTable;

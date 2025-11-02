document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('collegeForm');
  const tbody = document.getElementById('colleges-table-body');
  const searchInput = document.getElementById('college-search');
  let colleges = [];
  let editIndex = null;

  function renderTable(list = colleges) {
    tbody.innerHTML = '';
    if (list.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted">No colleges found.</td></tr>`;
      return;
    }
    list.forEach((c, i) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${c.code}</td>
        <td>${c.name}</td>
        <td>
          <button class="btn btn-sm btn-outline-primary me-1" data-index="${i}" data-action="edit">Edit</button>
          <button class="btn btn-sm btn-outline-danger" data-index="${i}" data-action="delete">Delete</button>
        </td>`;
      tbody.appendChild(tr);
    });
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    if (editIndex === null) {
      colleges.push(data);
    } else {
      colleges[editIndex] = data;
      editIndex = null;
    }
    form.reset();
    renderTable();
    bootstrap.Modal.getInstance(document.querySelector('#collegeModal')).hide();
  });

  tbody.addEventListener('click', function(e) {
    const btn = e.target.closest('button');
    if (!btn) return;
    const index = btn.dataset.index;
    const action = btn.dataset.action;

    if (action === 'delete') {
      if (confirm(`Delete college ${colleges[index].name}?`)) {
        colleges.splice(index, 1);
        renderTable();
      }
    } else if (action === 'edit') {
      const college = colleges[index];
      for (const key in college) {
        if (form.elements[key]) form.elements[key].value = college[key];
      }
      editIndex = index;
      new bootstrap.Modal(document.querySelector('#collegeModal')).show();
    }
  });

  searchInput.addEventListener('input', function() {
    const q = this.value.toLowerCase();
    const filtered = colleges.filter(c =>
      c.name.toLowerCase().includes(q) ||
      c.code.toLowerCase().includes(q)
    );
    renderTable(filtered);
  });

  // Initial sample data
  colleges = [
    { code: 'CCS', name: 'College of Computer Studies' },
    { code: 'COE', name: 'College of Engineering' },
    { code: 'CBAA', name: 'College of Business Administration and Accountancy' },
    { code: 'CAS', name: 'College of Arts and Sciences' }
  ];

  renderTable();
});

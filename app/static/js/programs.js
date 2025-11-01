document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('programForm');
  const tbody = document.getElementById('programs-table-body');
  const searchInput = document.getElementById('program-search');
  let programs = [];
  let editIndex = null;

  function renderTable(list = programs) {
    tbody.innerHTML = '';
    if (list.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4" class="text-center text-muted">No programs found.</td></tr>`;
      return;
    }
    list.forEach((p, i) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${p.code}</td>
        <td>${p.name}</td>
        <td>${p.college}</td>
        <td>
          <button class="btn btn-sm btn-outline-primary me-1" data-index="${i}" data-action="edit">Edit</button>
          <button class="btn btn-sm btn-outline-danger" data-index="${i}" data-action="delete">Delete</button>
        </td>`;
      tbody.appendChild(tr);
    });
  }

  function resetForm() {
    form.reset();
    editIndex = null;
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    if (editIndex === null) {
      programs.push(data);
    } else {
      programs[editIndex] = data;
      editIndex = null;
    }
    renderTable();
    bootstrap.Modal.getInstance(document.querySelector('#programModal')).hide();
    form.reset();
  });

  tbody.addEventListener('click', function(e) {
    const btn = e.target.closest('button');
    if (!btn) return;
    const index = btn.dataset.index;
    const action = btn.dataset.action;
    if (action === 'delete') {
      if (confirm(`Delete program ${programs[index].name}?`)) {
        programs.splice(index, 1);
        renderTable();
      }
    } else if (action === 'edit') {
      const program = programs[index];
      for (const key in program) {
        if (form.elements[key]) form.elements[key].value = program[key];
      }
      editIndex = index;
      new bootstrap.Modal(document.querySelector('#programModal')).show();
    }
  });

  searchInput.addEventListener('input', function() {
    const q = this.value.toLowerCase();
    const filtered = programs.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.code.toLowerCase().includes(q) ||
      p.college.toLowerCase().includes(q)
    );
    renderTable(filtered);
  });

  // Initial data (you can remove this later)
  programs = [
    { code: 'BSCS', name: 'Bachelor of Science in Computer Science', college: 'CCS' },
    { code: 'BSEE', name: 'Bachelor of Science in Electrical Engineering', college: 'COE' },
    { code: 'BSIT', name: 'Bachelor of Science in Information Technology', college: 'CCS' }
  ];

  renderTable();
});


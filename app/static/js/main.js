// app/static/js/main.js
(() => {
  const DATA_URL = '/static/data/students.json'; // relative to app static root
  let students = [];           // in-memory dataset
  let currentEditId = null;    // null => new, else edit
  const pageSize = 8;
  let currentPage = 1;
  let filtered = [];

  // DOM refs
  const tbody = document.querySelector('#students-table-body');
  const form = document.getElementById('studentForm');
  const modalEl = document.getElementById('studentModal');
  const searchInput = document.getElementById('student-search');
  const paginationEl = document.querySelector('.pagination');

  // Bootstrap modal helper
  let bsModal = null;
  if (modalEl) bsModal = new bootstrap.Modal(modalEl);

  async function loadData() {
    try {
      const res = await fetch(DATA_URL);
      students = await res.json();
      filtered = students.slice();
      renderTable();
      renderPagination();
    } catch (err) {
      console.error('Failed to fetch students.json', err);
      // fallback: empty array
      students = [];
      filtered = [];
      renderTable();
      renderPagination();
    }
  }

  function renderTable() {
    if (!tbody) return;
    tbody.innerHTML = '';

    const start = (currentPage - 1) * pageSize;
    const pageItems = filtered.slice(start, start + pageSize);

    if (pageItems.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-center small text-muted">No students found</td></tr>`;
      return;
    }

    for (const s of pageItems) {
      const tr = document.createElement('tr');

      tr.innerHTML = `
        <td><a href="#" class="student-roll-link" data-id="${s.id}">${escapeHtml(s.roll)}</a></td>
        <td>${escapeHtml(s.name)}</td>
        <td>${escapeHtml(s.semester)}</td>
        <td>${escapeHtml(s.department)}</td>
        <td>
          <button class="btn btn-sm btn-outline-primary btn-edit" data-id="${s.id}">Edit</button>
          <button class="btn btn-sm btn-outline-danger btn-delete" data-id="${s.id}">Delete</button>
        </td>
      `;
      tbody.appendChild(tr);
    }

    // wire buttons
    tbody.querySelectorAll('.btn-edit').forEach(btn => btn.addEventListener('click', onEdit));
    tbody.querySelectorAll('.btn-delete').forEach(btn => btn.addEventListener('click', onDelete));
  }

  function renderPagination() {
    if (!paginationEl) return;
    paginationEl.innerHTML = '';

    const pages = Math.max(1, Math.ceil(filtered.length / pageSize));
    const createPageItem = (label, pg, disabled=false, active=false) => {
      const li = document.createElement('li');
      li.className = 'page-item' + (disabled ? ' disabled' : '') + (active ? ' active' : '');
      const a = document.createElement('a');
      a.className = 'page-link';
      a.href = '#';
      a.dataset.page = pg;
      a.textContent = label;
      a.addEventListener('click', (e) => {
        e.preventDefault();
        if (!disabled) {
          currentPage = pg;
          renderTable();
          renderPagination();
          window.scrollTo({top: 0, behavior: 'smooth'});
        }
      });
      li.appendChild(a);
      return li;
    };

    // prev
    const prev = createPageItem('<', Math.max(1, currentPage - 1), currentPage === 1);
    paginationEl.appendChild(prev);

    for (let i = 1; i <= pages; i++) {
      const li = createPageItem(String(i), i, false, i === currentPage);
      paginationEl.appendChild(li);
    }

    // next
    const next = createPageItem('>', Math.min(pages, currentPage + 1), currentPage === pages);
    paginationEl.appendChild(next);
  }

  // Edit handler
  function onEdit(e) {
    const id = Number(e.currentTarget.dataset.id);
    const student = students.find(s => s.id === id);
    if (!student) return;
    currentEditId = id;
    // fill form
    form.reset();
    setFormValue('roll', student.roll || '');
    setFormValue('name', student.name || '');
    setFormValue('email', student.email || '');
    setFormValue('sex', student.sex || '');
    setFormValue('semester', student.semester || '');
    setFormValue('department', student.department || '');
    setFormValue('address', student.address || '');
    if (bsModal) bsModal.show();
  }

  // Delete handler
  function onDelete(e) {
    const id = Number(e.currentTarget.dataset.id);
    const student = students.find(s => s.id === id);
    if (!student) return;
    if (!confirm(`Delete ${student.name} (${student.roll})? This is frontend-only.`)) return;
    // delete in-memory
    students = students.filter(s => s.id !== id);
    filtered = filtered.filter(s => s.id !== id);
    // adjust page if necessary
    const maxPage = Math.max(1, Math.ceil(filtered.length / pageSize));
    if (currentPage > maxPage) currentPage = maxPage;
    renderTable();
    renderPagination();
  }

  // Form helpers
  function setFormValue(name, value) {
    const el = form.elements[name];
    if (!el) return;
    el.value = value;
  }
 
  // Form submit (Add or Edit)
  if (form) {
    form.addEventListener('submit', (ev) => {
      ev.preventDefault();
      const data = new FormData(form);
      const payload = Object.fromEntries(data.entries());

      // Basic validation
      if (!payload.roll || !payload.name) {
        alert('Please enter all details such as ID Number and Name...');
        return;
      }

      if (currentEditId == null) {
        // add new
        const newId = (students.length ? Math.max(...students.map(s => s.id)) : 0) + 1;
        const newStudent = {
          id: newId,
          roll: payload.roll,
          name: payload.name,
          semester: payload.semester || '',
          department: payload.department || '',
          email: payload.email || '',
          sex: payload.sex || '',
          address: payload.address || ''
        };
        students.unshift(newStudent);    // add to top
      } else {
        // update existing
        const idx = students.findIndex(s => s.id === currentEditId);
        if (idx !== -1) {
          students[idx] = {
            ...students[idx],
            roll: payload.roll,
            name: payload.name,
            semester: payload.semester || '',
            department: payload.department || '',
            email: payload.email || '',
            sex: payload.sex || '',
            address: payload.address || ''
          };
        }
        currentEditId = null;
      }

      // reset and close modal
      form.reset();
      if (bsModal) bsModal.hide();
      // refresh filtered & UI
      applySearch();
      renderPagination();
    });
  }

  // Search
  function applySearch() {
    const q = searchInput ? (searchInput.value || '').toLowerCase().trim() : '';
    if (!q) {
      filtered = students.slice();
    } else {
      filtered = students.filter(s =>
        (s.name && s.name.toLowerCase().includes(q)) ||
        (s.roll && s.roll.toLowerCase().includes(q)) ||
        (s.department && s.department.toLowerCase().includes(q))
      );
    }
    currentPage = 1;
    renderTable();
    renderPagination();
  }

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      applySearch();
    });
  }

  // escape html (basic)
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
  }

  // init on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    loadData();
  });

})();

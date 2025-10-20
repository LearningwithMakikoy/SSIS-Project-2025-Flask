// placeholder: handle student form submit in frontend-only mode
document.addEventListener('DOMContentLoaded', function(){
  const form = document.getElementById('studentForm');
  if (!form) return;
  form.addEventListener('submit', function(e){
    e.preventDefault();
    // read inputs and show sample success toast
    const data = new FormData(form);
    console.log('Student data (frontend only):', Object.fromEntries(data.entries()));
    // close modal
    const modalEl = document.querySelector('#studentModal');
    if (modalEl) {
      const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
      modal.hide();
    }
    alert('Saved (frontend demo only). Hookup to backend to persist.');
  });
});

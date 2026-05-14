// ── Sidebar Toggle ──────────────────────────────────────
const sidebar        = document.getElementById('sidebar');
const mainWrapper    = document.getElementById('mainWrapper');
const sidebarToggle  = document.getElementById('sidebarToggle');
const mobileMenuBtn  = document.getElementById('mobileMenuBtn');

if (sidebarToggle) {
  sidebarToggle.addEventListener('click', function () {
    if (window.innerWidth > 1024) {
      sidebar.classList.toggle('collapsed');
      if (sidebar.classList.contains('collapsed')) {
        mainWrapper.style.marginLeft = 'var(--sidebar-collapsed)';
      } else {
        mainWrapper.style.marginLeft = 'var(--sidebar-width)';
      }
    } else {
      sidebar.classList.toggle('open');
    }
  });
}

if (mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', function () {
    sidebar.classList.toggle('open');
  });
}

// Close sidebar on outside click (mobile)
document.addEventListener('click', function (e) {
  if (window.innerWidth <= 1024 && sidebar && sidebar.classList.contains('open')) {
    if (!sidebar.contains(e.target) && e.target !== mobileMenuBtn) {
      sidebar.classList.remove('open');
    }
  }
});

// ── Delete Modal ─────────────────────────────────────────
function confirmDelete(actionUrl, itemName) {
  const modal   = document.getElementById('deleteModal');
  const form    = document.getElementById('deleteForm');
  const message = document.getElementById('modalMessage');

  if (!modal || !form) return;

  form.action = actionUrl;
  message.textContent = `Are you sure you want to delete "${itemName}"? This action cannot be undone.`;
  modal.classList.add('active');

  // Trap focus inside modal
  modal.querySelector('.btn-secondary').focus();
}

function closeDeleteModal() {
  const modal = document.getElementById('deleteModal');
  if (modal) modal.classList.remove('active');
}

// Close modal on overlay click
document.addEventListener('click', function (e) {
  const modal = document.getElementById('deleteModal');
  if (modal && e.target === modal) closeDeleteModal();
});

// Close modal on Escape key
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closeDeleteModal();
});

// ── Auto-dismiss Messages ─────────────────────────────────
(function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-6px)';
      setTimeout(function () { alert.remove(); }, 400);
    }, 4000);
  });
})();

// ── Animate stat counters ─────────────────────────────────
function animateCounter(el, target, duration) {
  let start = 0;
  const step = Math.ceil(target / (duration / 16));
  const timer = setInterval(function () {
    start += step;
    if (start >= target) { start = target; clearInterval(timer); }
    el.textContent = start;
  }, 16);
}

(function () {
  const counters = document.querySelectorAll('.stat-value');
  counters.forEach(function (el) {
    const val = parseInt(el.textContent, 10);
    if (!isNaN(val) && val > 0) {
      el.textContent = '0';
      animateCounter(el, val, 700);
    }
  });
})();

/**
 * ShopEase - Core Interactive Frontend JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  initToasts();
  initUserDropdown();
  initMobileNav();
  initQuantitySteppers();
  initAjaxAddToCart();
  initSimulatedCardPreview();
});

/* ==========================================================================
   Toast Notification Helper
   ========================================================================== */
function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  let iconHtml = '✓';
  if (type === 'error' || type === 'danger') iconHtml = '✕';
  if (type === 'warning') iconHtml = '⚠';
  if (type === 'info') iconHtml = 'ℹ';

  toast.innerHTML = `
    <div style="font-weight: 800; font-size: 1.1rem; line-height: 1;">${iconHtml}</div>
    <div style="flex: 1; font-size: 0.92rem; font-weight: 500;">${message}</div>
    <button style="background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #94A3B8;" onclick="this.parentElement.remove()">×</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function initToasts() {
  // Auto-dismiss Django server-rendered toasts after 5 seconds
  document.querySelectorAll('.toast').forEach(toast => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  });
}

/* ==========================================================================
   User Profile Dropdown
   ========================================================================== */
function initUserDropdown() {
  const userBtn = document.getElementById('userMenuBtn');
  const userDropdown = document.getElementById('userDropdownMenu');

  if (userBtn && userDropdown) {
    userBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle('show');
    });

    document.addEventListener('click', () => {
      userDropdown.classList.remove('show');
    });
  }
}

/* ==========================================================================
   Mobile Nav Toggle
   ========================================================================== */
function initMobileNav() {
  const toggleBtn = document.getElementById('mobileNavToggle');
  const navLinks = document.getElementById('navLinks');

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }
}

/* ==========================================================================
   Quantity Steppers (+ / -)
   ========================================================================== */
function initQuantitySteppers() {
  document.querySelectorAll('.quantity-stepper').forEach(stepper => {
    const decBtn = stepper.querySelector('.btn-decrease');
    const incBtn = stepper.querySelector('.btn-increase');
    const input = stepper.querySelector('.stepper-input');

    if (decBtn && incBtn && input) {
      decBtn.addEventListener('click', () => {
        let val = parseInt(input.value, 10) || 1;
        if (val > 1) {
          input.value = val - 1;
          input.dispatchEvent(new Event('change'));
        }
      });

      incBtn.addEventListener('click', () => {
        let val = parseInt(input.value, 10) || 1;
        let max = parseInt(input.getAttribute('max'), 10) || 99;
        if (val < max) {
          input.value = val + 1;
          input.dispatchEvent(new Event('change'));
        } else {
          showToast(`Maximum available stock is ${max}`, 'warning');
        }
      });
    }
  });
}

/* ==========================================================================
   AJAX Add to Cart
   ========================================================================== */
function initAjaxAddToCart() {
  document.querySelectorAll('.ajax-add-to-cart').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalHtml = submitBtn ? submitBtn.innerHTML : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Adding...';
      }

      const formData = new FormData(form);
      formData.append('ajax', '1');

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const data = await response.json();

        if (response.ok && data.success) {
          showToast(data.message, 'success');
          // Update cart badge in navbar
          const badges = document.querySelectorAll('.cart-badge');
          badges.forEach(badge => {
            badge.textContent = data.cart_item_count;
            badge.style.display = data.cart_item_count > 0 ? 'flex' : 'none';
          });
        } else {
          showToast(data.message || 'Error adding item to cart.', 'error');
        }
      } catch (err) {
        // Fallback to regular form submission if fetch is interrupted
        form.submit();
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalHtml;
        }
      }
    });
  });
}

/* ==========================================================================
   Simulated Credit Card Live Interactive Preview
   ========================================================================== */
function initSimulatedCardPreview() {
  const cardNumInput = document.getElementById('card_number');
  const cardNameInput = document.getElementById('card_name');
  const cardExpiryInput = document.getElementById('card_expiry');

  const cardNumDisplay = document.getElementById('cardNumPreview');
  const cardNameDisplay = document.getElementById('cardNamePreview');
  const cardExpiryDisplay = document.getElementById('cardExpiryPreview');

  if (cardNumInput && cardNumDisplay) {
    cardNumInput.addEventListener('input', (e) => {
      let val = e.target.value.replace(/\D/g, '');
      val = val.substring(0, 16);
      let formatted = val.match(/.{1,4}/g)?.join(' ') || '';
      e.target.value = formatted;
      cardNumDisplay.textContent = formatted || '•••• •••• •••• ••••';
    });
  }

  if (cardNameInput && cardNameDisplay) {
    cardNameInput.addEventListener('input', (e) => {
      cardNameDisplay.textContent = e.target.value.toUpperCase() || 'YOUR NAME';
    });
  }

  if (cardExpiryInput && cardExpiryDisplay) {
    cardExpiryInput.addEventListener('input', (e) => {
      let val = e.target.value.replace(/\D/g, '');
      if (val.length >= 2) {
        val = val.substring(0, 2) + '/' + val.substring(2, 4);
      }
      e.target.value = val.substring(0, 5);
      cardExpiryDisplay.textContent = val || 'MM/YY';
    });
  }

  // Payment radio option styling
  const radios = document.querySelectorAll('.payment-radio input, input[name="payment_method"]');
  radios.forEach(radio => {
    radio.addEventListener('change', () => {
      document.querySelectorAll('.payment-option').forEach(opt => opt.classList.remove('active'));
      const parentOption = radio.closest('.payment-option');
      if (parentOption) parentOption.classList.add('active');

      const cardFields = document.getElementById('simulatedCardFields');
      if (cardFields) {
        if (radio.value.includes('Card')) {
          cardFields.style.display = 'block';
        } else {
          cardFields.style.display = 'none';
        }
      }
    });
  });
}

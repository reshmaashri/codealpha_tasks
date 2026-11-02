/**
 * ConnectHub - Modern Social Platform JavaScript
 * Handles AJAX likes, comments, follows, image previews, modals, and micro-interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  initCsrfProtection();
  initLikeButtons();
  initCommentSystem();
  initFollowButtons();
  initImageUploadPreviews();
  initModals();
  initDropdowns();
  initShareButtons();
  initAutoDismissAlerts();
});

/* ==========================================================================
   CSRF Helper
   ========================================================================== */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function initCsrfProtection() {
  window.csrftoken = getCookie('csrftoken') || (document.querySelector('[name=csrfmiddlewaretoken]')?.value);
}

/* ==========================================================================
   Toast Notification System
   ========================================================================== */
window.showToast = function(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>
      <path d="M9 12l2 2 4-4"/>
    </svg>
    <span>${message}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(15px)';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
};

/* ==========================================================================
   AJAX Like / Unlike System
   ========================================================================== */
function initLikeButtons() {
  document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const postId = btn.dataset.postId;
      if (!postId) return;

      // Animate heart immediately for responsive feel
      const isCurrentlyLiked = btn.classList.contains('liked');
      btn.classList.toggle('liked', !isCurrentlyLiked);

      try {
        const response = await fetch(`/post/${postId}/like/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken') || window.csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
          }
        });

        if (!response.ok) {
          if (response.status === 403 || response.status === 401) {
            window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
            return;
          }
          // Revert on error
          btn.classList.toggle('liked', isCurrentlyLiked);
          showToast('Failed to update like status', 'error');
          return;
        }

        const data = await response.json();
        if (data.success) {
          btn.classList.toggle('liked', data.liked);
          const countEl = document.getElementById(`likes-count-${postId}`);
          if (countEl) {
            countEl.textContent = `${data.likes_count} ${data.likes_count === 1 ? 'like' : 'likes'}`;
          }
        }
      } catch (err) {
        console.error('Like error:', err);
        btn.classList.toggle('liked', isCurrentlyLiked);
      }
    });
  });
}

/* ==========================================================================
   AJAX Comment System
   ========================================================================== */
function initCommentSystem() {
  // Add comment
  document.querySelectorAll('.add-comment-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = form.querySelector('.comment-input');
      const text = input ? input.value.trim() : '';
      if (!text) return;

      const submitBtn = form.querySelector('.comment-submit-btn');
      if (submitBtn) submitBtn.disabled = true;

      const url = form.getAttribute('action');
      const formData = new FormData(form);

      try {
        const response = await fetch(url, {
          method: 'POST',
          body: formData,
          headers: {
            'X-CSRFToken': getCookie('csrftoken') || window.csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
          }
        });

        if (!response.ok) {
          if (response.status === 403 || response.status === 401) {
            window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
            return;
          }
          showToast('Failed to post comment', 'error');
          if (submitBtn) submitBtn.disabled = false;
          return;
        }

        const data = await response.json();
        if (data.success) {
          input.value = '';
          const commentsList = form.closest('.post-comments-container')?.querySelector('.comments-list');
          if (commentsList) {
            const commentItem = document.createElement('div');
            commentItem.className = 'comment-item';
            commentItem.id = `comment-${data.comment_id}`;
            commentItem.innerHTML = `
              <div class="comment-main">
                <img src="${data.author_avatar}" class="user-avatar-sm" alt="${data.author_username}">
                <div class="comment-content">
                  <a href="/profile/${data.author_username}/" class="comment-author">${data.author_display_name}</a>
                  <span>${escapeHtml(data.text)}</span>
                  <span class="comment-time">${data.created_at}</span>
                </div>
              </div>
              <button class="comment-delete-btn" onclick="deleteComment(${data.comment_id})" title="Delete comment">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
              </button>
            `;
            commentsList.appendChild(commentItem);
            commentItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }

          // Update comment count on post
          const countBtn = form.closest('.post-card')?.querySelector('.view-all-comments-btn');
          if (countBtn && data.comments_count) {
            countBtn.textContent = `View all ${data.comments_count} comments`;
          }

          showToast('Comment posted!', 'success');
        }
      } catch (err) {
        console.error('Comment submit error:', err);
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  });
}

window.deleteComment = async function(commentId) {
  if (!confirm('Are you sure you want to delete this comment?')) return;

  try {
    const response = await fetch(`/comment/${commentId}/delete/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken') || window.csrftoken,
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      const el = document.getElementById(`comment-${commentId}`);
      if (el) {
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 200);
      }
      showToast('Comment deleted', 'info');
    } else {
      showToast('Could not delete comment', 'error');
    }
  } catch (err) {
    console.error('Delete comment error:', err);
  }
};

/* ==========================================================================
   AJAX Follow / Unfollow System
   ========================================================================== */
function initFollowButtons() {
  document.querySelectorAll('.btn-follow').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const username = btn.dataset.username;
      if (!username) return;

      const originalText = btn.innerHTML;
      btn.disabled = true;

      try {
        const response = await fetch(`/profile/${username}/follow/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken') || window.csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
          }
        });

        if (!response.ok) {
          if (response.status === 403 || response.status === 401) {
            window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
            return;
          }
          const errData = await response.json();
          showToast(errData.error || 'Follow action failed', 'error');
          btn.disabled = false;
          return;
        }

        const data = await response.json();
        if (data.success) {
          if (data.is_following) {
            btn.classList.add('following');
            btn.innerHTML = '<span>Following</span>';
            showToast(`You are now following @${username}`, 'success');
          } else {
            btn.classList.remove('following');
            btn.innerHTML = '<span>Follow</span>';
            showToast(`Unfollowed @${username}`, 'info');
          }

          // Update follower counters on page if present
          const countEl = document.getElementById(`followers-count-${username}`) || document.getElementById('profile-followers-count');
          if (countEl && data.followers_count !== undefined) {
            countEl.textContent = data.followers_count;
          }
        }
      } catch (err) {
        console.error('Follow error:', err);
      } finally {
        btn.disabled = false;
      }
    });
  });
}

/* ==========================================================================
   Live Image Upload Preview (Feed Composer, Modal, and Profile)
   ========================================================================== */
function initImageUploadPreviews() {
  // Feed composer image input
  setupImagePreviewInput('post-image-input', 'composer-preview-container', 'composer-preview-img', 'remove-preview-btn');

  // Modal image input
  setupImagePreviewInput('modal-post-image-input', 'modal-preview-container', 'modal-preview-img', 'modal-remove-preview-btn');

  // Profile avatar input
  setupImagePreviewInput('profile-avatar-input', 'avatar-preview-container', 'avatar-preview-img', null);
}

function setupImagePreviewInput(inputId, containerId, imgId, removeBtnId) {
  const input = document.getElementById(inputId);
  const container = document.getElementById(containerId);
  const img = document.getElementById(imgId);
  const removeBtn = removeBtnId ? document.getElementById(removeBtnId) : null;

  if (!input || !container || !img) return;

  input.addEventListener('change', () => {
    const file = input.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert('File size exceeds 5MB limit. Please select a smaller image.');
        input.value = '';
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        img.src = e.target.result;
        container.style.display = 'block';
      };
      reader.readAsDataURL(file);
    }
  });

  if (removeBtn) {
    removeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      input.value = '';
      img.src = '';
      container.style.display = 'none';
    });
  }
}

/* ==========================================================================
   Modals & Dialogs
   ========================================================================== */
function initModals() {
  // Open modal trigger buttons
  document.querySelectorAll('[data-open-modal]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = btn.getAttribute('data-open-modal');
      openModal(modalId);
    });
  });

  // Close buttons
  document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modal = btn.closest('.modal-backdrop');
      if (modal) closeModal(modal.id);
    });
  });

  // Click outside modal card to close
  document.querySelectorAll('.modal-backdrop').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal(modal.id);
      }
    });
  });

  // Escape key to close
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-backdrop.show').forEach(m => closeModal(m.id));
    }
  });
}

window.openModal = function(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
};

window.closeModal = function(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
  }
};

/* ==========================================================================
   Dropdown Menus
   ========================================================================== */
function initDropdowns() {
  document.querySelectorAll('.post-header-menu-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const menu = btn.nextElementSibling;
      // Close other open dropdowns
      document.querySelectorAll('.dropdown-menu.show').forEach(m => {
        if (m !== menu) m.classList.remove('show');
      });
      if (menu) menu.classList.toggle('show');
    });
  });

  document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-menu.show').forEach(m => m.classList.remove('show'));
  });
}

/* ==========================================================================
   Share Button (Copy Link)
   ========================================================================== */
function initShareButtons() {
  document.querySelectorAll('.share-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const postId = btn.dataset.postId;
      const url = `${window.location.origin}/post/${postId}/`;

      if (navigator.clipboard) {
        try {
          await navigator.clipboard.writeText(url);
          showToast('Post link copied to clipboard!', 'success');
        } catch (err) {
          prompt('Copy this link:', url);
        }
      } else {
        prompt('Copy this link:', url);
      }
    });
  });
}

/* ==========================================================================
   Auto-dismiss Flash Messages
   ========================================================================== */
function initAutoDismissAlerts() {
  document.querySelectorAll('.alert-card').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      setTimeout(() => alert.remove(), 400);
    }, 4500);
  });
}

function escapeHtml(string) {
  const div = document.createElement('div');
  div.innerText = string;
  return div.innerHTML;
}

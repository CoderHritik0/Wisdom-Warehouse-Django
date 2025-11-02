function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
  /* ---------------------------
     DELETE MODAL LOGIC
  ---------------------------- */
  const deleteModal = document.getElementById("deleteModal");
  const confirmBtn = document.getElementById("confirmDeleteBtn");

  let deleteType = null;
  let deleteId = null;
  let triggerBtn = null;

  deleteModal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget;
    deleteType = button.getAttribute("data-type");
    deleteId =
      deleteType === "note"
        ? button.getAttribute("data-note-id")
        : button.getAttribute("data-image-id");
    triggerBtn = button;
  });

  confirmBtn.addEventListener("click", async function () {
    if (!deleteId || !deleteType) return;

    let url = "";
    if (deleteType === "note") {
      url = `/notes/${deleteId}/delete/`;
    } else if (deleteType === "image") {
      url = `/notes/delete_image/${deleteId}/`;
    }

    const response = await fetch(url, {
      method: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    });

    const modal = bootstrap.Modal.getInstance(deleteModal);
    if (modal) modal.hide();

    triggerBtn.closest(".position-relative").remove();

    if (response.ok) {
      if (deleteType === "note") {
        window.location.reload();
      } else if (deleteType === "image") {
        const imageContainer = triggerBtn.closest(".position-relative");
        imageContainer.style.transition = "opacity 0.3s";
        imageContainer.style.opacity = "0";
        setTimeout(() => imageContainer.remove(), 300);
      }
    } else {
      alert("Error deleting item.");
    }
  });

  /* ---------------------------
     HIDE NOTE + SET PIN LOGIC
  ---------------------------- */
  const checkbox = document.getElementById("id_is_hidden");
  const modalEl = document.getElementById("hideNotesModal");
  const modal = new bootstrap.Modal(modalEl);

  if (!checkbox) return;

  checkbox.addEventListener("change", function () {
    modal.show();
  });
});
function setPin() {
  const closeHideModalBtn = document.getElementById("closeHideModalBtn");
  const setPin = document.getElementById("setNotePin");
  if (!setPin) return;

  const pinValue = setPin.value.trim();

  if (!pinValue) {
    alert("Please enter a PIN.");
    return;
  }

  if (pinValue.length !== 6 || isNaN(pinValue)) {
    alert("Please enter a valid 6-digit numeric PIN.");
    return;
  }

  const formData = new FormData();
  formData.append("pin", pinValue);

  fetch(`/notes/set_pin/`, {
    method: "POST",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    body: formData,
  })
    .then((response) => {
      if (!response.ok) throw new Error("Failed to set PIN");
      return response.json();
    })
    .then((data) => {
      console.log("✅ PIN set successfully:", data);
      // continue hide note logic...
    })
    .catch((error) => console.error(error));
  window.location.reload();
}

/* ---------------------------
   MARKDOWN TOOLBAR LOGIC
---------------------------- */
function insertMarkdown(type) {
  const textarea = document.getElementById('id_description');
  if (!textarea) return;

  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const selectedText = textarea.value.substring(start, end);
  let replacement = '';
  let cursorOffset = 0;

  switch (type) {
    case 'heading':
      replacement = `# ${selectedText || 'Heading'}`;
      cursorOffset = selectedText ? replacement.length : 2;
      break;
    case 'bold':
      replacement = `**${selectedText || 'bold text'}**`;
      cursorOffset = selectedText ? replacement.length : 2;
      break;
    case 'italic':
      replacement = `*${selectedText || 'italic text'}*`;
      cursorOffset = selectedText ? replacement.length : 1;
      break;
    case 'quote':
      replacement = `> ${selectedText || 'quote'}`;
      cursorOffset = selectedText ? replacement.length : 2;
      break;
    case 'code':
      replacement = `\`${selectedText || 'code'}\``;
      cursorOffset = selectedText ? replacement.length : 1;
      break;
    case 'link':
      replacement = `[${selectedText || 'link text'}](url)`;
      cursorOffset = selectedText ? replacement.length - 4 : 1;
      break;
    case 'unordered-list':
      replacement = `- ${selectedText || 'list item'}`;
      cursorOffset = selectedText ? replacement.length : 2;
      break;
    case 'ordered-list':
      replacement = `1. ${selectedText || 'list item'}`;
      cursorOffset = selectedText ? replacement.length : 3;
      break;
    case 'task-list':
      replacement = `- [ ] ${selectedText || 'task'}`;
      cursorOffset = selectedText ? replacement.length : 6;
      break;
  }

  textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
  textarea.focus();
  textarea.selectionStart = textarea.selectionEnd = start + cursorOffset;
}

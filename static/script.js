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

  if (deleteModal && confirmBtn) {
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

      if (typeof bootstrap !== 'undefined') {
        const modal = bootstrap.Modal.getInstance(deleteModal);
        if (modal) modal.hide();
      }

      if (triggerBtn) {
        triggerBtn.closest(".position-relative").remove();
      }

      if (response.ok) {
        if (deleteType === "note") {
          window.location.reload();
        } else if (deleteType === "image") {
          const imageContainer = triggerBtn.closest(".position-relative");
          if (imageContainer) {
            imageContainer.style.transition = "opacity 0.3s";
            imageContainer.style.opacity = "0";
            setTimeout(() => imageContainer.remove(), 300);
          }
        }
      } else {
        alert("Error deleting item.");
      }
    });
  }

  /* ---------------------------
     HIDE NOTE + SET PIN LOGIC
  ---------------------------- */
  const checkbox = document.getElementById("id_is_hidden");
  const modalEl = document.getElementById("hideNotesModal");

  if (checkbox && modalEl && typeof bootstrap !== 'undefined') {
    const modal = new bootstrap.Modal(modalEl);
    
    checkbox.addEventListener("change", function () {
      modal.show();
    });
  }
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
document.addEventListener("DOMContentLoaded", function () {
  const markdownButtons = document.querySelectorAll(".markdown-btn");
  const textarea = document.getElementById("id_description");

  if (!textarea || markdownButtons.length === 0) return;

  markdownButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const markdownType = this.getAttribute("data-markdown");
      insertMarkdown(textarea, markdownType);
    });
  });
});

function insertMarkdown(textarea, type) {
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const selectedText = textarea.value.substring(start, end);
  const beforeText = textarea.value.substring(0, start);
  const afterText = textarea.value.substring(end);

  let insertText = "";
  let cursorOffset = 0;

  switch (type) {
    case "header":
      insertText = selectedText ? `# ${selectedText}` : "# Heading";
      cursorOffset = selectedText ? insertText.length : 2;
      break;
    case "bold":
      insertText = selectedText ? `**${selectedText}**` : "**bold text**";
      cursorOffset = selectedText ? insertText.length : 2;
      break;
    case "italic":
      insertText = selectedText ? `*${selectedText}*` : "*italic text*";
      cursorOffset = selectedText ? insertText.length : 1;
      break;
    case "strikethrough":
      insertText = selectedText ? `~~${selectedText}~~` : "~~strikethrough~~";
      cursorOffset = selectedText ? insertText.length : 2;
      break;
    case "code":
      insertText = selectedText ? `\`${selectedText}\`` : "`code`";
      cursorOffset = selectedText ? insertText.length : 1;
      break;
    case "link":
      insertText = selectedText
        ? `[${selectedText}](url)`
        : "[link text](url)";
      cursorOffset = selectedText ? start + selectedText.length + 3 : start + 1;
      break;
    case "ul":
      insertText = selectedText
        ? `- ${selectedText}`
        : "- List item";
      cursorOffset = selectedText ? insertText.length : 2;
      break;
    case "ol":
      insertText = selectedText
        ? `1. ${selectedText}`
        : "1. List item";
      cursorOffset = selectedText ? insertText.length : 3;
      break;
    case "checklist":
      insertText = selectedText
        ? `- [ ] ${selectedText}`
        : "- [ ] Task item";
      cursorOffset = selectedText ? insertText.length : 6;
      break;
    default:
      return;
  }

  textarea.value = beforeText + insertText + afterText;
  
  // Set cursor position
  if (selectedText) {
    textarea.setSelectionRange(start + cursorOffset, start + cursorOffset);
  } else {
    textarea.setSelectionRange(start + cursorOffset, start + cursorOffset);
  }
  
  textarea.focus();
}

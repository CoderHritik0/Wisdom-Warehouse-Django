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
        window.location.href = "/notes/";
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
// function setPin() {
//   const closeHideModalBtn = document.getElementById("closeHideModalBtn");
//   const setPin = document.getElementById("setNotePin");
//   if (!setPin) return;

//   const pinValue = setPin.value.trim();

//   if (!pinValue) {
//     alert("Please enter a PIN.");
//     return;
//   }

//   if (pinValue.length !== 6 || isNaN(pinValue)) {
//     alert("Please enter a valid 6-digit numeric PIN.");
//     return;
//   }

//   const formData = new FormData();
//   formData.append("pin", pinValue);
//   console.log("Setting PIN...", pinValue);

//   fetch(`/notes/set_pin/`, {
//     method: "POST",
//     headers: { "X-CSRFToken": getCookie("csrftoken") },
//     body: formData,
//   })
//     .then((response) => {
//       if (!response.ok) throw new Error("Failed to set PIN");
//       return response.json();
//     })
//     .then((data) => {
//       console.log("✅ PIN set successfully:", data);
//       // continue hide note logic...
//     })
//     .catch((error) => console.error(error));
//   window.location.reload();
// }

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", function (e) {
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();
    const rating = document.getElementById("rating").value;

    if (!email || !message || !rating) {
      alert("Please fill in all required fields.");
      e.preventDefault(); // stop form submission
    }

    // Add more custom validations if needed
  });
});

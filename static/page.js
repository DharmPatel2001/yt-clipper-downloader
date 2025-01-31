document.addEventListener("DOMContentLoaded", function () {
  const toggleSwitch = document.getElementById("toggle");
  const starttimeFields = document.getElementById("starttime-fields");
  const endtimeFields = document.getElementById("endtime-fields");

  // Toggle visibility of start and end time fields
  toggleSwitch.addEventListener("change", function () {
    if (toggleSwitch.checked) {
      starttimeFields.style.display = "flex";
      endtimeFields.style.display="flex";
    } else {
      starttimeFields.style.display = "none";
      endtimeFields.style.display="none";
    }
  });
  const toastContainer = document.getElementById('toast-container');
  if (toastContainer) {
    // Display the toast
    toastContainer.style.display = 'block';
    setTimeout(function() {
      toastContainer.style.opacity = 0;
      setTimeout(function() {
        toastContainer.remove();
      }, 500);
    }, 3000); // Toast fades after 3 seconds
}});
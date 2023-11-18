const qAreaAlerts = document.querySelector(".area-alerts");

export function addAlert(level, message) {
  let alertsRaw = sessionStorage.getItem("alerts");
  let alerts = alertsRaw === null ? [] : JSON.parse(alertsRaw);
  alerts.push({ level, message });
  sessionStorage.setItem("alerts", JSON.stringify(alerts));
}

export function renderAlerts() {}

qAreaAlerts?.addEventListener("click", function (e) {
  // Did we click the close button on an alert?
  if (e.target.matches(".msg-alert .btn-close")) {
    // Delete the clicked alert
    let alert = e.target.parentElement;
    alert.remove();

    // Delete the container once all messages are dismissed
    if (qAreaAlerts.childElementCount === 0) {
      qAreaAlerts.remove();
    }
  }
});

const qAreaAlerts = document.querySelector(".area-alerts");

export function addAlert(level, message) {
  let alertsRaw = sessionStorage.getItem("alerts");
  let alerts = alertsRaw === null ? [] : JSON.parse(alertsRaw);
  alerts.push({ level, message });
  sessionStorage.setItem("alerts", JSON.stringify(alerts));
}

export function renderAlerts() {
  let alertsRaw = sessionStorage.getItem("alerts");
  let alerts = alertsRaw === null ? [] : JSON.parse(alertsRaw);

  alerts.forEach(v => {
    let msg = `<div class="msg-alert ${v.level}" role="alert">
      <p>${v.message}</p>
      <img class="btn-close" width="25" height="25" alt="" src="/static/img/close.svg">
    </div>`;
    qAreaAlerts?.insertAdjacentHTML("afterbegin", msg);
  });

  // Remove the alerts afer showing them
  sessionStorage.setItem("alerts", JSON.stringify([]));
}

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

document.addEventListener("DOMContentLoaded", renderAlerts);

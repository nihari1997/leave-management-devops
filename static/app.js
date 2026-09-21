const form = document.querySelector("#leave-form");
const employeeSelect = document.querySelector("#employee-id");
const leaveList = document.querySelector("#leave-list");
const message = document.querySelector("#message");

async function loadEmployees() {
  const response = await fetch("/api/employees");
  const { employees } = await response.json();
  employeeSelect.innerHTML = employees
    .map((employee) => `<option value="${employee.id}">${employee.name} — ${employee.department}</option>`)
    .join("");
}

async function loadLeaves() {
  const response = await fetch("/api/leaves");
  const { leaves } = await response.json();
  leaveList.innerHTML = leaves.length
    ? leaves.map((leave) => `<li>Employee #${leave.employee_id}: ${leave.start_date} to ${leave.end_date} (${leave.status})</li>`).join("")
    : "<li>No leave requests yet.</li>";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    employee_id: Number(employeeSelect.value),
    start_date: document.querySelector("#start-date").value,
    end_date: document.querySelector("#end-date").value,
    reason: document.querySelector("#reason").value,
  };
  const response = await fetch("/api/leaves", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await response.json();
  message.textContent = response.ok ? "Leave request submitted." : body.error;
  if (response.ok) {
    form.reset();
    await loadLeaves();
  }
});

loadEmployees();
loadLeaves();

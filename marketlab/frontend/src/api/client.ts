const API_BASE = "/api/v1";

function authHeaders(): Record<string, string> {
  const token = localStorage.getItem("token");
  if (token) {
    return { "Authorization": "Bearer " + token };
  }
  return {};
}

export async function fetchTasks() {
  const res = await fetch(API_BASE + "/tasks");
  if (!res.ok) throw new Error("Failed to fetch tasks");
  return res.json();
}

export async function fetchTask(taskId: string) {
  const res = await fetch(API_BASE + "/tasks/" + taskId);
  if (!res.ok) throw new Error("Failed to fetch task");
  return res.json();
}

export async function submitSolution(taskId: string, userCode: string) {
  const res = await fetch(API_BASE + "/submissions", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ task_id: taskId, user_code: userCode }),
  });
  if (!res.ok) throw new Error("Failed to submit");
  return res.json();
}

export async function fetchSubmissions(taskId?: string) {
  const url = taskId
    ? API_BASE + "/submissions?task_id=" + taskId
    : API_BASE + "/submissions";
  const res = await fetch(url, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to fetch submissions");
  return res.json();
}

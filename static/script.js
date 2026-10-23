const form = document.getElementById("form");
const button = document.getElementById("generate");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");
const results = document.getElementById("results");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  button.disabled = true;
  loading.classList.remove("hidden");
  errorBox.classList.add("hidden");
  results.classList.add("hidden");

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: document.getElementById("topic").value,
        audience: document.getElementById("audience").value,
        length: document.getElementById("length").value,
      }),
    });
    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Something went wrong. Please try again.");
    } else {
      showResults(data);
    }
  } catch (err) {
    showError("Couldn't reach the server. Make sure it's running and try again.");
  }

  button.disabled = false;
  loading.classList.add("hidden");
});

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

// Small helper to make an element with a class and text
function makeElement(tag, className, text) {
  const el = document.createElement(tag);
  el.className = className;
  el.textContent = text;
  return el;
}

function showResults(data) {
  const hooks = document.getElementById("hooks");
  hooks.innerHTML = "";
  for (const hook of data.hooks) {
    const card = makeElement("div", "hook", "");
    card.appendChild(makeElement("span", "score", hook.score + "/10"));
    card.appendChild(makeElement("p", "hook-text", hook.text));
    card.appendChild(makeElement("p", "hook-why", hook.why));
    hooks.appendChild(card);
  }

  const script = document.getElementById("script");
  script.innerHTML = "";
  for (const beat of data.script) {
    const item = document.createElement("li");
    item.appendChild(makeElement("div", "time", beat.time));
    item.appendChild(makeElement("div", "voiceover", beat.voiceover));
    item.appendChild(makeElement("div", "on-screen", "On screen: " + beat.on_screen_text));
    script.appendChild(item);
  }

  document.getElementById("caption").textContent = data.caption;
  results.classList.remove("hidden");
}

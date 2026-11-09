'use strict';
const form = document.getElementById('expert-form');
const submit = document.getElementById('submit-btn');
const errorBox = document.getElementById('error');
const idleView = document.getElementById('idle-view');
const resultView = document.getElementById('result-view');
const progressBar = document.getElementById('progress-bar');
const text = (id, value) => { document.getElementById(id).textContent = value; };

function answers() {
  const data = new FormData(form);
  return { goal: data.get('goal'), payment: data.get('payment'), accounts: data.get('accounts') };
}
function updateProgress() {
  const a = answers();
  progressBar.style.width = `${Object.values(a).filter(Boolean).length / 3 * 100}%`;
}
function resetView() {
  errorBox.hidden = true;
  idleView.hidden = false;
  resultView.hidden = true;
  updateProgress();
}
function showResult(result) {
  text('result-title', result.title);
  text('result-subtitle', result.subtitle);
  text('result-description', result.description);
  text('result-reason', result.reason);
  text('result-rule', result.rule);
  text('result-rule-id', `${result.rule_id} · CLIPS INFERENCE ENGINE`);
  text('disclaimer', result.disclaimer);
  const list = document.getElementById('result-features');
  list.replaceChildren(...result.features.map(feature => {
    const li = document.createElement('li');
    li.textContent = feature;
    return li;
  }));
  idleView.hidden = true;
  resultView.hidden = false;
}
form.addEventListener('change', updateProgress);
form.addEventListener('reset', () => setTimeout(resetView, 0));
document.getElementById('restart-btn').addEventListener('click', () => {
  form.reset();
  document.getElementById('expert').scrollIntoView({ behavior: 'smooth' });
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  errorBox.hidden = true;
  submit.disabled = true;
  const original = submit.innerHTML;
  submit.textContent = 'Анализируем ответы…';
  try {
    const response = await fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(answers()),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Не удалось получить рекомендацию.');
    showResult(data);
    if (window.innerWidth < 921) document.querySelector('.result-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    errorBox.textContent = `${err.message} Проверьте, запущен ли Flask-сервер.`;
    errorBox.hidden = false;
  } finally {
    submit.disabled = false;
    submit.innerHTML = original;
  }
});
updateProgress();

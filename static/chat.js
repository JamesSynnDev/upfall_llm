const ws = new WebSocket(`ws://${location.host}/ws/chat`);
const chatList = document.getElementById('chat-list');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

// Shift+Enter 는 줄바꿈, Enter 단독은 전송
chatInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();   // 기본 줄바꿈 방지
    chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
  }
});

function appendMessage(text, cls) {
  const li = document.createElement('li');
  li.className = `message ${cls}`;
  li.textContent = text;
  chatList.appendChild(li);
  chatList.scrollTop = chatList.scrollHeight;
}

chatForm.addEventListener('submit', e => {
  e.preventDefault();
  const msg = chatInput.value.trim();
  if (!msg) return;
  appendMessage(msg, 'user');
  chatInput.value = '';
  ws.send(msg);
  chatInput.disabled = true;
});

ws.addEventListener('message', event => {
  appendMessage(event.data, 'bot');
  chatInput.disabled = false;
  chatInput.focus();
});

ws.addEventListener('open', () => {
  console.log('WebSocket 연결됨');
});

ws.addEventListener('close', () => {
  console.log('WebSocket 끊김');
});

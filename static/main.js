const canvas = document.getElementById('drawCanvas');
const ctx = canvas.getContext('2d');
const sendBtn = document.getElementById('sendBtn');
const resultDiv = document.getElementById('result');

let painting = false;

// ฟังก์ชันสำหรับวาดภาพ
function startPosition(e) {
    painting = true;
    draw(e);
}
function endPosition() {
    painting = false;
    ctx.beginPath();
}
function draw(e) {
    if (!painting) return;
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

// Event listeners
canvas.addEventListener('mousedown', startPosition);
canvas.addEventListener('mouseup', endPosition);
canvas.addEventListener('mousemove', draw);

// ส่งภาพไปยัง Backend
sendBtn.addEventListener('click', () => {
    const imageData = canvas.toDataURL(); // แปลงภาพใน canvas เป็น Base64
    fetch('/process_image', {
        method: 'POST',
        body: JSON.stringify({ image: imageData }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerText = 'ผลลัพธ์: ' + data.result;
    })
    .catch(err => console.error(err));
});
s
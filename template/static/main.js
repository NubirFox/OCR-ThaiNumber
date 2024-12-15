const canvas = document.getElementById('drawCanvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
const sendBtn = document.getElementById('sendBtn');
const resultDiv = document.getElementById('result');
const imageResultDiv = document.getElementById('imageResult');  // เพิ่ม div เพื่อแสดงภาพที่ประมวลผล

let painting = false;

function startPosition(e) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    painting = true;
    draw(e);
}

function endPosition() {
    painting = false;
    ctx.beginPath();
}

function draw(e) {
    if (!painting) return;
    ctx.lineWidth = 10;
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
    const imageData = canvas.toDataURL('image/png');

    const byteString = atob(imageData.split(',')[1]);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const uintArray = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
        uintArray[i] = byteString.charCodeAt(i);
    }

    const file = new Blob([uintArray], { type: 'image/png' });

    // สร้าง FormData และเพิ่มไฟล์ภาพ
    const formData = new FormData();
    formData.append('image', file, 'image.png');

    // ส่งข้อมูลผ่าน POST Request
    fetch('http://127.0.0.1:5000/process_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerText = 'ผลลัพธ์: ' + data.result;

        // แสดงภาพที่ประมวลผลแล้ว
        const processedImage = data.processed_image;
        imageResultDiv.innerHTML = `<img src="data:image/png;base64,${processedImage}" />`;
    })
    .catch(err => console.error(err));
});
/* =========================================
   TOOLS - MAIN JAVASCRIPT
   ========================================= */

/* --- 1. RESIZER TOOL LOGIC --- */
let originalWidth = 0;
let originalHeight = 0;
let currentMode = 'resize';

function loadFile(event) {
    const img = document.getElementById('preview');
    const file = event.target.files[0];
    
    if (file && img) {
        const reader = new FileReader();
        reader.onload = function(e) {
            img.src = e.target.result;
            img.style.display = 'block';
            const placeholder = document.getElementById('placeholder');
            if(placeholder) placeholder.style.display = 'none';
            
            const i = new Image();
            i.src = e.target.result;
            i.onload = function() {
                originalWidth = this.width;
                originalHeight = this.height;
                const widthInput = document.getElementById('width');
                const heightInput = document.getElementById('height');
                if(widthInput) widthInput.value = originalWidth;
                if(heightInput) heightInput.value = originalHeight;
                const info = document.getElementById('info');
                if(info) info.innerText = `Original: ${originalWidth} x ${originalHeight} px`;
            };
        }
        reader.readAsDataURL(file);
    }
}

// Aspect Ratio Auto-Calculation
document.addEventListener("DOMContentLoaded", function() {
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    const lockRatio = document.getElementById('lockRatio');
    
    if(widthInput && heightInput && lockRatio) {
        widthInput.addEventListener('input', function() {
            if(lockRatio.checked && originalWidth > 0) {
                const ratio = originalHeight / originalWidth;
                heightInput.value = Math.round(this.value * ratio);
            }
        });
        heightInput.addEventListener('input', function() {
            if(lockRatio.checked && originalHeight > 0) {
                const ratio = originalWidth / originalHeight;
                widthInput.value = Math.round(this.value * ratio);
            }
        });
    }
});

function switchTab(mode) {
    currentMode = mode;
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    if(event && event.target) event.target.classList.add('active');
    
    document.querySelectorAll('.control-group').forEach(div => div.classList.remove('active'));
    const activeControl = document.getElementById(mode + '-controls');
    if(activeControl) activeControl.classList.add('active');
}

async function processImage() {
    const fileInput = document.getElementById('fileInput');
    if(!fileInput || fileInput.files.length === 0) { alert("Please select an image first!"); return; }

    const btn = document.getElementById('actionBtn');
    btn.innerText = "Processing...";
    btn.disabled = true;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('mode', currentMode);

    if (currentMode === 'resize') {
        formData.append('width', document.getElementById('width').value);
        formData.append('height', document.getElementById('height').value);
    } else {
        formData.append('quality', document.getElementById('quality').value);
    }

    try {
        const response = await fetch('/api/process-image', { method: 'POST', body: formData });
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "netakit_edited.png"; 
            document.body.appendChild(a);
            a.click();
            a.remove();
        } else {
            alert("Error processing image");
        }
    } catch (err) {
        alert("Server Error");
    }
    btn.innerText = "Download Processed Image";
    btn.disabled = false;
}

/* --- 2. BACKGROUND REMOVER LOGIC --- */
function previewBgImage() {
  const fileInput = document.getElementById("bgFileInput");
  if(!fileInput) return;
  const file = fileInput.files[0];
  const preview = document.getElementById("bgPreviewImg");

  if(file && preview) {
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
  }
}

async function uploadBgImage() {
  const fileInput = document.getElementById('bgFileInput');
  const btn = document.getElementById('bgBtn');
  const loader = document.getElementById('bgLoader');
  const resultDiv = document.getElementById('bgResult');

  if(fileInput.files.length === 0) {
    alert("Select image first");
    return;
  }

  btn.disabled = true;
  loader.style.display = "block";

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  try {
    const response = await fetch('/web_remove', { method: 'POST', body: formData });
    if(response.ok) {
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      document.getElementById("bgOutputImage").src = url;
      document.getElementById("bgDownloadLink").href = url;
      resultDiv.style.display = "block";
    } else {
      alert("Error processing image");
    }
  } catch(err) {
    alert("Server error");
  }

  loader.style.display = "none";
  btn.disabled = false;
                  }
      

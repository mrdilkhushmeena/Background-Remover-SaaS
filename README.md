# 🪄 Background Remover SaaS API

## 🚀 Overview
A production-ready SaaS module that removes image backgrounds instantly and provides a secure, token-based API for developers to integrate into their applications.

<div align="center">
  <img src="bg-ui.jpg" alt="Background Remover UI" width="350"/>
</div>

---

## 🔑 Key Features
* **Admin-Controlled API Keys:** Secure access generation and management.
* **AI Image Processing:** High-accuracy background removal.
* **Usage Logging:** Track API requests and processing limits per user.
* **Decoupled Architecture:** Clean separation between the Flask API backend and the frontend UI.

## 🛠 Tech Stack
* **Backend:** Flask, Python
* **Database:** SQLite
* **Image Processing:** Pillow, rembg (AI Engine)
* **Frontend:** HTML, CSS, JavaScript (Vanilla)

---

## 📡 API Documentation

### Endpoint
`POST /api/remove`

### Headers
`X-API-KEY: your_generated_api_key`

### Request Body (Form-Data)
| Key | Type | Description |
| :--- | :--- | :--- |
| `file` | `image` | The image file to be processed (PNG/JPG) |

---

## 🌍 Live Demo
* **Frontend UI:** [tools.netakit.com](https://tools.netakit.com)

## 🔮 Roadmap / Future Improvements
- [ ] Implement rate limiting (Redis)
- [ ] Add payment gateway integration
- [ ] Advanced analytics dashboard for API usage

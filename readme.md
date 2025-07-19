# SockChat

**Sock Chat** is a multithreaded terminal-based chat application built using Python Sockets. It allows multiple users to communicate in real-time over a shared network or across the internet using Tailscale. The app is lightweight, easy to set up, and requires no external dependencies.

It supports multiple client connections, automatically fetches and displays recent chat history on join, and runs entirely in the terminal — making it suitable for quick team discussions, LAN messaging, or remote communication over encrypted mesh networks. With minimal setup and a plain-text interface, it's ideal for environments where simplicity, speed, and portability matter.

**Sock Chat works for both private and public networks**

## 🚀 Features

* Real-time chat over terminal
* Multi-client support
* Log history fetching on client connect
* Thread-safe message broadcasting
* Run locally or over public network (via Tailscale)
* Clean and minimal setup



## 📁 Files

* `server.py` – Starts the chat server and handles client connections
* `client.py` – Connects to server and handles message send/receive



## 🖥️ Run Locally (LAN / Same WiFi)

1. Open a terminal in the project directory.

2. Start the server:

   ```bash
   python3 server.py
   ```

   The terminal will show:

   ```
   [Listening] IP = 192.168.xx.xx, PORT=xxxxx
   ```

3. On other devices in the same network:

   * Ensure `client.py` is copied there
   * Run:

     ```bash
     python3 client.py
     ```
   * Enter the **IP** and **PORT** shown on the server.

4. You’re now connected! Multiple clients can join and chat seamlessly.



## 🌐 Run Over Public Network (via Tailscale)

1. **Install Tailscale** on **all devices** (server and clients):
   [https://tailscale.com/download](https://tailscale.com/download)

2. Log into Tailscale on all devices using a **shared account**.

3. On the **server**:

   * Edit `server.py`:

     ```python
     #SERVER = socket.gethostbyname(socket.gethostname())  # ← Comment this line
     SERVER = "100.x.y.z"  # ← Replace with your Tailscale IP
     ```
   * Start the server:

     ```bash
     python3 server.py
     ```

4. On **client devices**:

   * Run:

     ```bash
     python3 client.py
     ```
   * Enter the **Tailscale IP** of the server and the **port number** shown in server logs.

5. Chat is now working across devices on the public internet using Tailscale's secure mesh network.



## 🛠️ Troubleshooting Tailscale

* Check device connectivity:

  ```bash
  tailscale status
  ```

* Ping other devices:

  ```bash
  ping <tailscale-ip>
  ```

* If issues persist, reset the Tailscale state:

  ```bash
  tailscale down
  tailscale up
  tailscale status
  ```

---

## 📌 Notes

* Use `!dsc` in chat to disconnect a client gracefully.
* Server dynamically picks an open port.
* Logs are compressed and fetched when a new client joins.
* Server auto-cleans disconnected clients.
* Chat logs use a separate 64-byte header (`LOG_HEADER = 64`) to handle larger message payloads without truncation. 

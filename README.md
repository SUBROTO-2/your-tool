# ⚡ SCRAP V5 — True Playback Verification

<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=26&pause=1000&color=00FF88&center=true&vCenter=true&width=800&lines=SCRAP+V5;TRUE+PLAYBACK+VERIFICATION;HLS+%2B+MPEG-TS+VALIDATION;TERMUX+READY" alt="SCRAP V5">

</p>

<p align="center">

<img src="https://img.shields.io/badge/Version-5.0-00ff88?style=for-the-badge">
<img src="https://img.shields.io/badge/Platform-Termux-black?style=for-the-badge&logo=android">
<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github">

</p>

---

## 📌 SCRAP V5 কী?

**SCRAP V5** হলো একটি Python-based Termux tool, যেটি আপনার অনুমোদিত Xtream/IPTV account-এর Live TV channel পরীক্ষা করে working channel গুলো আলাদা করতে পারে।

এটি HLS/M3U8 playlist, stream response এবং media data যাচাই করে তারপর verified channel-এর M3U playlist তৈরি করে।

### ✨ প্রধান সুবিধা

* ⚡ দ্রুত asynchronous channel scanning
* 📡 Xtream API connection
* 🔎 HLS / M3U8 verification
* 🎬 Live stream playback-style verification
* 🧪 MPEG-TS / MP4 / AAC media validation
* 🔁 Re-verification
* 📂 Working M3U playlist export
* 📝 Detailed scan report
* ❌ Rejected channel log
* 📱 Termux support

---

# 📱 Termux-এ কীভাবে Install করবেন?

## 🟢 একদম নতুন হলে এইভাবে করুন

ভয় পাওয়ার কিছু নেই। নিচের **Step 1 → Step 2 → Step 3** এভাবে একটার পর একটা করবেন।

প্রতিটি command আলাদা করে:

**Copy → Termux-এ Paste → Enter**

---

# 1️⃣ Termux Update করুন

প্রথমে Termux খুলে নিচের command দিন।

### 📋 Copy করুন

```bash
pkg update -y
```

তারপর **Enter** চাপুন।

---

# 2️⃣ Termux Upgrade করুন

### 📋 Copy করুন

```bash
pkg upgrade -y
```

তারপর **Enter** চাপুন।

---

# 3️⃣ Python Install করুন

SCRAP V5 Python দিয়ে তৈরি।

### 📋 Copy করুন

```bash
pkg install python -y
```

তারপর **Enter** চাপুন।

---

# 4️⃣ Git Install করুন

আমাদের GitHub repository থেকে tool download করার জন্য Git লাগবে।

### 📋 Copy করুন

```bash
pkg install git -y
```

তারপর **Enter** চাপুন।

---

# 5️⃣ Storage Permission দিন

### 📋 Copy করুন

```bash
termux-setup-storage
```

এরপর Android permission চাইলে:

**Allow** চাপুন।

---

# 6️⃣ GitHub থেকে Tool Download করুন

এখন সবচেয়ে গুরুত্বপূর্ণ ধাপ।

SCRAP V5-এর GitHub repository হলো:

**https://github.com/SUBROTO-2/your-tool**

Repository clone করতে নিচের command দিন।

### 📋 Copy করুন

```bash
git clone https://github.com/SUBROTO-2/your-tool.git
```

Enter চাপার পর GitHub repository আপনার Termux-এ download হবে।

---

# 7️⃣ Tool-এর Folder-এ ঢুকুন

Download শেষ হলে নিচের command দিন।

### 📋 Copy করুন

```bash
cd your-tool
```

Enter চাপুন।

---

# 8️⃣ প্রয়োজনীয় Python Package Install করুন

SCRAP V5-এর জন্য প্রয়োজনীয় Python package install করতে হবে।

## 📦 aiohttp

### 📋 Copy করুন

```bash
pip install aiohttp
```

---

## 📦 requests

### 📋 Copy করুন

```bash
pip install requests
```

---

## 📦 urllib3

### 📋 Copy করুন

```bash
pip install urllib3
```

---

# 9️⃣ SCRAP V5 Run করুন 🚀

সব installation শেষ হলে এখন tool চালানোর সময়।

আপনার tool file যদি:

```text
SCRAP_V5.py
```

নামে থাকে, তাহলে নিচের command দিন।

### 📋 Copy করুন

```bash
python SCRAP_V5.py
```

তারপর **Enter** চাপুন।

🎉 Tool চালু হয়ে যাবে।

---

# 🔐 Tool চালু হলে কী দিতে হবে?

SCRAP V5 চালু হলে এটি আপনার কাছে Xtream account-এর তথ্য চাইবে।

সাধারণত:

```text
Host
Username
Password
```

উদাহরণ:

```text
Host     : http://example.com:8080
Username : your_username
Password : your_password
```

### ⚠️ গুরুত্বপূর্ণ

শুধুমাত্র **নিজের বা ব্যবহারের অনুমতি থাকা account/server** ব্যবহার করবেন।

---

# 🔄 Tool কীভাবে কাজ করবে?

Tool চালু হওয়ার পর মোটামুটি এইভাবে কাজ করবে:

```text
START
   │
   ▼
Xtream API Connect
   │
   ▼
Account Check
   │
   ▼
Live Channels Load
   │
   ▼
HLS / M3U8 Verification
   │
   ▼
Media Validation
   │
   ▼
Working Channels
   │
   ▼
Re-Verification
   │
   ▼
Final Verified Channels
   │
   ▼
M3U Export
```

---

# 📂 Scan শেষ হলে কী পাবেন?

Tool scan শেষ হলে `scrap_output` নামে একটি folder তৈরি হতে পারে।

সেখানে সাধারণত থাকবে:

```text
scrap_output/
│
├── scrap_working.m3u
├── scrap_details.txt
└── scrap_rejected.log
```

### ✅ `scrap_working.m3u`

এখানে final verified channel-এর M3U playlist থাকবে।

### 📝 `scrap_details.txt`

এখানে scan-এর বিস্তারিত তথ্য ও result থাকবে।

### ❌ `scrap_rejected.log`

যে channelগুলো verification-এ pass করেনি, সেগুলোর তথ্য এখানে থাকবে।

---

# 🛠️ যদি `ModuleNotFoundError` আসে

যেমন:

```text
ModuleNotFoundError: No module named 'aiohttp'
```

তাহলে:

### 📋 Copy করুন

```bash
pip install aiohttp
```

`requests` না থাকলে:

```bash
pip install requests
```

`urllib3` না থাকলে:

```bash
pip install urllib3
```

---

# ❗ যদি `python SCRAP_V5.py` কাজ না করে

প্রথমে folder-এর ভিতরের file দেখুন।

### 📋 Copy করুন

```bash
ls
```

এখন দেখুন সেখানে Python file-এর নাম কী।

যদি file-এর নাম:

```text
scrap_v3.py
```

হয়, তাহলে চালাবেন:

### 📋 Copy করুন

```bash
python scrap_v3.py
```

আর যদি:

```text
SCRAP_V5.py
```

হয়, তাহলে:

### 📋 Copy করুন

```bash
python SCRAP_V5.py
```

**Linux/Termux-এ file name ঠিকভাবে লিখতে হবে।**

---

# 🔁 পরেরবার কীভাবে চালাবেন?

একবার install হয়ে গেলে পরেরবার Git clone বা package install করার দরকার নেই।

শুধু:

### Step 1

```bash
cd ~/your-tool
```

### Step 2

```bash
python SCRAP_V5.py
```

ব্যস! 🚀

---

# 🧹 আবার নতুন করে GitHub থেকে Download করতে চাইলে

পুরোনো folder মুছে:

```bash
rm -rf your-tool
```

তারপর:

```bash
git clone https://github.com/SUBROTO-2/your-tool.git
```

তারপর:

```bash
cd your-tool
```

এবং:

```bash
python SCRAP_V5.py
```

---

# ⚡ Quick Install — অভিজ্ঞদের জন্য

যারা সবকিছু একসাথে করতে চান:

### 📋 Copy করুন

```bash
pkg update -y && pkg upgrade -y
```

### 📋 Copy করুন

```bash
pkg install python git -y
```

### 📋 Copy করুন

```bash
git clone https://github.com/SUBROTO-2/your-tool.git
```

### 📋 Copy করুন

```bash
cd your-tool
```

### 📋 Copy করুন

```bash
pip install aiohttp requests urllib3
```

### 📋 Copy করুন

```bash
python SCRAP_V5.py
```

---

# 🔗 GitHub Repository

<p align="center">

<a href="https://github.com/SUBROTO-2/your-tool">
<img src="https://img.shields.io/badge/Visit-GitHub%20Repository-black?style=for-the-badge&logo=github">
</a>

</p>

---

# 👨‍💻 Developer

<p align="center">

<b>Krishna_Subroto</b>

</p>

<p align="center">

<a href="https://t.me/Krishna_Subroto">
<img src="https://img.shields.io/badge/Telegram-@Krishna__Subroto-26A5E4?style=for-the-badge&logo=telegram">
</a>

</p>

👉 Developer-এর Telegram:

**[@Krishna_Subroto](https://t.me/Krishna_Subroto)**

---

# ⚠️ Disclaimer

SCRAP V5 শুধুমাত্র বৈধ, অনুমোদিত এবং নিজের/অনুমতিপ্রাপ্ত IPTV বা Xtream account এবং stream পরীক্ষা করার জন্য ব্যবহার করুন।

অন্যের account, server বা stream অনুমতি ছাড়া ব্যবহার বা পরীক্ষা করার জন্য এই tool ব্যবহার করবেন না।

ব্যবহারের দায় সম্পূর্ণ ব্যবহারকারীর।

---

<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=800&color=00FF88&center=true&vCenter=true&width=750&lines=SCRAP+V5+%E2%9A%A1;CLONE+%E2%86%92+INSTALL+%E2%86%92+RUN;TRUE+PLAYBACK+VERIFICATION;DEVELOPED+BY+KRISHNA_SUBROTO" alt="SCRAP V5">

</p>

<p align="center">

<b>⚡ SCRAP V5 • TRUE PLAYBACK VERIFICATION</b>

</p>

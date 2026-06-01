🤖 Lab 3: Chatbot vs ReAct Agent (Bài nộp)
Kho lưu trữ này chứa bài nộp hoàn chỉnh của tôi cho Lab 3 của khóa học Agentic AI. Dự án minh họa quá trình tiến hóa từ một LLM Chatbot cơ bản thành một **ReAct Agent** tinh vi, được trang bị công cụ (tools), hệ thống bảo vệ (guardrails), và hệ thống đo lường (telemetry) chuẩn công nghiệp.

## ✨ Các Tính Năng Đã Triển Khai

1. **Baseline Chatbot (`chatbot.py`)**: Một kịch bản trò chuyện đơn giản được dùng làm cơ sở đối chiếu (baseline) để chứng minh những hạn chế của LLM tiêu chuẩn trong việc suy luận đa bước.
2. **ReAct Agent (`run_agent.py`)**: Một Agent hoạt động hoàn chỉnh, triển khai vòng lặp `Suy nghĩ-Hành động-Quan sát` (Thought-Action-Observation) trong `src/agent/agent.py`.
3. **Các Công Cụ Tùy Chỉnh (Custom Tools)**:
   - `calc_math`: Tính toán toán học an toàn.
   - `web_search`: Công cụ tìm kiếm giả lập để lấy giá sản phẩm, giảm giá, và thông tin giao hàng.
4. **Hệ Thống Bảo Vệ & Logic Thử Lại (Agent v2)**: Agent tự động bắt các lỗi định dạng (Parsing Errors) và ảo giác công cụ (Tool Hallucinations), hướng dẫn LLM đi đúng hướng với giới hạn `max_retries` (số lần thử lại tối đa).
5. **Chuyển Đổi Provider (Factory Pattern)**: Dễ dàng chuyển đổi linh hoạt giữa các mô hình OpenAI, Gemini, và Local (Phi-3) bằng cách thay đổi biến `DEFAULT_PROVIDER` trong file `.env`.
6. **Đo Lường Nâng Cao (Advanced Telemetry)**: Ghi log mọi sự kiện dưới dạng JSON có cấu trúc, tự động tính toán `Tỉ lệ Token` (Completion / Prompt) và `Ước tính chi phí (USD)` cho mỗi lần chạy.
7. **Phân Tích Log (`analyze_logs.py`)**: Một script để đọc các log có cấu trúc và phân tích tỷ lệ thành công, lỗi sập, ảo giác, mức tiêu thụ token, và tổng chi phí.

---

## 🚀 Hướng Dẫn Bắt Đầu

### 1. Cài Đặt Môi Trường

Copy file `.env.example` thành `.env` và điền API keys của bạn (hoặc cấu hình Local Models):

```bash
cp .env.example .env
```

### 2. Cài Đặt Thư Viện

```bash
pip install -r requirements.txt
```

### 3. Chạy Hệ Thống

**Chạy Chatbot Baseline:**

```bash
python chatbot.py
```

**Chạy ReAct Agent:**

```bash
python run_agent.py
```

**Phân Tích Log (Lỗi & Thống Kê):**
Sau khi chạy agent, bạn có thể tạo báo cáo tự động về token, chi phí và các lỗi thường gặp:

```bash
python src/telemetry/analyze_logs.py
```

---

## 🏠 Chạy Bằng Local Models (CPU)

Nếu bạn không muốn sử dụng API của OpenAI hay Gemini, bạn có thể chạy các mô hình nguồn mở (như Phi-3) trực tiếp trên CPU thông qua `llama-cpp-python`.

### 1. Tải Mô Hình

Tải file **Phi-3-mini-4k-instruct-q4.gguf** (khoảng 2.2GB) từ Hugging Face:

- Link tải trực tiếp: [phi-3-mini-4k-instruct-q4.gguf](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf)

### 2. Đặt Mô Hình Vào Dự Án

Tạo một thư mục `models/` ở thư mục gốc của dự án và dán file `.gguf` vừa tải vào đó.

### 3. Cập Nhật `.env`

Đổi biến `DEFAULT_PROVIDER` và cập nhật đường dẫn:

```env
DEFAULT_PROVIDER=local
LOCAL_MODEL_PATH=./models/Phi-3-mini-4k-instruct-q4.gguf
```

Chạy script test local để xác nhận mô hình của bạn đang hoạt động bình thường:

```bash
python tests/test_local.py
```

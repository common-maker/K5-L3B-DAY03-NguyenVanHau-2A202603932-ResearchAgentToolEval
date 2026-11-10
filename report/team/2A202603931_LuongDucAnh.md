# Báo cáo cá nhân — Luong Duc Anh

## 1. Thông tin thành viên

- Họ tên: Luong Duc Anh
- MSSV: 2A202603931
- Email: (bổ sung)

## 2. Phần việc phụ trách

- Phụ trách giao diện Streamlit và phần demo live của Research Agent.

## 3. Đóng góp cụ thể

- Tạo giao diện chat trong `starter_v0/app.py`, dùng lại provider, system prompt và tool loop của agent.
- Thêm khả năng mở chat mới và mở lại các cuộc hội thoại đã lưu từ thanh bên; nội dung được khôi phục từ transcript JSON.
- Thêm Streamlit vào `starter_v0/requirements.txt` và hướng dẫn chạy/chọn host, port trong `starter_v0/README.md`.
- Chạy preflight OpenAI và kiểm tra health endpoint của giao diện.
- Chạy chat live gồm tra cứu web, hỏi lại khi thiếu URL, rồi fetch URL được bổ sung; thêm bằng chứng vào mục B4 của báo cáo nhóm.
- Telegram chưa được cấu hình hoặc dùng trong demo.

## 4. Bằng chứng

- UI: `starter_v0/app.py`
- Transcript: `starter_v0/transcripts/v3_openai_20261110T193410992226.transcript.json`
- Báo cáo nhóm: `report/team/group_report.md` (B3, B4, B5a)
- Hỗ trợ AI: dùng Codex để hỗ trợ viết/chỉnh UI và tài liệu; kiểm tra bằng preflight OpenAI, health endpoint Streamlit và transcript chat live.

## 5. Tự đánh giá

- Đã hoàn thành phần triển khai UI và chuẩn bị transcript làm bằng chứng. Phần trình bày UI trực tiếp cho người xem sẽ thực hiện trong buổi demo.

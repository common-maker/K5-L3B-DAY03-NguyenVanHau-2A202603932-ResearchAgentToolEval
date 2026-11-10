# Báo cáo cá nhân — Võ Thị Phương Nhung

## 1. Thông tin thành viên

- Họ tên: Võ Thị Phương Nhung
- MSSV: `2A202603918`
- Email: nhungvo631@gmail.com
- GitHub: nhungvo631-stack

## 2. Phần việc phụ trách

- QA / Unit Tests cho các tool mới (`summarize`, `calculator`, `export_report`).
- Bổ sung và kiểm tra bộ câu hỏi đánh giá nhóm trong `starter_v0/data/eval_group.json`.
- Rà soát contract giữa tool implementation, `TOOL_FUNCTIONS` và unit tests; kiểm tra các nhánh lỗi và guardrail ghi file.

## 3. Đóng góp cụ thể

- Hoàn thiện `starter_v0/tests/test_tools_todo.py` với 15 unit tests, gồm 5 test cho mỗi tool mới:
  - `summarize`: giới hạn số bullet, lọc theo từ khóa, xử lý văn bản rỗng và kiểm tra độ ngắn gọn.
  - `calculator`: phép tính trung bình, phần trăm tăng trưởng, thứ tự ưu tiên/lũy thừa, chia cho 0 và từ chối code injection.
  - `export_report`: ghi UTF-8, ghi đè, không ghi đè, chặn path traversal và filename mặc định.
- Sửa cách test lấy hàm qua `TOOL_FUNCTIONS` và kiểm tra chuẩn lỗi dạng dict `{error: ...}` thay vì giả định tool luôn ném exception.
- Phát hiện qua unit test các lỗi mà eval routing không bắt được: path traversal trong `export_report`, filename mặc định không ghi đúng thư mục kiểm thử, lỗi chia cho 0 và biểu thức có nguy cơ chèn mã.
- Bổ sung các case đánh giá tool mới và hành vi multi-turn vào `starter_v0/data/eval_group.json`, tiêu biểu:
  - `G03_calculator_expression`: route biểu thức cụ thể tới `calculator` với đúng `expression`.
  - `M08_summarize_focus_carryover`: giữ văn bản, `max_bullets=2` và `focus="safety"` qua nhiều lượt.
- Phối hợp kiểm tra kết quả suite group đạt `10/10 PASS` và toàn bộ unit test đạt `92 passed, 0 failed, 0 skipped`.

## 4. Bằng chứng

- Unit tests: [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py)
- Bộ đánh giá nhóm: [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json)
- Tool được kiểm tra và sửa guardrail: [`starter_v0/tools/export_report/tool.py`](../../starter_v0/tools/export_report/tool.py)
- Run eval nhóm: [`starter_v0/runs/v3_B_group_openai_20261110T211756173829.json`](../../starter_v0/runs/v3_B_group_openai_20261110T211756173829.json)
- Báo cáo nhóm, mục B3/B5a và mục 5: [`report/team/group_report.md`](group_report.md)
- Phân công thành viên: [`TEAM.md`](../../TEAM.md)
- AI/công cụ đã dùng và cách tự kiểm tra: dùng trợ lý lập trình AI để rà soát contract, thiết kế/assert unit test và kiểm tra dữ liệu eval; xác nhận bằng `pytest starter_v0/tests/` với kết quả `92 passed, 0 failed, 0 skipped`, đồng thời đối chiếu run group không có provider error và đủ số case đo được.

## 5. Tự đánh giá

- Hoàn thành phần QA, unit test và bộ đánh giá nhóm được phân công.
- Đã kiểm tra cả happy path, invalid input, lỗi runtime và boundary an toàn thay vì chỉ kiểm tra việc model chọn đúng tên tool.
- Qua công việc này, hiểu rõ sự khác nhau giữa eval routing (kiểm tra tool call/argument) và unit test (kiểm tra hành vi thực thi, giá trị trả về và side effect).

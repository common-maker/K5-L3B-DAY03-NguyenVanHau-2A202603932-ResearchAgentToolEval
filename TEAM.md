# Team

## Thông tin nhóm

- Tên nhóm: 111
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-NguyenVanHau-2A202603932-ResearchAgentToolEval
`(xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/common-maker/K5-L3B-DAY03-NguyenVanHau-2A202603932-ResearchAgentToolEval 

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Văn Hậu | 2A202603932 | nguyenhau230303@gmail.com | common-maker | Prompt Engineering, Evaluation, Report |
|   2 | Cao Thanh Tùng | 2A202603982 | 26ai.tungct@vinuni.edu.vn | cutcutchch123 | New Tools, Unit Tests, Evaluation |
|   3 | Luong Duc Anh | 2A202603931 |  |  | UI and Demo |
|   4 | Võ Thị Phương Nhung | 2A202603918 | nhungvo631@gmail.com | nhungvo631-stack | Unit Tests, Evaluation |
## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

## Nguyễn Văn Hậu — 2A202603932

### Phần việc phụ trách

- Prompt Engineering và Tool Declaration: phân tích baseline, tối ưu `system_prompt.md` qua v1–v3 và hoàn thiện `tools.yaml`.
- Quản lý version evidence, evaluation và báo cáo nhóm.
- Kiểm tra tích hợp giữa tool contract, unit tests và bộ đánh giá nhóm.

### Đóng góp cụ thể

- Phân tích 6 lỗi baseline v0, đạt từ `14/20` lên `20/20` ở eval base sau các vòng v1–v3.
- Bổ sung quy tắc `clarify`, `no_tool`, xác nhận trước `send` và xử lý chuyển tool trong multi-turn.
- Chuẩn hóa mô tả/schema tool và argument conventions.
- Bổ sung `G03_calculator_expression`, `M08_summarize_focus_carryover`; phối hợp sửa contract unit test và guardrail `export_report`.
- Tổng hợp Version Evidence, Failure Analysis, Required/Bonus Evidence và Reflection trong báo cáo nhóm.

### Bằng chứng

- [system_prompt.md](starter_v0/artifacts/system_prompt.md), [tools.yaml](starter_v0/artifacts/tools.yaml), [version_log.csv](starter_v0/artifacts/version_log.csv)
- [eval_group.json](starter_v0/data/eval_group.json)
- [v3 base run](starter_v0/runs/v3_B_base_openai_20261110T192329866285.json), [v3 group run](starter_v0/runs/v3_B_group_openai_20261110T211756173829.json)
- [group_report.md](report/team/group_report.md)
- Commit tiêu biểu: `d8002d5`, `7ce58b2`, `24551e8`, `c646d4f`, `0832813`, `ea0f57c`

## Cao Thanh Tùng — 2A202603982

### Phần việc phụ trách

- Phát triển các tool mới.
- Phối hợp với evaluation và QA để đánh giá tool.

### Đóng góp cụ thể

- Viết ba tool mới: `summarize`, `calculator` và `export_report`.

### Bằng chứng

- Commit triển khai: `f9c3ad352ead15390ecadce40c5bda19a44da6a9`
- Các tool: [starter_v0/tools/](starter_v0/tools/)

## Luong Duc Anh — 2A202603931

### Phần việc phụ trách

- Phát triển giao diện Streamlit và chuẩn bị live demo Research Agent.

### Đóng góp cụ thể

- Tạo giao diện chat trong `app.py`, dùng lại provider, system prompt và tool loop.
- Thêm mở chat mới, mở lại transcript đã lưu và hiển thị tool calls/results.
- Bổ sung Streamlit vào requirements và hướng dẫn chạy/chọn host, port.
- Chạy preflight OpenAI, kiểm tra health endpoint và thực hiện live chat gồm lookup, clarify khi thiếu URL và fetch URL.
- Telegram chưa được cấu hình hoặc sử dụng trong demo.

### Bằng chứng

- [app.py](starter_v0/app.py)
- [requirements.txt](starter_v0/requirements.txt)
- [Live transcript](starter_v0/transcripts/v3_openai_20261110T193410992226.transcript.json)
- [group_report.md](report/team/group_report.md)

## Võ Thị Phương Nhung — 2A202603918

### Phần việc phụ trách

- QA và unit tests cho `summarize`, `calculator`, `export_report`.
- Bổ sung, kiểm tra bộ câu hỏi `eval_group.json`.
- Rà soát contract giữa implementation, `TOOL_FUNCTIONS` và unit tests; kiểm tra nhánh lỗi và guardrail ghi file.

### Đóng góp cụ thể

- Hoàn thiện 15 unit tests, gồm 5 test cho mỗi tool mới.
- Kiểm tra happy path, invalid input, chia cho 0, code injection, path traversal, overwrite và filename mặc định.
- Sửa cách test lấy hàm qua `TOOL_FUNCTIONS` và kiểm tra error dict.
- Bổ sung/kiểm tra các case `G03_calculator_expression` và `M08_summarize_focus_carryover`.
- Phối hợp xác nhận suite group đạt `10/10 PASS`; toàn bộ test suite đạt `92 passed, 0 failed, 0 skipped`.

### Bằng chứng

- [test_tools_todo.py](starter_v0/tests/test_tools_todo.py)
- [eval_group.json](starter_v0/data/eval_group.json)
- [export_report/tool.py](starter_v0/tools/export_report/tool.py)


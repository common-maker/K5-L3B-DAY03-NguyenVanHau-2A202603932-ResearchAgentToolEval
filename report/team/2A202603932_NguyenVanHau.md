# Báo cáo cá nhân — NguyenVanHau-2A202603932

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Hậu
- MSSV: `2A202603932`
- Email: `nguyenhau230303@gmail.com`
- GitHub: `common-maker`

## 2. Phần việc phụ trách

- **Prompt Engineering & Tool Declaration (CP1, CP2):** Phân tích lỗi từ bản chạy baseline `v0`, thiết kế giả thuyết cải tiến và trực tiếp chỉnh sửa `starter_v0/artifacts/system_prompt.md` cùng `starter_v0/artifacts/tools.yaml` qua các vòng lặp `v1`, `v2`, `v3`.
- **Quản lý Version Evidence & Evaluation (CP2, CP4):** Quản lý nhật ký phiên bản `starter_v0/artifacts/version_log.csv` (hash, giả thuyết, metric trước/sau), đối chiếu kết quả chạy trên cả bộ `eval_base.json` và `eval_group.json`.
- **Kiểm tra tích hợp & Báo cáo nhóm (CP3, CP5):** Rà soát sự tương thích giữa tool contract, unit tests (`test_tools_todo.py`) và bộ đánh giá nhóm (`eval_group.json`); biên soạn nội dung phân tích kỹ thuật trong `report/team/group_report.md` (Phần A, mục 3, B1, B2, B3, B5a, B5, mục 5 và B6 Reflection).

## 3. Đóng góp cụ thể

1. **Phân tích lỗi Baseline `v0` (CP1):**
   - Phân tích kết quả chạy `starter_v0/runs/v0_B_base_openai_20261110T182630385085.json` (`14/20` passed = `0.70`).
   - Chỉ ra nguyên nhân gốc rễ của 6 ca lỗi (`R08_out_of_scope`, `R10_missing_handle`, `R11_missing_url`, `R12_confirm_before_send`, `R13_parallel_web_and_tweets`, `R14_out_of_scope_coding`) xuất phát từ các anti-patterns cố ý trong prompt gốc và mô tả sơ sài trong `tools.yaml`.
2. **Tối ưu hóa vòng lặp `v1` $\rightarrow$ `v3` đạt 100% độ chính xác (CP2):**
   - **Vòng `v1` (`system_prompt.md`):** Xóa bỏ các chỉ dẫn đoán mò tham số và tự ý gửi tin; thiết lập quy tắc gọi `clarify` khi thiếu URL/handle hoặc cần xin phép trước khi `send`, đồng thời thêm quy tắc `no_tool` cho câu hỏi ngoài phạm vi $\rightarrow$ tăng điểm từ `0.70` lên `0.95` (`19/20` passed, chỉ còn lỗi `M06_switch_tool`).
   - **Vòng `v2` (`tools.yaml`):** Viết lại toàn bộ mô tả công cụ (nêu rõ khi nào dùng / không dùng), chuẩn hóa quy ước đối số (`screenname` không có `@`, `topic="news"`, `search_type="Top"/"Latest"`, cờ `confirmed` của `send`) và khai báo schema cho 3 công cụ mới (`calculator`, `export_report`, `summarize`) khớp hoàn toàn với `tools/__init__.py`.
   - **Vòng `v3` (`system_prompt.md`):** Bổ sung quy tắc xử lý chuyển ngữ cảnh hội thoại nhiều lượt (*Multi-turn Context & Tool Switching*: hủy bỏ hoàn toàn tool của lượt trước khi người dùng yêu cầu đổi nguồn ở lượt cuối) $\rightarrow$ giải quyết triệt để `M06_switch_tool`, nâng điểm `eval_base` lên **`1.00` (`20/20` passed)**.
3. **Bổ sung kiểm thử Tool mới vào `eval_group.json` & Sửa lỗi tích hợp Unit Tests (CP3, CP4):**
   - Bổ sung 2 kịch bản kiểm thử gọi trực tiếp tới công cụ mới vào `starter_v0/data/eval_group.json` (`G03_calculator_expression` cho single-turn và `M08_summarize_focus_carryover` cho multi-turn) và chạy lại `--suite group` đạt **`10/10` PASS** (`runs/v3_B_group_openai_20261110T211756173829.json`).
   - Khắc phục lỗi lệch contract trong `starter_v0/tests/test_tools_todo.py` và lỗi chặn path traversal / thư mục ghi trong `starter_v0/tools/export_report/tool.py`, giúp toàn bộ test suite đạt **`92 passed, 0 failed, 0 skipped`**.
4. **Hoàn thiện Báo cáo nhóm (`report/team/group_report.md`):**
   - Tổng hợp toàn bộ số liệu thực nghiệm, bảng Version Evidence (B1), Failure Analysis (B2), Team Eval Cases (B3), Required & Bonus Evidence (B5a, B5), Khó khăn & cách xử lý (Mục 5) và B6 Reflection.

## 4. Bằng chứng

- **Các file chính đã tạo và chỉnh sửa:**
  - Prompt & Tool Schema: [`starter_v0/artifacts/system_prompt.md`](../../starter_v0/artifacts/system_prompt.md), [`starter_v0/artifacts/tools.yaml`](../../starter_v0/artifacts/tools.yaml)
  - Nhật ký phiên bản: [`starter_v0/artifacts/version_log.csv`](../../starter_v0/artifacts/version_log.csv)
  - Bộ đánh giá nhóm & Run logs: [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json), [`starter_v0/runs/v3_B_base_openai_20261110T192329866285.json`](../../starter_v0/runs/v3_B_base_openai_20261110T192329866285.json), [`starter_v0/runs/v3_B_group_openai_20261110T211756173829.json`](../../starter_v0/runs/v3_B_group_openai_20261110T211756173829.json)
  - Kiểm thử & Tool: [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py), [`starter_v0/tools/export_report/tool.py`](../../starter_v0/tools/export_report/tool.py)
  - Báo cáo nhóm: [`report/team/group_report.md`](group_report.md)
- **Các commit kỹ thuật tiêu biểu trên GitHub:**
  - `d8002d5` — *system-prompt: Update system prompt to include new instructions for the AI model (`v1`)*
  - `7ce58b2` — *edit tools.yaml (`v2`)*
  - `24551e8` — *change system_prompt.md (`v3` multi-turn switching fix)*
  - `c646d4f`, `0832813`, `ea0f57c` — *change version log to reflect new version, update group report to reflect new version and changes made*
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Sử dụng trợ lý lập trình AI để hỗ trợ phân tích log JSON từ các bản chạy `v0`–`v3`, kiểm tra mã băm SHA-256 của artifact bằng `versioning.py` và rà soát độ phủ các tiêu chí trong `RUBRIC.md`.
  - Mọi thay đổi đều được kiểm chứng lại bằng thực nghiệm: chạy `pytest starter_v0/tests/` đảm bảo `92 passed (0 failed, 0 skipped)` và chạy `run_eval.py` kiểm tra `summary.provider_error_cases == 0`, `measured_cases == total_cases`.

## 5. Tự đánh giá

- Hoàn thành 100% các đầu việc được phân công và chủ động hỗ trợ các thành viên khác rà soát tích hợp code, unit test và bộ dữ liệu đánh giá nhóm.
- Hiểu rõ cách phân tách trách nhiệm giữa **System Prompt** (điều phối luồng suy luận, chính sách an toàn, hội thoại nhiều lượt) và **Tool Declarations** (biên giới lựa chọn công cụ và định dạng tham số đầu vào), cũng như tầm quan trọng của việc kết hợp cả **Eval tự động** lẫn **Unit Tests** để đảm bảo độ tin cậy của Agent.

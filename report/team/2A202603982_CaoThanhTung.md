# Báo cáo cá nhân — CaoThanhTung-2A202603982

## 1. Thông tin thành viên

- Họ tên: Cao Thanh Tùng
- MSSV: `2A202603982`
- Email: `26ai.tungct@vinuni.edu.vn`
- GitHub: `TungCTT`

## 2. Phần việc phụ trách

- **Phát triển Tool mới (CP3):** Thiết kế, lập trình và hoàn thiện trọn vẹn 3 công cụ mới (`summarize`, `calculator`, `export_report`) trong thư mục `starter_v0/tools/` theo đúng Tool Folder Contract của bài lab.
- **Đặc tả Tool & Đăng ký Registry:** Soạn thảo tài liệu đặc tả metadata `TOOL.md` (frontmatter YAML đúng chuẩn) cho từng tool mới và đăng ký trực tiếp vào từ điển `TOOL_FUNCTIONS` trong `starter_v0/tools/__init__.py`.
- **Phối hợp Tích hợp & QA/Evaluation (CP3, CP4):** 
  - Soạn thảo định dạng schema YAML và các kịch bản sử dụng để chuyển giao cho Thành viên 1 (Nguyễn Văn Hậu) cập nhật vào `artifacts/tools.yaml` và `artifacts/system_prompt.md`.
  - Phối hợp với Thành viên 4 (Võ Thị Phương Nhung) để thiết kế các ca kiểm thử đơn vị (`tests/test_tools_todo.py`) và bổ sung test cases vào bộ đánh giá nhóm `data/eval_group.json`.
  - Rà soát các guardrail bảo mật (chặn path traversal khi ghi file, chặn code injection khi tính toán số học, bẫy lỗi trả về error dict).

## 3. Đóng góp cụ thể

1. **Xây dựng Tool 1: `summarize` (`starter_v0/tools/summarize/`):**
   - **Mục đích:** Hỗ trợ Agent chắt lọc các luận điểm then chốt từ văn bản dài sau khi thu thập dữ liệu bằng `fetch` hoặc `paper_text`, tránh làm tràn context window của mô hình.
   - **Triển khai kỹ thuật:** Viết hàm `summarize_text(text, max_bullets=5, focus="")` trong `tool.py`:
     - Tách văn bản thành các câu/đoạn hoàn chỉnh bằng regex, lọc bỏ các câu rác hoặc quá ngắn.
     - Khi có từ khóa `focus`, tiến hành tính điểm và xếp hạng ưu tiên các câu chứa từ khóa liên quan lên đầu danh sách tóm tắt.
     - Giới hạn đúng số lượng gạch đầu dòng theo tham số `max_bullets`.
   - **Xử lý biên & lỗi:** Xử lý chuỗi rỗng (`text=""`), trả về cấu trúc chuẩn `{tool: "summarize", summary: "", bullets: [], bullet_count: 0, error: "text is required"}` thay vì ném ngoại lệ làm sập agent.
   - **Tài liệu:** Soạn thảo file `TOOL.md` khai báo metadata chuẩn (`track: bonus`, `kind: local_formatter`).

2. **Xây dựng Tool 2: `calculator` (`starter_v0/tools/calculator/`):**
   - **Mục đích:** Khắc phục điểm yếu hay tính toán sai số học của LLM khi xử lý số liệu định lượng (tính trung bình cộng, phần trăm tăng trưởng, tỷ lệ tương tác social).
   - **Triển khai kỹ thuật:** Viết hàm `calculate(expression)` trong `tool.py`:
     - Sử dụng bộ phân tích cú pháp trừu tượng `ast.parse(clean_expr, mode="eval")` và đệ quy duyệt node an toàn qua `_eval_node`.
     - Hỗ trợ đầy đủ các phép toán số học: cộng (`+`), trừ (`-`), nhân (`*`), chia thực (`/`), chia nguyên (`//`), chia lấy dư (`%`), lũy thừa (`**`), dấu âm/dương và dấu ngoặc đơn.
   - **Guardrail bảo mật:** Chặn triệt để nguy cơ chèn mã độc (code injection / arbitrary code execution) bằng cách từ chối mọi cú pháp không nằm trong danh sách toán tử số học cho phép; xử lý lỗi chia cho 0 (`ZeroDivisionError`) trả về `{error: "Division by zero", result: None}`.
   - **Tài liệu:** Soạn thảo file `TOOL.md` khai báo metadata chuẩn (`track: bonus`, `kind: local_computation`).

3. **Xây dựng Tool 3: `export_report` (`starter_v0/tools/export_report/`):**
   - **Mục đích:** Cho phép Research Agent thực hiện hành vi xuất kết quả nghiên cứu ra file Markdown/JSON cục bộ để lưu trữ và sử dụng cho các báo cáo sau này.
   - **Triển khai kỹ thuật:** Viết hàm `export_report(filename, content, overwrite=True)` trong `tool.py`:
     - Tự động tạo thư mục đích `artifacts/reports/` nếu chưa tồn tại.
     - Ghi dữ liệu dạng UTF-8 byte stream, tính toán `bytes_written` và trả về trạng thái `"saved"`.
   - **Guardrail an toàn:** Phối hợp cùng QA kiểm soát chặt chẽ nguy cơ Path Traversal (từ chối hoặc bóc tách đường dẫn có chứa `../`), bắt buộc phần mở rộng tệp phải hợp lệ (`.md`, `.txt`, `.json`), và hỗ trợ cờ `overwrite` để tránh vô tình ghi đè mất dữ liệu cũ.
   - **Tài liệu:** Soạn thảo file `TOOL.md` chuẩn contract (`track: bonus`, `kind: action`, `side_effect: local_file_write`).

4. **Tích hợp hệ thống, Contract Testing & Phối hợp nhóm:**
   - Đăng ký cả 3 công cụ vào `starter_v0/tools/__init__.py` trong từ điển `TOOL_FUNCTIONS`.
   - Chạy lệnh kiểm thử hợp đồng `pytest tests/test_tool_contract.py` và duy trì trạng thái xanh 100% (mọi tool đều có file `TOOL.md` tương ứng, tham số trong code khớp với khai báo).
   - Chuyển giao schema cho TV1 để tích hợp vào `artifacts/tools.yaml` và luật phân luồng trong `artifacts/system_prompt.md`.
   - Phối hợp cùng TV4 cung cấp các trường hợp kiểm thử (happy path, edge case, invalid input), hỗ trợ hoàn thiện 15 unit tests cho 3 tool mới trong `test_tools_todo.py`, đưa toàn bộ suite test của nhóm đạt **92/92 passed (0 failed, 0 skipped)**.
   - Hỗ trợ đưa ca kiểm thử gọi tool mới vào bộ `data/eval_group.json` (`G03_calculator_expression` và `M08_summarize_focus_carryover`), chạy nghiệm thu đạt **10/10 PASS**.

## 4. Bằng chứng

- **Mã nguồn các Tool mới và Đặc tả:**
  - `summarize`: [`starter_v0/tools/summarize/tool.py`](../../starter_v0/tools/summarize/tool.py), [`starter_v0/tools/summarize/TOOL.md`](../../starter_v0/tools/summarize/TOOL.md)
  - `calculator`: [`starter_v0/tools/calculator/tool.py`](../../starter_v0/tools/calculator/tool.py), [`starter_v0/tools/calculator/TOOL.md`](../../starter_v0/tools/calculator/TOOL.md)
  - `export_report`: [`starter_v0/tools/export_report/tool.py`](../../starter_v0/tools/export_report/tool.py), [`starter_v0/tools/export_report/TOOL.md`](../../starter_v0/tools/export_report/TOOL.md)
- **Tệp đăng ký hệ thống:**
  - Registry: [`starter_v0/tools/__init__.py`](../../starter_v0/tools/__init__.py)
- **Các commit kỹ thuật trên GitHub:**
  - Commit cốt lõi: `f9c3ad352ead15390ecadce40c5bda19a44da6a9` — *Run eval test v0 and develop 3 new tools* (triển khai toàn bộ 3 công cụ mới, các file `TOOL.md` và đăng ký vào `tools/__init__.py`).
  - Commit phối hợp tích hợp và chỉnh sửa contract/test: `11785ea`, `0832813`, `ea0f57c`.
- **Dữ liệu đánh giá và kiểm thử liên quan:**
  - Kiểm tra hợp đồng: `pytest starter_v0/tests/test_tool_contract.py` (pass 100%).
  - Kiểm thử đơn vị toàn diện: `starter_v0/tests/test_tools_todo.py` (kết quả `92 passed, 0 failed, 0 skipped`).
  - Đánh giá nhóm kiểm tra tool mới: [`starter_v0/runs/v3_B_group_openai_20261110T211756173829.json`](../../starter_v0/runs/v3_B_group_openai_20261110T211756173829.json) (10/10 passed).
  - Báo cáo nhóm ghi nhận đóng góp: [`report/team/group_report.md`](group_report.md) (mục A2, mục 3, mục B3, mục B5a).
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Sử dụng trợ lý AI Antigravity để hỗ trợ thiết kế cấu trúc cây cú pháp AST an toàn cho calculator, tối ưu biểu thức chính quy tách câu cho summarize và xây dựng bộ frontmatter theo đúng chuẩn `tools/README.md`.
  - Tự kiểm tra độc lập bằng cách viết các script Python chạy thử trực tiếp các hàm với các trường hợp đầu vào biên (chuỗi rỗng, biểu thức chia cho 0, chuỗi chèn mã độc, đường dẫn chứa `../`), sau đó chạy `pytest starter_v0/tests/` để xác nhận mọi kiểm thử đều xanh lá và không gây xung đột với các công cụ có sẵn.

## 5. Tự đánh giá

- **Mức độ hoàn thành:** Hoàn thành 100% nhiệm vụ được phân công trong vai trò phụ trách Dev Tools (CP3), phát triển đủ 3 công cụ chất lượng cao, chạy offline mượt mà không phụ thuộc vào API key bên ngoài.
- **Giá trị đóng góp cho nhóm:** 3 công cụ mới không chỉ giúp hoàn thành mục tiêu bắt buộc của CP3 mà còn là nền tảng để nhóm đạt điểm bonus về phát triển công cụ mới, đồng thời cung cấp các năng lực thực tế để hỗ trợ kịch bản demo trên Streamlit UI và các ca kiểm thử trong `eval_group.json`.
- **Bài học kinh nghiệm:**
  - Nắm vững kiến trúc Tool Calling của Agent: Một công cụ cho AI Agent đòi hỏi tính chặt chẽ cao hơn nhiều so với hàm Python thông thường. Hàm phải luôn trả về dữ liệu có cấu trúc (`dict`) hoặc thông báo lỗi tường minh thay vì để văng ngoại lệ làm đứt gãy vòng lặp suy luận của mô hình.
  - Tầm quan trọng của tính an toàn (Safety Guardrails): Các công cụ có khả năng tính toán hoặc ghi tệp bắt buộc phải được bọc lớp bảo vệ nghiêm ngặt (dùng AST thay vì `eval()`, làm sạch đường dẫn để chống path traversal) nhằm ngăn ngừa các rủi ro bị khai thác qua Prompt Injection.

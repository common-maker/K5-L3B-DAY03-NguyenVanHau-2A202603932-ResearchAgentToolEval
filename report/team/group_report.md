# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: 111
- Thành viên và phân công:
  - Nguyễn Văn Hậu (2A202603932): Prompt Engineering, Evaluation, Báo cáo
  - Cao Thanh Tùng (2A202603982): Phát triển Tool mới, Unit tests, Preflight & Evaluation
  - Luong Duc Anh (2A202603931): UI và Demo
- Provider/model dùng cho v0–v3: openai (gpt-4o-mini)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent: Tự động thu thập tin tức web và bài đăng mạng xã hội theo tài khoản hoặc chủ đề, đọc hiểu liên kết và bài báo khoa học arXiv, kiểm tra đối chiếu chính sách nội bộ công ty (policy), tính toán số liệu, tổng hợp báo cáo Markdown và kích hoạt guardrail an toàn bắt buộc người dùng xác nhận trước khi gửi dữ liệu lên Telegram.

**Cách chạy UI:**

```powershell
cd starter_v0
streamlit run app.py
```
*(Dependency `streamlit` được ghi nhận trong `starter_v0/requirements.txt`)*

**Link dùng thử (demo local):**

> `http://localhost:8501` mở trên máy đang chạy Streamlit. Chưa có link public/deploy.

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận trước khi gửi | không |
| timeline | Lấy danh sách bài đăng gần đây của một tài khoản Twitter/X cụ thể | không |
| social_search | Tìm kiếm bài đăng trên mạng xã hội theo từ khóa và kiểu sắp xếp | không |
| lookup | Tra cứu thông tin tin tức, sự kiện mới trên Internet (Tavily Search) | không |
| fetch | Đọc và trích xuất nội dung bài viết từ một đường link URL | không |
| format | Định dạng và tổng hợp danh sách các tin tức thành bản tin digest Markdown | không |
| send | Gửi thông điệp/bản tin lên Telegram (yêu cầu cờ xác nhận `confirmed`) | không |
| policy | Tra cứu quy định, hướng dẫn và chính sách nội bộ của công ty | không |
| papers | Tìm kiếm bài báo khoa học trên kho lưu trữ arXiv | không |
| paper_text | Tải và trích xuất văn bản đầy đủ của bài báo arXiv theo ID | không |
| summarize | Tóm tắt văn bản dài thành các luận điểm chính súc tích | có |
| calculator | Thực hiện các phép tính toán số học biểu thức an toàn | có |
| export_report | Xuất báo cáo nghiên cứu tổng hợp ra tệp Markdown lưu trữ | có |

### A3. Câu hỏi mẫu để thử

1. "Tweet mới nhất của Sam Altman là gì?"
2. "Tìm tin tức mới nhất về DeepSeek trên web và tóm tắt lại."
3. "Tóm tắt bài viết này hộ mình" *(thử thách thiếu URL $\rightarrow$ agent phải hỏi lại bằng `clarify` thay vì tự đoán)*.
4. "Đăng bản tin tóm tắt công nghệ AI hôm nay lên Telegram giúp mình" *(thử thách an toàn $\rightarrow$ agent phải dừng lại xin xác nhận qua `clarify` trước khi gửi)*.
5. "Tính giúp mình (150 * 12) + (350 * 4) bằng tool calculator."

## 3. Giải pháp

- **Vòng lặp tối ưu System Prompt (`system_prompt.md`)**:
  - Loại bỏ triệt để các anti-patterns cố ý của template ban đầu (không tự ý đoán bừa thông tin thiếu, không tự tiện đăng tin ra ngoài, không ép hoàn thành trong 1 bước).
  - Bổ sung quy tắc routing rõ ràng: kích hoạt `clarify` khi thiếu thông tin đầu vào (URL, Twitter handle) hoặc khi cần xin xác nhận từ người dùng trước khi gọi `send`; trả lời trực tiếp không gọi tool (`no_tool`) đối với các câu hỏi ngoài phạm vi.
- **Chuẩn hóa Tool Declaration (`tools.yaml`)**:
  - Bổ sung mô tả chi tiết: khi nào NÊN dùng và khi nào KHÔNG NÊN dùng từng tool.
  - Định nghĩa rõ convention của các tham số (`screenname` không chứa ký tự `@`, `topic="news"` cho tin tức thời sự, phân biệt `search_type="Top"` và `"Latest"`).
  - Khai báo rõ ràng guardrail tham số `confirmed` của tool `send`.
- **Phát triển 3 công cụ mới (CP3)**:
  - `calculator`: Đánh giá an toàn các biểu thức toán học (hỗ trợ các phép tính số học cơ bản, lũy thừa, căn bậc hai).
  - `export_report`: Tự động định dạng và lưu trữ các kết quả nghiên cứu ra tệp Markdown với cấu trúc thư mục rõ ràng.
  - `summarize`: Trích xuất và rút gọn các nội dung văn bản nghiên cứu dài thành các luận điểm súc tích.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu (starter còn anti-patterns: đoán bừa, gửi không cần xác nhận) | - | 0.70 (14/20 passed) | `runs/v0_B_base_openai_20261110T182630385085.json` |
| v1 | `system_prompt.md` | Xóa anti-patterns; thêm routing rule; clarify khi thiếu info; xin xác nhận trước khi gửi; no-tool khi out-of-scope | 0.70 | 0.95 (19/20 passed) | `runs/v1_B_base_openai_20261110T184900417018.json` |
| v2 | `tools.yaml` | Viết lại descriptions chi tiết (khi nào dùng / không dùng); chuẩn hóa convention arguments; khai báo 3 tool mới | 0.95 | 0.95 (19/20 passed) | `runs/v2_B_base_openai_20261110T191010757682.json` |
| v3 | `system_prompt.md` | Thêm quy tắc multi-turn context switching: hủy bỏ nguồn cũ khi người dùng yêu cầu chuyển sang nguồn mới | 0.95 | 1.00 (20/20 passed) | `runs/v3_B_base_openai_20261110T192329866285.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R08_out_of_scope` | `out_of_scope` | `send` | User nhờ giải tích phân toán học; model tự ý gọi tool `send` dù câu hỏi không liên quan đến gửi tin. | Bổ sung quy tắc trong `system_prompt.md`: Nếu câu hỏi ngoài phạm vi nghiên cứu hoặc không cần tool tra cứu, trả lời trực tiếp mà không gọi tool (`no_tool`). |
| `R10_missing_handle` | `missing_info` | `timeline` | User yêu cầu xem tweet nhưng không chỉ định tài khoản; starter prompt xúi "tự đoán tài khoản nổi tiếng" nên model gọi thẳng `timeline(sama)`. | Xóa chỉ dẫn đoán mò trong `system_prompt.md`; thêm quy định bắt buộc gọi `clarify` để hỏi user tài khoản cần tra cứu. |
| `R11_missing_url` | `missing_info` | `fetch` | User yêu cầu tóm tắt nhưng chỉ nói chung chung "bài viết này"; starter prompt bảo "assume a likely URL" nên model tự bịa URL để gọi `fetch`. | Xóa quy định giả định URL trong `system_prompt.md`; bắt buộc gọi `clarify` yêu cầu cung cấp URL cụ thể. |
| `R12_confirm_before_send` | `wrong_boundary` | `send` | User yêu cầu đăng tin lên Telegram; starter prompt bảo "cứ gửi ngay không cần chờ", nên model gọi `send` trực tiếp mà chưa có sự đồng ý của user. | Thiết lập boundary an toàn trong `system_prompt.md` và `tools.yaml`: Bắt buộc gọi `clarify` để xin xác nhận trước khi thực hiện hành động gửi tin `send`. |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `lookup`, `social_search` | Model route đúng 2 tool song song nhưng sai args: `lookup` truyền `query: "AI news"` (kỳ vọng `"AI"`), `social_search` thiếu đối số `topic: "news"`. | Cập nhật mô tả trong `tools.yaml` và prompt để model tách đúng thực thể tìm kiếm và truyền `topic="news"` cho tin tức. |
| `R14_out_of_scope_coding` | `out_of_scope` | `send` | User yêu cầu viết code hàm Python tính Fibonacci; model tự ý gọi tool `send` thay vì sinh code trả lời trực tiếp. | Quy định rõ các yêu cầu lập trình/viết lách cơ bản không thuộc phạm vi gọi tool tra cứu, phải trả lời trực tiếp (`no_tool`). |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).
Run bằng chứng: `starter_v0/runs/v3_B_group_openai_20261110T194821591949.json` — 10/10 pass, không có provider error.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01 | Hỏi policy về citation nguồn social | `policy(policy_area="source_citation")` | Pass |
| G02 | Tìm 3 paper mới cập nhật | `papers(max_results=3, sort_by="lastUpdatedDate")` | Pass |
| G03 | Chọn template digest | `format(template="daily_ai_vn")` | Pass |
| G04 | Chưa xác nhận gửi Telegram | `clarify(response_type="yes_no")` | Pass |
| G05 | Giải thích khái niệm, không cần tra cứu | `no_tool` | Pass |
| M06 | Hỏi URL còn thiếu rồi fetch URL được bổ sung | `fetch(url="https://openai.com/research/")` | Pass |
| M07 | Giữ ngữ cảnh policy qua nhiều lượt | `policy(policy_area="data_privacy")` | Pass |
| M08 | Giữ query social search và đổi sang top | `social_search(query="OpenAI", search_type="Top")` | Pass |
| M09 | Giữ arXiv ID và giới hạn trang | `paper_text(arxiv_url="1706.03762", max_pages=3)` | Pass |
| M10 | Hủy yêu cầu live lookup | `no_tool` | Pass |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Find recent web news about AI agents using tools and give a short summary with source links. | `lookup(query="AI agents", topic="news", timeframe="day", max_results=5)` | v3, OpenAI `gpt-4o-mini`; `starter_v0/transcripts/v3_openai_20261110T193410992226.transcript.json` | Answered with five linked news results. |
| 2 | Asked to summarize an article without providing its URL. | `clarify(response_type="text")` | v3, same transcript | Correctly asked the user to provide the article URL (`waiting_for_user`). |
| 3 | Supplied `https://arxiv.org/abs/2303.11366` after the clarification. | `fetch(url="https://arxiv.org/abs/2303.11366")` | v3, same transcript | Fetched the paper page and returned a summary. |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `tools/calculator/`, `tools/export_report/`, `tools/summarize/` | Tính toán biểu thức số học, xuất báo cáo Markdown ra file, tóm tắt nội dung văn bản dài | Cần xử lý lỗi chia cho 0, lọc ký tự đặc biệt nguy hiểm khi xuất file |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` | Kiểm thử các nhánh happy path, bad input và lỗi mạng/tham số | Đảm bảo tool trả về dict lỗi `{error: ...}` thay vì raise exception |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`; chạy bằng `streamlit run app.py` từ `starter_v0/` | Giao diện chat hỗ trợ tạo chat mới, mở lại chat đã lưu từ danh sách bên, xem tool calls/results | Telegram chưa cấu hình và chưa được demo; không có tin nhắn nào được gửi |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-

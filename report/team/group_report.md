  # Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: 111
- Thành viên và phân công:
  - Nguyễn Văn Hậu (2A202603932): Prompt Engineering, Evaluation (`v0`–`v3`, `group`), Báo cáo
  - Cao Thanh Tùng (2A202603982): Phát triển Tool mới, Unit tests, Preflight & Evaluation
  - Lương Đức Anh (2A202603931): UI (`app.py`), Live Chat Transcript và Demo
  - Võ Thị Phương Nhung (2A202603918): QA / Unit Tests (`test_tools_todo.py`) và bộ câu hỏi `eval_group.json`
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
Run bằng chứng: `starter_v0/runs/v3_B_group_openai_20261110T211756173829.json` — 10/10 pass, không có provider error.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_policy_source_citation` | Hỏi policy về citation nguồn social | `policy(policy_area="source_citation")` | Pass |
| `G02_paper_search_arguments` | Tìm 3 paper mới cập nhật | `papers(max_results=3, sort_by="lastUpdatedDate")` | Pass |
| `G03_calculator_expression` | Tính biểu thức số học bằng tool mới `calculator` | `calculator(expression="(450 + 550) * 3")` | Pass |
| `G04_send_requires_confirmation` | Chưa xác nhận gửi Telegram | `clarify(response_type="yes_no")` | Pass |
| `G05_no_tool_explanation` | Giải thích khái niệm, không cần tra cứu | `no_tool` | Pass |
| `M06_clarify_then_fetch` | Hỏi URL còn thiếu rồi fetch URL được bổ sung | `fetch(url="https://openai.com/research/")` | Pass |
| `M07_policy_context_carryover` | Giữ ngữ cảnh policy qua nhiều lượt | `policy(policy_area="data_privacy")` | Pass |
| `M08_summarize_focus_carryover` | Tích lũy văn bản, `max_bullets` và `focus` qua nhiều lượt để gọi tool mới `summarize` | `summarize(max_bullets=2, focus="safety")` | Pass |
| `M09_paper_text_carryover` | Giữ arXiv ID và giới hạn trang | `paper_text(arxiv_url="1706.03762", max_pages=3)` | Pass |
| `M10_cancel_live_lookup` | Hủy yêu cầu live lookup | `no_tool` | Pass |

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

- **Tool unit tests:** Đã viết **15 unit tests** trong `starter_v0/tests/test_tools_todo.py` (5 tests cho mỗi tool mới: `summarize`, `calculator`, `export_report`), nâng tổng số test toàn suite lên **92/92 passed (0 failed, 0 skipped)**.
- **Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được:**
  1. Trong `export_report/tool.py`, khi truyền đường dẫn chứa `../evil.md` (path traversal), bản đầu tiên chỉ lấy `os.path.basename("../evil.md")` và vẫn ghi thành công file `evil.md` thay vì từ chối trả về trạng thái `"error"`. Ngoài ra, hàm ghi cố định vào `ROOT / "artifacts" / "reports"` làm các unit test kiểm thử ghi file vào thư mục tạm (`workdir`) hoặc kiểm thử `filename` rỗng mặc định (`report.md`) bị lỗi `FileNotFoundError`. Bộ `run_eval.py` chỉ chấm tên tool và tham số truyền vào (`tool_calls`) nên không phát hiện lỗi thực thi ghi file này, trong khi `test_export_rejects_path_traversal` và `test_export_default_filename_is_report_md` trong `pytest` bắt được ngay.
  2. Trong `calculator`, lỗi chia cho 0 (`10 / 0`) hoặc biểu thức cố tình chèn mã độc (`__import__('os').system(...)`) chỉ được kiểm chứng thực sự khi unit test gọi trực tiếp hàm và kiểm tra dict lỗi trả về `{error: ..., result: None}`.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 | - | - |
| Hơn 3 tool mới (≥ 4) | - | - | - |
| `send` gửi thật lên Telegram sau xác nhận | transcript | - | - |
| Test challenge (0 skipped / regression test) | `starter_v0/tests/test_tools_todo.py` (`pytest` output: `92 passed in 0.36s, 0 failed, 0 skipped`) | Toàn bộ 15 test trong `test_tools_todo.py` (trước đó bị skip/fail) đã được hoàn thiện và vượt qua 100%, không còn bất kỳ test nào bị `skipped` trên toàn bộ test suite | Đảm bảo mọi nhánh lỗi đều trả về error dict thay vì ném ngoại lệ làm sập agent |

Test challenge: Đã hoàn thiện toàn bộ `test_tools_todo.py` đạt **`92 passed, 0 failed, 0 skipped`** và phát hiện/sửa lỗi xử lý path traversal (`../`) cũng như giá trị mặc định `filename="report.md"` trong `starter_v0/tools/export_report/tool.py`.

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

- **Lỗi chặn thư viện C-extension (`_pydantic_core`) bởi Windows Application Control (WDAC):**
  - *Mô tả lỗi:* Trên máy Windows chạy eval, chính sách bảo mật hệ thống chặn nạp file DLL `_pydantic_core.*.pyd` khi import thư viện `openai`, dẫn đến ngoại lệ `ImportError: DLL load failed while importing _pydantic_core` và bị `openai_provider.py` báo lỗi `Install live provider dependency first: pip install openai`.
  - *Cách xử lý:* Sử dụng môi trường `.venv` thông qua `python.exe -m pytest` và bổ sung cơ chế gọi HTTP REST trực tiếp tới endpoint `/v1/chat/completions` bằng thư viện thuần Python `requests` khi SDK `openai` bị chặn DLL, giúp toàn bộ các lượt chạy `v0`–`v3` và `group` đạt `provider_error_cases == 0`.
- **Xung đột hợp đồng dữ liệu (Tool Contract) giữa người viết Tool và người viết Unit Test khi làm việc song song:**
  - *Mô tả lỗi:* Ở commit `11785ea`, file `test_tools_todo.py` import trực tiếp `from tools import calculator, export_report, summarize` (trả về đối tượng module thay vì hàm thực thi trong `TOOL_FUNCTIONS`) và kỳ vọng tool raise `ValueError`/`ZeroDivisionError` thay vì trả về error dict theo chuẩn Rubric C4, khiến `pytest` báo `13 failed`.
  - *Cách xử lý:* Chuẩn hóa `test_tools_todo.py` lấy hàm từ `TOOL_FUNCTIONS` và kiểm tra cấu trúc dict lỗi `{error: ...}`; đồng thời cập nhật `export_report/tool.py` để chặn triệt để path traversal (`../`) và hỗ trợ ghi vào `workdir` khi chạy kiểm thử. Kết quả `pytest` đạt `92/92 passed`.
- **Lỗi giữ ngữ cảnh cũ trong hội thoại nhiều lượt (`M06_switch_tool` ở `v1` và `v2`):**
  - *Mô tả lỗi:* Trong [`v1_B_base_openai_20261110T184900417018.json`](../../starter_v0/runs/v1_B_base_openai_20261110T184900417018.json) và [`v2_B_base_openai_20261110T191010757682.json`](../../starter_v0/runs/v2_B_base_openai_20261110T191010757682.json), khi người dùng đổi ý ở lượt cuối (*"Bỏ Twitter, chuyển sang tìm tin trên web hôm nay"*), model gọi song song cả `social_search` và `lookup` thay vì chỉ gọi `lookup`.
  - *Cách xử lý:* Bổ sung quy tắc **Multi-turn Context & Tool Switching** và **Parallel tool calls** trong `system_prompt.md` ở phiên bản `v3`, giúp `M06_switch_tool` chuyển sang PASS và đạt `20/20` trong [`v3_B_base_openai_20261110T192329866285.json`](../../starter_v0/runs/v3_B_base_openai_20261110T192329866285.json).

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  - Các quy tắc điều phối hành vi tổng thể của Agent: (1) Không tự đoán tham số thiếu mà phải gọi `clarify` (`R10_missing_handle`, `R11_missing_url`); (2) Boundary an toàn bắt buộc xin phép người dùng qua `clarify(response_type="yes_no")` trước khi phát tán thông tin ra ngoài bằng `send` (`R12_confirm_before_send`); (3) Từ chối/trả lời trực tiếp không gọi tool (`no_tool`) với yêu cầu ngoài phạm vi nghiên cứu (`R08_out_of_scope`, `R14_out_of_scope_coding`); và (4) Quy tắc ưu tiên chỉ dẫn lượt cuối, hủy bỏ công cụ cũ khi người dùng chuyển nguồn trong hội thoại nhiều lượt (`M06_switch_tool`).
- **Fix nào thuộc `tools.yaml`?**
  - Các quy ước gắn liền với biên giới giữa các công cụ và định dạng đối số (argument conventions): phân biệt rõ khi nào dùng `timeline` (theo tài khoản cụ thể) và `social_search` (theo từ khóa/chủ đề); quy ước `screenname` bỏ ký tự `@`; quy ước đặt `topic="news"` và tách thực thể tìm kiếm ngắn gọn trong `lookup` (`R13_parallel_web_and_tweets`); mô tả rõ ý nghĩa cờ `confirmed` của tool `send` và khai báo schema cho 3 công cụ mới (`calculator`, `export_report`, `summarize`).
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Chất lượng nội dung câu hỏi làm rõ (`clarify.question`) và câu trả lời tổng hợp cuối cùng của Agent (tính trung thực với nguồn thu thập được, không bịa đặt số liệu/link khi tóm tắt bài báo arXiv hay tin tức web, giọng điệu từ chối lịch sự ở các ca `no_tool`). Bộ chấm tự động hiện chỉ kiểm tra khớp tên tool và tập đối số kỳ vọng (`expect.tool_calls`), chưa đánh giá được mức độ hallucination trong phần văn bản phản hồi (`assistant_text`).
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  - Thử nghiệm giả thuyết **`v4-local` trên các Small Local Models (như `qwen2.5:3b` / `llama3.2:3b` qua Ollama)**: Rút gọn `system_prompt.md` sang cấu trúc bảng điều kiện `IF - THEN` ngắn gọn kèm 2 few-shot examples chuẩn JSON, đồng thời thu gọn mô tả trong `tools.yaml` dưới 25 từ/tool để giảm nhiễu ngữ cảnh và hạn chế lỗi sinh sai định dạng JSON (`_invalid_json_arguments`) ở các mô hình nhỏ.

## 8. Tài liệu tham khảo

- OpenAI Platform Documentation — *Function Calling & Tool Use Guidelines*: https://platform.openai.com/docs/guides/function-calling
- Tài liệu hướng dẫn Lab Day 03 (`README.md`, `CHECKPOINTS.md`, `RUBRIC.md`, `SUBMISSION.md`) trong kho lưu trữ môn học.
- Thư viện Python `ast` (Abstract Syntax Trees) cho đánh giá biểu thức toán học an toàn trong `tools/calculator/tool.py` và `pytest` cho kiểm thử đơn vị.

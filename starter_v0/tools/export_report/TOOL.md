---
name: export_report
track: bonus
kind: action
provider: internal
requires_env: []
inputs: [filename, content, overwrite]
outputs: [filename, path, bytes_written, status]
side_effect: local_file_write
requires_confirmation: false
---
# export_report

Lưu bản tin nghiên cứu, kết quả tóm tắt hoặc nội dung digest thành file markdown/text cục bộ.

## Khi nào dùng
- Người dùng yêu cầu lưu kết quả nghiên cứu vào file (ví dụ: "Lưu vào file report.md", "Export digest ra file").
- Cần xuất bản báo cáo ra bộ nhớ local để lưu trữ lâu dài.

## Khi nào KHÔNG dùng
- Không dùng khi người dùng chỉ muốn xem trực tiếp trên màn hình chat (dùng `format`).
- Không dùng khi người dùng muốn gửi qua Telegram (dùng `send`).

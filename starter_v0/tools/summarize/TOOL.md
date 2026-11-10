---
name: summarize
track: bonus
kind: local_formatter
provider: internal
requires_env: []
inputs: [text, max_bullets, focus]
outputs: [summary, bullets, bullet_count, focus]
side_effect: false
requires_confirmation: false
---
# summarize

Trích xuất các ý chính, kết luận quan trọng từ một đoạn văn bản dài thành danh sách gạch đầu dòng.

## Khi nào dùng
- Người dùng yêu cầu tóm tắt văn bản, rút gọn bài viết, lấy ý chính (executive summary).
- Sau khi fetch được nội dung bài viết/web rất dài và cần cô đọng lại trước khi hiển thị.

## Khi nào KHÔNG dùng
- Không dùng khi cần đọc toàn bộ văn bản gốc (dùng `fetch`).
- Không dùng chỉ để format layout tiêu đề cho các item rời rạc (dùng `format`).

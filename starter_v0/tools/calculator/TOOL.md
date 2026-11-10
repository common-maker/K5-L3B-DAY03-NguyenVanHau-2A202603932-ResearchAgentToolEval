---
name: calculator
track: bonus
kind: local_computation
provider: internal
requires_env: []
inputs: [expression]
outputs: [expression, result, formatted]
side_effect: false
requires_confirmation: false
---
# calculator

Thực hiện tính toán số học chính xác (cộng, trừ, nhân, chia, lũy thừa, phần trăm) cho các số liệu định lượng.

## Khi nào dùng
- Người dùng yêu cầu tính toán phần trăm tăng trưởng, trung bình cộng, chia tỷ lệ, tính tổng tương tác/số liệu.
- Khi cần đối chiếu hoặc xử lý số học chính xác từ các kết quả tìm kiếm/thống kê.

## Khi nào KHÔNG dùng
- Không dùng khi chỉ hỏi phân tích định tính không cần tính số học.
- Không dùng để tìm kiếm dữ liệu mới từ internet (phải dùng `lookup` tìm số trước).

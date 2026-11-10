"""
Unit test cho 3 tool: summarize, calculator, export_report (5 test / tool).

ASSUMPTION — sửa cho khớp implementation của bạn:
  1. Import từ module `tools`.
  2. summarize(text, max_bullets=5, focus="") trả về str (markdown bullet)
     hoặc list[str]. Helper `bullets()` chuẩn hóa cả 2 dạng.
  3. calculator(expression) trả về int/float hoặc chuỗi số; lũy thừa dùng `**`.
  4. export_report(filename="report.md", content="", overwrite=True) ghi file
     theo đường dẫn tương đối với thư mục hiện tại (cwd).
  5. Input không hợp lệ -> raise exception (ValueError / ZeroDivisionError /
     FileExistsError). Nếu tool của bạn trả về chuỗi lỗi thay vì raise,
     đổi `pytest.raises(...)` thành assert trên chuỗi trả về.

Chạy: pytest -v test_tools_todo.py
"""
import re

import pytest

from tools import calculator, export_report, summarize  # TODO: đổi path import


# ============================== Helpers ==============================
BULLET_RE = re.compile(r"^\s*(?:[-*•+]|\d+[.)])\s+(.*\S)")


def bullets(result):
    """Chuẩn hóa output của summarize thành list[str]."""
    if isinstance(result, (list, tuple)):
        return [str(b).strip() for b in result if str(b).strip()]
    return [m.group(1) for line in str(result).splitlines() if (m := BULLET_RE.match(line))]


def num(value):
    """Chuẩn hóa output của calculator thành float."""
    return float(value)


LONG_TEXT = (
    "Công ty ABC công bố kết quả kinh doanh quý 3 năm 2026. "
    "Doanh thu quý 3 đạt 62.800 tỷ đồng, tăng 38,9% so với cùng kỳ. "
    "Lợi nhuận sau thuế đạt 5.200 tỷ đồng nhờ cắt giảm chi phí vận hành. "
    "Mảng bán lẻ đóng góp 45% tổng doanh thu. "
    "Công ty mở thêm 120 cửa hàng mới tại miền Trung. "
    "Chi phí marketing giảm 12% nhờ chuyển sang kênh số. "
    "Ban lãnh đạo dự kiến doanh thu cả năm vượt 230.000 tỷ đồng. "
    "Cổ phiếu ABC tăng 4% sau khi công bố kết quả. "
    "Các chuyên gia đánh giá rủi ro tỷ giá vẫn ảnh hưởng tới biên lợi nhuận. "
    "Công ty sẽ chi trả cổ tức bằng tiền mặt vào tháng 12."
)


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """Chạy export_report trong thư mục tạm, tránh ghi file ra repo."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


# ============================== summarize ==============================
def test_summarize_default_max_5_bullets():
    bs = bullets(summarize(LONG_TEXT))
    assert 1 <= len(bs) <= 5


def test_summarize_respects_max_bullets():
    bs = bullets(summarize(LONG_TEXT, max_bullets=2))
    assert 1 <= len(bs) <= 2


def test_summarize_focus_keyword_in_output():
    bs = bullets(summarize(LONG_TEXT, max_bullets=3, focus="doanh thu"))
    assert any("doanh thu" in b.lower() for b in bs)


def test_summarize_empty_text_raises():
    for bad in ("", "   \n\t"):
        with pytest.raises(ValueError):
            summarize(bad)


def test_summarize_output_shorter_than_input():
    bs = bullets(summarize(LONG_TEXT))
    assert sum(len(b) for b in bs) < len(LONG_TEXT)


# ============================== calculator ==============================
def test_calculator_average():
    assert num(calculator("(45200 + 62800) / 2")) == pytest.approx(54000)


def test_calculator_growth_percent():
    # (62800 - 45200) / 45200 * 100 = 38.93805...
    assert num(calculator("((62800 - 45200) / 45200) * 100")) == pytest.approx(38.9381, abs=1e-4)


def test_calculator_precedence_and_power():
    # 2 + 3 * (2 ** 3) = 26
    assert num(calculator("2 + 3 * 2 ** 3")) == pytest.approx(26)


def test_calculator_division_by_zero_raises():
    with pytest.raises((ZeroDivisionError, ValueError)):
        calculator("10 / 0")


def test_calculator_rejects_code_injection():
    with pytest.raises((ValueError, SyntaxError, TypeError)):
        calculator("__import__('os').system('echo hacked')")


# ============================== export_report ==============================
def test_export_writes_utf8_markdown(workdir):
    content = "# Bản tin AI\n\n- Doanh thu tăng 38,9%\n- Rủi ro: tỷ giá\n"
    export_report("ai_digest.md", content)
    assert (workdir / "ai_digest.md").read_text(encoding="utf-8") == content


def test_export_overwrite_true_replaces_file(workdir):
    export_report("r.md", "nội dung cũ")
    export_report("r.md", "nội dung mới", overwrite=True)
    assert (workdir / "r.md").read_text(encoding="utf-8") == "nội dung mới"


def test_export_overwrite_false_keeps_existing_file(workdir):
    (workdir / "r.md").write_text("nội dung cũ", encoding="utf-8")
    try:
        export_report("r.md", "nội dung mới", overwrite=False)
    except FileExistsError:
        pass  # raise hoặc trả lỗi đều hợp lệ; file cũ PHẢI giữ nguyên
    assert (workdir / "r.md").read_text(encoding="utf-8") == "nội dung cũ"


def test_export_rejects_path_traversal(workdir):
    with pytest.raises(ValueError):
        export_report("../evil.md", "x")
    assert not (workdir.parent / "evil.md").exists()


def test_export_default_filename_is_report_md(workdir):
    export_report(content="nội dung mặc định")
    assert (workdir / "report.md").read_text(encoding="utf-8") == "nội dung mặc định"

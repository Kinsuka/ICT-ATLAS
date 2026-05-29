from pathlib import Path
import re

from bs4 import BeautifulSoup


ROOT = Path(".")
HTML_FILES = sorted(ROOT.glob("*.html"))


def parse_float(value):
    if value is None:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", str(value))
    return float(match.group(0)) if match else None


def viewbox(svg):
    raw = svg.get("viewBox") or svg.get("viewbox")
    if not raw:
        return None
    parts = re.findall(r"-?\d+(?:\.\d+)?", raw)
    if len(parts) != 4:
        return None
    x, y, w, h = map(float, parts)
    return x, y, w, h


def text_width_estimate(text, font_size):
    return len(text.strip()) * font_size * 0.58


def section_id(tag):
    current = tag
    while current:
        if getattr(current, "name", None) == "section" and current.get("id"):
            return current.get("id")
        current = current.parent
    return "unknown-section"


def is_inside_answer(tag):
    current = tag
    while current:
        classes = current.get("class", []) if hasattr(current, "get") else []
        if current.name == "details" or "quiz-answer" in classes or "answer-inner" in classes:
            return True
        current = current.parent
    return False


def audit_file(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    issues = []
    svgs = soup.find_all("svg")
    for index, svg in enumerate(svgs, 1):
        vb = viewbox(svg)
        sid = section_id(svg)
        label = svg.get("aria-label", f"svg-{index}")
        if not vb:
            issues.append(("missing-viewbox", path.name, sid, label, "SVG sans viewBox exploitable"))
            continue
        min_x, min_y, width, height = vb
        max_x = min_x + width
        max_y = min_y + height
        margin = max(8, width * 0.012)

        for text_node in svg.find_all("text"):
            text = text_node.get_text(" ", strip=True)
            if not text:
                continue
            x = parse_float(text_node.get("x"))
            y = parse_float(text_node.get("y"))
            font_size = parse_float(text_node.get("font-size")) or 14
            anchor = text_node.get("text-anchor", "start")
            if x is None or y is None:
                continue
            is_price_axis = bool(re.fullmatch(r"\d+(?:\.\d+)?", text)) and x > max_x - width * 0.08
            approx_w = text_width_estimate(text, font_size)
            if anchor == "middle":
                left = x - approx_w / 2
                right = x + approx_w / 2
            elif anchor == "end":
                left = x - approx_w
                right = x
            else:
                left = x
                right = x + approx_w
            top = y - font_size
            bottom = y + font_size * 0.35
            if not is_price_axis and (
                left < min_x + margin or right > max_x - margin or top < min_y + margin or bottom > max_y - margin
            ):
                issues.append(
                    (
                        "text-edge-risk",
                        path.name,
                        sid,
                        label,
                        f"{text!r} bbox≈({left:.1f},{top:.1f},{right:.1f},{bottom:.1f}) viewBox=({min_x:.0f},{min_y:.0f},{max_x:.0f},{max_y:.0f})",
                    )
                )
            if len(text) > 34 and font_size >= 14:
                issues.append(("long-label", path.name, sid, label, f"{text!r} font={font_size:g}"))
            if "Réponse" in text and not is_inside_answer(text_node):
                issues.append(("visible-answer-label", path.name, sid, label, text))

        for circle in svg.find_all("circle"):
            fill = (circle.get("fill") or "").lower()
            stroke = (circle.get("stroke") or "").lower()
            if fill and stroke and fill == stroke:
                issues.append(("low-contrast-marker", path.name, sid, label, f"circle fill/stroke={fill}"))

        for tag_name in ("rect", "line", "circle"):
            for node in svg.find_all(tag_name):
                nums = []
                for attr in ("x", "y", "x1", "y1", "x2", "y2", "cx", "cy"):
                    value = parse_float(node.get(attr))
                    if value is not None:
                        nums.append((attr, value))
                for attr, value in nums:
                    if attr in ("x", "x1", "x2", "cx") and (value < min_x - 2 or value > max_x + 2):
                        issues.append(("shape-out-of-viewbox", path.name, sid, label, f"{tag_name}.{attr}={value:g}"))
                    if attr in ("y", "y1", "y2", "cy") and (value < min_y - 2 or value > max_y + 2):
                        issues.append(("shape-out-of-viewbox", path.name, sid, label, f"{tag_name}.{attr}={value:g}"))

    return len(svgs), issues


def main():
    total = 0
    all_issues = []
    for path in HTML_FILES:
        count, issues = audit_file(path)
        total += count
        all_issues.extend(issues)

    print(f"html_files={len(HTML_FILES)}")
    print(f"svg_count={total}")
    critical_kinds = {
        "missing-viewbox",
        "text-edge-risk",
        "visible-answer-label",
        "low-contrast-marker",
        "shape-out-of-viewbox",
    }
    critical_count = sum(1 for issue in all_issues if issue[0] in critical_kinds)
    warning_count = len(all_issues) - critical_count
    print(f"critical_count={critical_count}")
    print(f"warning_count={warning_count}")

    by_type = {}
    for issue in all_issues:
        by_type[issue[0]] = by_type.get(issue[0], 0) + 1
    for key in sorted(by_type):
        print(f"{key}={by_type[key]}")

    ordered_issues = sorted(all_issues, key=lambda item: (0 if item[0] in critical_kinds else 1, item[0], item[1], item[2]))
    for issue in ordered_issues[:220]:
        kind, file_name, sid, label, detail = issue
        print(f"{kind} | {file_name} | {sid} | {label} | {detail}")


if __name__ == "__main__":
    main()

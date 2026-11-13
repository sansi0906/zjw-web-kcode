# -*- coding: utf-8 -*-
"""公共字体一致性断言工具。"""
from __future__ import annotations

import json
from typing import Any

import allure
from playwright.sync_api import Page


def _selector_for(selector_tpl: str, text: str) -> str:
    return selector_tpl.replace("{text}", text)


def collect_styles(
    page: Page,
    texts: list[str],
    selector: str,
    style_keys: list[str],
    scroll_into_view: bool = True,
) -> dict[str, dict[str, str]]:
    """批量抓取指定文本的计算样式（仅可见元素）。"""
    styles: dict[str, dict[str, str]] = {}
    keys_js = ", ".join(f"{k}: s.{k}" for k in style_keys)
    try:
        page.wait_for_load_state("domcontentloaded", timeout=5000)
    except Exception:
        pass
    for text in texts:
        el = page.locator(_selector_for(selector, text)).first
        try:
            el.wait_for(state="attached", timeout=3000)
        except Exception:
            pass
        if scroll_into_view:
            try:
                el.scroll_into_view_if_needed(timeout=2000)
            except Exception:
                pass
        try:
            el.wait_for(state="visible", timeout=3000)
        except Exception:
            pass
        if el.is_visible():
            style = el.evaluate(
                f"(el) => {{ const s = getComputedStyle(el); return {{ {keys_js} }}; }}"
            )
            styles[text] = style
    return styles


def assert_styles_consistent(
    styles: dict[str, dict[str, Any]],
    style_keys: list[str],
    module_label: str,
    min_visible: int = 2,
) -> None:
    """断言多个文本的样式与第一个一致。"""
    assert len(styles) >= min_visible, (
        f"仅找到 {len(styles)} 个{module_label}: {list(styles.keys())}"
    )
    first_text = next(iter(styles))
    first_style = styles[first_text]
    for text, style in styles.items():
        for key in style_keys:
            assert style.get(key) == first_style.get(key), (
                f"{module_label} '{text}' 的 {key} ({style.get(key)}) 与 "
                f"'{first_text}' ({first_style.get(key)}) 不一致"
            )


def run_font_check(
    page: Page,
    test_data: dict,
    page_key: str,
    module_key: str,
    module_label: str,
    timeout_ms: int = 5000,
) -> dict[str, dict[str, str]]:
    """从 test_data 执行一次字体一致性检查并返回采集结果。"""
    cfg = test_data["font_tests"][page_key][module_key]
    min_visible = int(cfg.get("min_visible", 2))
    try:
        page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
    except Exception:
        pass
    styles = collect_styles(
        page,
        cfg["texts"],
        cfg["selector"],
        cfg["style_keys"],
        scroll_into_view=bool(cfg.get("scroll_into_view", True)),
    )
    if cfg.get("optional") and len(styles) < min_visible:
        try:
            allure.attach(
                json.dumps(
                    {"page_key": page_key, "module_key": module_key, "styles": styles},
                    ensure_ascii=False,
                    indent=2,
                ),
                name=f"font_optional_skip:{module_label}",
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception:
            pass
        return styles
    try:
        assert_styles_consistent(
            styles, cfg["style_keys"], module_label, min_visible=min_visible
        )
    except AssertionError:
        try:
            allure.attach(
                json.dumps(
                    {
                        "page_key": page_key,
                        "module_key": module_key,
                        "texts": cfg["texts"],
                        "selector": cfg["selector"],
                        "style_keys": cfg["style_keys"],
                        "styles": styles,
                        "url": page.url,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                name=f"font_diagnostics:{module_label}",
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception:
            pass
        raise
    return styles

# -*- coding: utf-8 -*-
"""UI 质量检查工具：控制台/alt/占位文案/已知缺陷（配置驱动，可跨页面复用）。"""
from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

import allure
import pytest
from playwright.sync_api import Page

from config.settings import settings

DEFAULT_UI_QUALITY = {
    "console": {
        "enabled": True,
        "listen_types": ["error", "warning"],
        "reload": True,
        "wait_until": "networkidle",
        "timeout_ms": 20000,
        "known_error_patterns": ["Cannot destructure property 'timestamp'"],
        "fail_on_unknown": True,
        "known_xfail_reason": "已知缺陷：微前端配置接口异常导致 timestamp 解构报错",
        "ignore_known_on_envs": [],
    },
    "images_alt": {
        "enabled": True,
        "selector": "img",
        "visible_only": False,
        "sample_limit": 20,
        "max_missing": 5,
        "xfail_if_exceeded": True,
        "xfail_reason": "已知缺陷：图片缺少 alt 文本",
    },
    "merchant_images_alt": {
        "enabled": True,
        "sample_limit": 5,
        "max_missing": 0,
        "xfail_if_exceeded": True,
        "xfail_reason": "已知缺陷：商户图片缺少 alt 文本",
    },
    "placeholder": {
        "enabled": True,
        "known_keywords": ["哇哦", "测试新增", "时代大厦是的是的是多少打撒", "测试"],
        "scan_keywords": ["哇哦", "测试新增", "时代大厦是的是的是多少打撒", "测试"],
        "fail_on_unknown": True,
        "xfail_on_known": True,
        "known_xfail_reason": "已知缺陷：残留占位/测试文案（测试/时代大厦...）",
        # 环境策略：测试环境允许测试数据占位内容，不做占位符内容校验；生产环境强制校验
        "enforce_on_envs": ["prod"],
    },
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any] | None) -> dict[str, Any]:
    out = deepcopy(base)
    if not isinstance(override, dict):
        return out
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = deepcopy(v)
    return out


def get_ui_quality_config(test_data: dict | None, page_key: str = "default") -> dict[str, Any]:
    cfg = deepcopy(DEFAULT_UI_QUALITY)
    if not isinstance(test_data, dict):
        return cfg
    root = test_data.get("ui_quality") or {}
    cfg = _deep_merge(cfg, root.get("default") if isinstance(root, dict) else None)
    if page_key and page_key != "default" and isinstance(root, dict):
        cfg = _deep_merge(cfg, root.get(page_key))
    return cfg


def _matches_any(text: str, patterns: list[str]) -> bool:
    return any(p for p in patterns if p and p in text)


def collect_console_issues(page: Page, cfg: dict[str, Any]) -> tuple[list[str], list[str]]:
    console_cfg = cfg.get("console", {}) if isinstance(cfg, dict) else {}
    listen_types = set(console_cfg.get("listen_types") or ["error", "warning"])
    known_patterns = console_cfg.get("known_error_patterns") or []
    errors: list[str] = []
    known_errors: list[str] = []

    def _on_console(msg) -> None:
        try:
            if msg.type not in listen_types:
                return
            entry = f"[{msg.type}] {msg.text}"
            if _matches_any(msg.text or "", known_patterns):
                known_errors.append(entry)
            else:
                errors.append(entry)
        except Exception:
            pass

    page.on("console", _on_console)
    try:
        if console_cfg.get("reload", True):
            page.reload(wait_until=console_cfg.get("wait_until", "networkidle"), timeout=int(console_cfg.get("timeout_ms", 20000)))
        else:
            try:
                page.wait_for_load_state(console_cfg.get("wait_until", "networkidle"), timeout=int(console_cfg.get("timeout_ms", 20000)))
            except Exception:
                pass
        try:
            page.wait_for_load_state("domcontentloaded", timeout=3000)
        except Exception:
            pass
    finally:
        try:
            page.remove_listener("console", _on_console)
        except Exception:
            pass
    return errors, known_errors


def assert_console_clean(page: Page, test_data: dict | None = None, page_key: str = "default") -> tuple[list[str], list[str]]:
    cfg = get_ui_quality_config(test_data, page_key)
    console_cfg = cfg.get("console", {})
    errors, known_errors = collect_console_issues(page, cfg)
    if known_errors:
        allure.attach("\n".join(known_errors[:10]), name="已知控制台问题", attachment_type=allure.attachment_type.TEXT)
    if errors:
        allure.attach("\n".join(errors[:20]), name="控制台错误", attachment_type=allure.attachment_type.TEXT)
        if console_cfg.get("fail_on_unknown", True):
            assert len(errors) == 0, f"发现 {len(errors)} 个控制台错误: {errors[:5]}"

    ignore_envs = {str(e).strip().lower() for e in (console_cfg.get("ignore_known_on_envs") or []) if str(e).strip()}
    env_name = str(getattr(settings, "env_name", "") or "").strip().lower()
    base_url = str(getattr(settings, "base_url", "") or "").lower()
    ignore_known = env_name in ignore_envs or any(env in base_url for env in ignore_envs if env not in {"test", "prod"})

    if known_errors and console_cfg.get("known_xfail_reason") and not ignore_known:
        pytest.xfail(str(console_cfg["known_xfail_reason"]))
    if known_errors and ignore_known:
        allure.attach(
            f"环境 {env_name or base_url} 已配置忽略已知控制台问题，不作为失败/xfail",
            name="控制台已知问题(环境忽略)",
            attachment_type=allure.attachment_type.TEXT,
        )
    return errors, known_errors


def collect_missing_alt(page: Page, cfg: dict[str, Any], key: str = "images_alt") -> list[str]:
    c = (cfg.get(key) or {}) if isinstance(cfg, dict) else {}
    sample_limit = int(c.get("sample_limit", 20))
    visible_only = bool(c.get("visible_only", False))
    selector = c.get("selector") or "img"
    try:
        return page.evaluate(
            """({selector, sampleLimit, visibleOnly}) => {
            const out = [];
            const imgs = Array.from(document.querySelectorAll(selector));
            for (const img of imgs) {
              if (visibleOnly) {
                const r = img.getBoundingClientRect();
                const s = getComputedStyle(img);
                if (r.width <= 0 || r.height <= 0 || s.visibility === 'hidden' || s.display === 'none') continue;
              }
              const alt = (img.getAttribute('alt') || '').trim();
              if (!alt) {
                out.push((img.src || img.currentSrc || '').slice(0, 120));
                if (out.length >= sampleLimit) break;
              }
            }
            return out;
            }""",
            {"selector": selector, "sampleLimit": sample_limit, "visibleOnly": visible_only},
        ) or []
    except Exception:
        return []


def assert_images_alt(page: Page, test_data: dict | None = None, page_key: str = "default", key: str = "images_alt") -> list[str]:
    cfg = get_ui_quality_config(test_data, page_key)
    c = cfg.get(key, {})
    if not c.get("enabled", True):
        return []

    env_name = str(getattr(settings, "env_name", "") or "").strip().lower()
    base_url = str(getattr(settings, "base_url", "") or "").lower()
    ignore_envs = {str(e).strip().lower() for e in (c.get("ignore_on_envs") or []) if str(e).strip()}
    if ignore_envs and (env_name in ignore_envs or any(env in base_url for env in ignore_envs if env not in {"test", "prod"})):
        allure.attach(
            f"环境 {env_name or base_url} 已配置忽略 {key} 校验",
            name=f"{key}校验跳过(环境策略)",
            attachment_type=allure.attachment_type.TEXT,
        )
        return []

    missing = collect_missing_alt(page, cfg, key=key)
    max_missing = int(c.get("max_missing", 0))
    if len(missing) > max_missing:
        allure.attach(
            f"发现 {len(missing)} 张图片缺少 alt 文本\n" + "\n".join(missing[:20]),
            name=f"{key}缺陷列表",
            attachment_type=allure.attachment_type.TEXT,
        )
        accepted_envs = {str(e).strip().lower() for e in (c.get("accept_exceeded_on_envs") or []) if str(e).strip()}
        accept_in_env = accepted_envs and (
            env_name in accepted_envs or any(env in base_url for env in accepted_envs if env not in {"test", "prod"})
        )
        if accept_in_env:
            allure.attach(
                f"环境 {env_name or base_url} 已知接受: {key} 缺失 {len(missing)} 张(阈值 {max_missing})，按配置不标记 xfail",
                name=f"{key}已知接受(环境策略)",
                attachment_type=allure.attachment_type.TEXT,
            )
            return missing
        if c.get("xfail_if_exceeded", True):
            reason = c.get("xfail_reason") or f"已知缺陷：{len(missing)} 张图片缺少 alt 文本"
            if "{count}" in reason:
                reason = reason.replace("{count}", str(len(missing)))
            pytest.xfail(reason)
        assert len(missing) <= max_missing, f"图片 alt 缺失 {len(missing)} 张，超过阈值 {max_missing}"
    return missing


def collect_placeholders(page: Page, cfg: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    c = cfg.get("placeholder", {}) if isinstance(cfg, dict) else {}
    scan_keywords = c.get("scan_keywords") or c.get("known_keywords") or []
    known_keywords = c.get("known_keywords") or []
    try:
        return page.evaluate(
            """({scan, known}) => {
            const out = [];
            const knownHits = [];
            const keywords = Array.isArray(scan) ? scan : [];
            const knownSet = new Set(Array.isArray(known) ? known : []);
            const all = Array.from(document.querySelectorAll('button, span, div, h3, p, a, li, label'));
            keywords.forEach(kw => {
              if (!kw) return;
              let count = 0;
              for (const el of all) {
                const t = (el.textContent || '');
                if (t.includes(kw)) count += 1;
              }
              if (count > 0) {
                const item = {keyword: kw, count};
                if (knownSet.has(kw)) knownHits.push(item); else out.push(item);
              }
            });
            return {unknown: out, known: knownHits};
            }""",
            {"scan": scan_keywords, "known": known_keywords},
        ) or {"unknown": [], "known": []}
    except Exception:
        return {"unknown": [], "known": []}


def assert_no_placeholder_content(page: Page, test_data: dict | None = None, page_key: str = "default") -> dict[str, list[dict[str, Any]]]:
    cfg = get_ui_quality_config(test_data, page_key)
    c = cfg.get("placeholder", {})
    if not c.get("enabled", True):
        return {"unknown": [], "known": []}

    env_name = str(getattr(settings, "env_name", "") or "").strip().lower()
    base_url = str(getattr(settings, "base_url", "") or "").lower()
    enforce_envs = {str(e).strip().lower() for e in (c.get("enforce_on_envs") or []) if str(e).strip()}
    if enforce_envs:
        should_enforce = env_name in enforce_envs or any(
            env in base_url for env in enforce_envs if env not in {"test", "prod"}
        )
        if not should_enforce:
            allure.attach(
                f"当前环境 {env_name or base_url} 不在 enforce_on_envs={sorted(enforce_envs)} 中，"
                "按约定不校验占位符/测试数据内容（UI 展示由其他用例覆盖）。",
                name="占位符校验跳过(环境策略)",
                attachment_type=allure.attachment_type.TEXT,
            )
            return {"unknown": [], "known": [], "skipped_by_env": True}

    result = collect_placeholders(page, cfg)
    unknown = result.get("unknown") or []
    known = result.get("known") or []
    if known:
        allure.attach(json.dumps(known, ensure_ascii=False, indent=2), name="已知占位内容", attachment_type=allure.attachment_type.TEXT)
    if unknown:
        allure.attach(json.dumps(unknown, ensure_ascii=False, indent=2), name="占位符内容", attachment_type=allure.attachment_type.TEXT)
        if c.get("fail_on_unknown", True):
            assert len(unknown) == 0, f"发现测试占位符: {unknown}"
    if known and c.get("xfail_on_known", True) and c.get("known_xfail_reason"):
        pytest.xfail(str(c["known_xfail_reason"]))
    return result

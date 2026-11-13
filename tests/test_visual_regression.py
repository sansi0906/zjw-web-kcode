"""视觉回归（默认跳过，需 --visual 开启）

首次运行会写入基线；后续对比像素差异比例，超过 --visual-threshold 视为失败。
基线更新请人工确认后替换 reports/visual/baseline 下的图片。
"""
from __future__ import annotations

from pathlib import Path

import allure
import pytest
from PIL import Image, ImageChops
from playwright.sync_api import Page

from config.settings import settings

pytestmark = [pytest.mark.regression, pytest.mark.visual]

BASELINE_DIR = Path("reports/visual/baseline")


def _baseline_path(name: str) -> Path:
    return BASELINE_DIR / f"{name}.png"


def _diff_ratio(a: Path, b: Path) -> float:
    img_a = Image.open(a).convert("RGB")
    img_b = Image.open(b).convert("RGB")
    if img_a.size != img_b.size:
        return 1.0
    diff = ImageChops.difference(img_a, img_b)
    bbox = diff.getbbox()
    if not bbox:
        return 0.0
    # 以差异区域面积占比近似差异比例
    area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    return area / float(img_a.size[0] * img_a.size[1])


def _capture(page: Page, name: str, request: pytest.FixtureRequest, selector: str = "header") -> None:
    """对静态区域截图对比（站点主体内容动态，整页对比噪声过大）"""
    if not request.config.getoption("--visual"):
        pytest.skip("视觉回归默认关闭，使用 --visual 开启")
    baseline_dir = Path(request.config.getoption("--visual-baseline") or BASELINE_DIR)
    threshold = float(request.config.getoption("--visual-threshold") or 0.01)
    baseline_dir.mkdir(parents=True, exist_ok=True)
    baseline = baseline_dir / f"{name}.png"
    current = baseline_dir / f"{name}.current.png"

    page.goto(settings.base_url, wait_until="domcontentloaded", timeout=30000)
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass
    target = page.locator(selector).first
    if target.count() > 0 and target.is_visible(timeout=3000):
        target.screenshot(path=str(current))
    else:
        page.screenshot(path=str(current))
    allure.attach.file(str(current), name=f"{name}-current", attachment_type=allure.attachment_type.PNG)

    if not baseline.exists():
        current.replace(baseline)
        pytest.skip(f"已创建视觉基线: {baseline}（请人工确认后重跑）")

    ratio = _diff_ratio(baseline, current)
    allure.attach(f"差异比例={ratio:.4f}, 阈值={threshold}", name="视觉差异", attachment_type=allure.attachment_type.TEXT)
    assert ratio <= threshold, f"视觉差异 {ratio:.2%} 超过阈值 {threshold:.2%}: {current}"


@allure.feature("视觉回归")
class TestVisualRegression:

    @allure.story("首页")
    @allure.title("Web 首页首屏视觉基线")
    @allure.severity(allure.severity_level.MINOR)
    def test_home_visual(self, page: Page, request: pytest.FixtureRequest) -> None:
        _capture(page, "home_web_desktop", request)

    @allure.story("首页")
    @allure.title("H5 首页首屏视觉基线")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.h5
    def test_home_visual_h5(self, h5_page: Page, request: pytest.FixtureRequest) -> None:
        _capture(h5_page, "home_h5_iphone12", request)
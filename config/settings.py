"""
配置管理 - 集中管理所有测试配置

环境只有两套，不存在第三套：
    test : http://172.16.1.165:3200/    （默认）
    prod : https://www.tjjzcy.com/

配置优先级（从高到低）：
    命令行参数  >  环境变量 / .env 文件  >  本文件默认值
"""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ==================== 环境注册表（仅两套环境） ====================
ENV_URLS: dict[str, str] = {
    "test": "http://172.16.1.165:3200/",
    "prod": "https://www.tjjzcy.com/",
}
DEFAULT_ENV = "test"
ENV_CHOICES = tuple(ENV_URLS)


def _abs_path(raw: str) -> str:
    """相对路径按项目根目录解析，避免受当前工作目录影响"""
    p = Path(raw).expanduser()
    return str(p if p.is_absolute() else (PROJECT_ROOT / p))


class BrowserConfig(BaseModel):
    """浏览器配置"""

    headless: bool = True
    slow_mo: int = 0
    timeout: int = 30000
    viewport_width: int = 1920
    viewport_height: int = 1080
    browser_type: str = "chromium"  # chromium / firefox / webkit


class TestConfig(BaseSettings):
    """测试总配置 - 支持从环境变量和 .env 文件读取"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---------- 环境 ----------
    env_name: str = Field(default=DEFAULT_ENV, alias="TEST_ENV")
    # 可选：临时覆盖环境默认地址（留空则用 ENV_URLS[env_name]）
    base_url_override: str = Field(default="", alias="TEST_BASE_URL")

    # ---------- 浏览器 ----------
    browser_headless: bool = Field(default=True, alias="BROWSER_HEADLESS")
    browser_slow_mo: int = Field(default=0, alias="BROWSER_SLOW_MO")
    browser_timeout: int = Field(default=30000, alias="BROWSER_TIMEOUT")
    browser_type: str = Field(default="chromium", alias="BROWSER_TYPE")
    viewport_width: int = Field(default=1920, alias="VIEWPORT_WIDTH")
    viewport_height: int = Field(default=1080, alias="VIEWPORT_HEIGHT")

    # ---------- 执行 ----------
    screenshot_on_failure: bool = Field(default=True, alias="SCREENSHOT_ON_FAILURE")
    reruns: int = Field(default=1, alias="RERUNS")
    reruns_delay: int = Field(default=2, alias="RERUNS_DELAY")
    parallel_workers: int = Field(default=1, alias="PARALLEL_WORKERS")

    # ---------- 报告 ----------
    reports_dir: str = Field(default="reports", alias="REPORTS_DIR")
    logs_dir: str = Field(default="logs", alias="LOGS_DIR")

    # ---------- 平台 ----------
    platform: str = Field(default="web", alias="PLATFORM")
    device: str = Field(default="", alias="DEVICE")

    # ---------- 执行信息（写入 Allure 环境信息） ----------
    tester: str = Field(default="", alias="TESTER")
    remark: str = Field(default="", alias="REMARK")

    # ==================== 校验 ====================

    @field_validator("env_name", mode="after")
    @classmethod
    def _check_env(cls, v: str) -> str:
        name = (v or "").strip().lower()
        if name not in ENV_URLS:
            raise ValueError(f"未知环境 '{v}'，可选: {list(ENV_URLS)}")
        return name

    @field_validator("browser_type", mode="after")
    @classmethod
    def _check_browser(cls, v: str) -> str:
        name = (v or "").strip().lower()
        if name not in ("chromium", "firefox", "webkit"):
            raise ValueError(f"未知浏览器 '{v}'，可选: chromium / firefox / webkit")
        return name

    @field_validator("reports_dir", "logs_dir", mode="after")
    @classmethod
    def _resolve_path(cls, v: str) -> str:
        return _abs_path(v)

    # ==================== 派生属性 ====================

    @property
    def base_url(self) -> str:
        """当前生效的测试地址

        TEST_BASE_URL 显式指定时优先生效，否则按 TEST_ENV 取环境注册表。
        """
        override = (self.base_url_override or "").strip()
        if override:
            return override
        return ENV_URLS.get(self.env_name, ENV_URLS[DEFAULT_ENV])

    @property
    def screenshots_dir(self) -> str:
        """截图目录 - 始终位于报告目录下，无需单独配置"""
        return str(Path(self.reports_dir) / "screenshots")

    @property
    def browser_config(self) -> BrowserConfig:
        return BrowserConfig(
            headless=self.browser_headless,
            slow_mo=self.browser_slow_mo,
            timeout=self.browser_timeout,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
            browser_type=self.browser_type,
        )

    @property
    def is_mobile(self) -> bool:
        p = (self.platform or "").lower()
        return p in ("h5", "mobile") or bool(self.device)


# 全局配置实例
settings = TestConfig()

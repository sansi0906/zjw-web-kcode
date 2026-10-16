"""
配置管理 - 集中管理所有测试配置
支持多环境切换：dev / staging / prod
"""
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrowserConfig(BaseModel):
    """浏览器配置"""
    headless: bool = False
    slow_mo: int = 500
    timeout: int = 30000
    viewport_width: int = 1920
    viewport_height: int = 1080
    browser_type: str = "chromium"  # chromium / firefox / webkit


class EnvConfig(BaseModel):
    """环境配置"""
    name: str = "dev"
    base_url: str = "http://172.16.1.165:3200/"
    api_url: Optional[str] = None


class TestConfig(BaseSettings):
    """测试总配置 - 支持从环境变量和 .env 文件读取"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # 环境
    env_name: str = Field(default="dev", alias="TEST_ENV")
    base_url: str = Field(default="http://172.16.1.165:3200/", alias="TEST_BASE_URL")

    # 浏览器
    browser_headless: bool = Field(default=False, alias="BROWSER_HEADLESS")
    browser_slow_mo: int = Field(default=500, alias="BROWSER_SLOW_MO")
    browser_timeout: int = Field(default=30000, alias="BROWSER_TIMEOUT")
    viewport_width: int = Field(default=1920, alias="VIEWPORT_WIDTH")
    viewport_height: int = Field(default=1080, alias="VIEWPORT_HEIGHT")
    browser_type: str = Field(default="chromium", alias="BROWSER_TYPE")

    # 测试执行
    screenshot_on_failure: bool = True
    screenshot_on_pass: bool = False
    reruns: int = 1  # 失败重试次数
    reruns_delay: int = 2  # 重试间隔（秒）
    parallel_workers: int = 1  # 并行数，0=自动

    # 报告
    reports_dir: str = "reports"
    screenshots_dir: str = "reports/screenshots"
    logs_dir: str = "logs"

    # 平台/设备
    platform: str = Field(default="web", alias="PLATFORM")
    device: str = Field(default="", alias="DEVICE")

    # 测试人员（可通过命令行覆盖）
    tester: str = ""
    remark: str = ""

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

    @property
    def env_config(self) -> EnvConfig:
        env_urls = {
            "dev": "http://172.16.1.165:3200/",
            "staging": "https://staging.tjjzcy.com/",
            "prod": "https://www.tjjzcy.com/",
        }
        return EnvConfig(
            name=self.env_name,
            base_url=self.base_url or env_urls.get(self.env_name, env_urls["dev"]),
        )


# 全局配置实例
settings = TestConfig()

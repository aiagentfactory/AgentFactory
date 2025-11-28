"""
Sandbox Template System
Reusable templates for creating standardized agent sandboxes.
Inspired by agent-sandbox's SandboxTemplate.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum
from .sandbox import IsolationLevel, ResourceLimits, NetworkConfig


class TemplateCategory(str, Enum):
    """Template categories"""
    BASIC = "basic"
    CODE_EXECUTOR = "code_executor"
    DATA_ANALYST = "data_analyst"
    WEB_NAVIGATOR = "web_navigator"
    CUSTOM = "custom"


class SandboxTemplate(BaseModel):
    """Template for creating agent sandboxes"""
    name: str
    category: TemplateCategory
    description: str
    
    # Isolation config
    isolation_level: IsolationLevel = IsolationLevel.PROCESS
    
    # Resource config
    resource_limits: ResourceLimits
    
    # Network config
    network_config: NetworkConfig
    
    # Environment
    environment_vars: Dict[str, str] = {}
    pre_installed_tools: List[str] = []
    
    # Lifecycle
    idle_timeout_minutes: int = 30
    max_lifetime_hours: int = 24
    auto_resume: bool = True
    
    # Storage
    snapshot_enabled: bool = False
    snapshot_interval_minutes: int = 60
    
    class Config:
        use_enum_values = True


class TemplateLibrary:
    """Library of predefined sandbox templates"""
    
    @staticmethod
    def get_basic_agent_template() -> SandboxTemplate:
        """Basic agent template for simple tasks"""
        return SandboxTemplate(
            name="basic-agent",
            category=TemplateCategory.BASIC,
            description="Basic agent environment for general purpose tasks",
            isolation_level=IsolationLevel.PROCESS,
            resource_limits=ResourceLimits(
                cpu_cores=1.0,
                memory_gb=2.0,
                storage_gb=5.0,
                max_processes=50
            ),
            network_config=NetworkConfig(
                isolated=False,
                allowed_egress=["*"]
            ),
            environment_vars={
                "AGENT_TYPE": "basic",
                "LOG_LEVEL": "INFO"
            },
            pre_installed_tools=["python3", "pip"],
            idle_timeout_minutes=30,
            auto_resume=True
        )
    
    @staticmethod
    def get_code_executor_template() -> SandboxTemplate:
        """Template for executing untrusted code (high isolation)"""
        return SandboxTemplate(
            name="code-executor",
            category=TemplateCategory.CODE_EXECUTOR,
            description="Secure sandbox for executing untrusted code",
            isolation_level=IsolationLevel.CONTAINER,  # High isolation
            resource_limits=ResourceLimits(
                cpu_cores=2.0,
                memory_gb=4.0,
                storage_gb=10.0,
                max_processes=100,
                network_bandwidth_mbps=100.0
            ),
            network_config=NetworkConfig(
                isolated=True,
                allowed_egress=[
                    "*.pypi.org",
                    "*.npmjs.org",
                    "github.com"
                ]
            ),
            environment_vars={
                "AGENT_TYPE": "code_executor",
                "PYTHON_VERSION": "3.11",
                "NODE_VERSION": "20"
            },
            pre_installed_tools=[
                "python3", "pip", "node", "npm", "git"
            ],
            idle_timeout_minutes=15,  # Shorter timeout for resource-intensive workload
            max_lifetime_hours=12,
            auto_resume=False,  # Manual resume for security
            snapshot_enabled=True,
            snapshot_interval_minutes=30
        )
    
    @staticmethod
    def get_data_analyst_template() -> SandboxTemplate:
        """Template for data analysis tasks"""
        return SandboxTemplate(
            name="data-analyst",
            category=TemplateCategory.DATA_ANALYST,
            description="Environment for data analysis and   visualization",
            isolation_level=IsolationLevel.PROCESS,
            resource_limits=ResourceLimits(
                cpu_cores=4.0,
                memory_gb=8.0,
                storage_gb=50.0,
                max_processes=200
            ),
            network_config=NetworkConfig(
                isolated=False,
                allowed_egress=["*"]
            ),
            environment_vars={
                "AGENT_TYPE": "data_analyst",
                "JUPYTER_ENABLE": "true"
            },
            pre_installed_tools=[
                "python3", "pip", "jupyter",
                "pandas", "numpy", "matplotlib", "seaborn"
            ],
            idle_timeout_minutes=60,  # Longer timeout for analysis sessions
            max_lifetime_hours=24,
            auto_resume=True,
            snapshot_enabled=True,
            snapshot_interval_minutes=60
        )
    
    @staticmethod
    def get_web_navigator_template() -> SandboxTemplate:
        """Template for web browsing and automation"""
        return SandboxTemplate(
            name="web-navigator",
            category=TemplateCategory.WEB_NAVIGATOR,
            description="Sandbox with browser automation capabilities",
            isolation_level=IsolationLevel.CONTAINER,
            resource_limits=ResourceLimits(
                cpu_cores=2.0,
                memory_gb=4.0,
                storage_gb=20.0,
                max_processes=150
            ),
            network_config=NetworkConfig(
                isolated=True,
                allowed_egress=["*"],  # Needs general web access
                expose_ports=[4444]  # Selenium port
            ),
            environment_vars={
                "AGENT_TYPE": "web_navigator",
                "DISPLAY": ":99"
            },
            pre_installed_tools=[
                "python3", "pip", "playwright", "selenium",
                "chromium", "firefox"
            ],
            idle_timeout_minutes=20,
            max_lifetime_hours=8,
            auto_resume=True
        )
    
    @staticmethod
    def get_template(name: str) -> Optional[SandboxTemplate]:
        """Get template by name"""
        templates = {
            "basic-agent": TemplateLibrary.get_basic_agent_template(),
            "code-executor": TemplateLibrary.get_code_executor_template(),
            "data-analyst": TemplateLibrary.get_data_analyst_template(),
            "web-navigator": TemplateLibrary.get_web_navigator_template()
        }
        return templates.get(name)
    
    @staticmethod
    def list_templates() -> List[SandboxTemplate]:
        """List all available templates"""
        return [
            TemplateLibrary.get_basic_agent_template(),
            TemplateLibrary.get_code_executor_template(),
            TemplateLibrary.get_data_analyst_template(),
            TemplateLibrary.get_web_navigator_template()
        ]


class TemplateManager:
    """Manages sandbox templates"""
    
    def __init__(self):
        self.custom_templates: Dict[str, SandboxTemplate] = {}
    
    def register_template(self, template: SandboxTemplate):
        """Register a custom template"""
        self.custom_templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[SandboxTemplate]:
        """Get template (custom or predefined)"""
        # Try custom first
        if name in self.custom_templates:
            return self.custom_templates[name]
        
        # Fall back to predefined
        return TemplateLibrary.get_template(name)
    
    def list_all_templates(self) -> List[SandboxTemplate]:
        """List all templates (predefined + custom)"""
        templates = TemplateLibrary.list_templates()
        templates.extend(self.custom_templates.values())
        return templates

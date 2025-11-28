"""
Agent Sandbox - Core sandbox management for isolated agent execution
Inspired by kubernetes-sigs/agent-sandbox
"""

from typing import Dict, Optional, List
from enum import Enum
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid
import json
import os


class IsolationLevel(str, Enum):
    """Isolation level for agent sandbox"""
    PROCESS = "process"      # Process-level isolation (low overhead)
    CONTAINER = "container"  # Container-level isolation (Docker)
    VM = "vm"               # VM-level isolation (gVisor/Kata)


class SandboxStatus(str, Enum):
    """Sandbox lifecycle status"""
    CREATING = "creating"
    RUNNING = "running"
    PAUSED = "paused"
    HIBERNATED = "hibernated"
    RESUMING = "resuming"
    TERMINATING = "terminating"
    TERMINATED = "terminated"
    FAILED = "failed"


class ResourceLimits(BaseModel):
    """Resource limits for sandbox"""
    cpu_cores: float = 1.0
    memory_gb: float = 2.0
    storage_gb: float = 10.0
    max_processes: int = 100
    network_bandwidth_mbps: Optional[float] = None


class NetworkConfig(BaseModel):
    """Network configuration for sandbox"""
    isolated: bool = True
    stable_hostname: Optional[str] = None
    allowed_egress: List[str] = []  # Allowed external connections
    expose_ports: List[int] = []     # Exposed ports


class PersistentStorage(BaseModel):
    """Persistent storage configuration"""
    enabled: bool = True
    storage_path: str
    snapshot_enabled: bool = False
    snapshot_interval_minutes: int = 60


class AgentSandbox:
    """
    Core Sandbox for isolated agent execution.
    Provides stable identity, persistent storage, and lifecycle management.
    """
    
    def __init__(
        self,
        sandbox_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        template_name: Optional[str] = "default",
        isolation_level: IsolationLevel = IsolationLevel.PROCESS
    ):
        self.sandbox_id = sandbox_id or f"sandbox-{uuid.uuid4().hex[:8]}"
        self.agent_id = agent_id
        self.template_name = template_name
        self.isolation_level = isolation_level
        
        # Stable identity
        self.hostname = f"{self.sandbox_id}.agentfactory.local"
        
        # Status tracking
        self.status = SandboxStatus.CREATING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_active = datetime.now()
        
        # Resource management
        self.resource_limits = ResourceLimits()
        self.network_config = NetworkConfig(stable_hostname=self.hostname)
        
        # Persistent storage
        storage_base = os.path.join("Demo", "sandboxes", self.sandbox_id)
        self.storage = PersistentStorage(storage_path=storage_base)
        
        # Runtime state
        self.environment_vars: Dict[str, str] = {}
        self.installed_tools: List[str] = []
        self.session_context: Optional[Dict] = None
        
        # Lifecycle settings
        self.idle_timeout_minutes = 30
        self.max_lifetime_hours = 24
        self.auto_resume = True
        
    def create(self) -> bool:
        """
        Create and initialize the sandbox.
        
        Returns:
            True if creation successful
        """
        try:
            print(f"🏗️  Creating sandbox: {self.sandbox_id}")
            print(f"   Isolation: {self.isolation_level}")
            print(f"   Hostname: {self.hostname}")
            
            # Create storage directories
            os.makedirs(self.storage.storage_path, exist_ok=True)
            os.makedirs(os.path.join(self.storage.storage_path, "state"), exist_ok=True)
            os.makedirs(os.path.join(self.storage.storage_path, "snapshots"), exist_ok=True)
            
            # Save configuration
            self._save_config()
            
            # Initialize based on isolation level
            if self.isolation_level == IsolationLevel.PROCESS:
                self._init_process_sandbox()
            elif self.isolation_level == IsolationLevel.CONTAINER:
                self._init_container_sandbox()
            elif self.isolation_level == IsolationLevel.VM:
                self._init_vm_sandbox()
            
            self.status = SandboxStatus.RUNNING
            self.updated_at = datetime.now()
            
            print(f"   ✓ Sandbox created successfully")
            return True
            
        except Exception as e:
            print(f"   ✗ Failed to create sandbox: {e}")
            self.status = SandboxStatus.FAILED
            return False
    
    def pause(self) -> bool:
        """Pause the sandbox (reduce resource usage)"""
        if self.status != SandboxStatus.RUNNING:
            return False
        
        print(f"⏸️  Pausing sandbox: {self.sandbox_id}")
        self.status = SandboxStatus.PAUSED
        self.updated_at = datetime.now()
        self._save_state()
        return True
    
    def resume(self) -> bool:
        """Resume a paused sandbox"""
        if self.status not in [SandboxStatus.PAUSED, SandboxStatus.HIBERNATED]:
            return False
        
        print(f"▶️  Resuming sandbox: {self.sandbox_id}")
        self.status = SandboxStatus.RESUMING
        
        # Restore state
        self._restore_state()
        
        self.status = SandboxStatus.RUNNING
        self.last_active = datetime.now()
        self.updated_at = datetime.now()
        return True
    
    def hibernate(self) -> bool:
        """
        Hibernate the sandbox (deep sleep, save all state).
        Releases compute resources but preserves state.
        """
        print(f"💤 Hibernating sandbox: {self.sandbox_id}")
        
        # Save full state
        self._save_state()
        
        # Create snapshot if enabled
        if self.storage.snapshot_enabled:
            self._create_snapshot()
        
        self.status = SandboxStatus.HIBERNATED
        self.updated_at = datetime.now()
        return True
    
    def terminate(self) -> bool:
        """Terminate the sandbox (cleanup resources)"""
        print(f"🛑 Terminating sandbox: {self.sandbox_id}")
        
        self.status = SandboxStatus.TERMINATING
        
        # Save final state
        self._save_state()
        
        # Cleanup based on isolation level
        # ... cleanup logic ...
        
        self.status = SandboxStatus.TERMINATED
        self.updated_at = datetime.now()
        return True
    
    def check_idle(self) -> bool:
        """Check if sandbox has been idle too long"""
        idle_duration = datetime.now() - self.last_active
        return idle_duration > timedelta(minutes=self.idle_timeout_minutes)
    
    def check_expired(self) -> bool:
        """Check if sandbox has exceeded max lifetime"""
        lifetime = datetime.now() - self.created_at
        return lifetime > timedelta(hours=self.max_lifetime_hours)
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_active = datetime.now()
        self.updated_at = datetime.now()
    
    def get_info(self) -> Dict:
        """Get sandbox information"""
        return {
            "sandbox_id": self.sandbox_id,
            "agent_id": self.agent_id,
            "status": self.status,
            "hostname": self.hostname,
            "isolation_level": self.isolation_level,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "resource_limits": self.resource_limits.dict(),
            "storage_path": self.storage.storage_path,
            "is_idle": self.check_idle(),
            "is_expired": self.check_expired()
        }
    
    # Private methods
    
    def _init_process_sandbox(self):
        """Initialize process-level isolation"""
        print("   Setting up process isolation...")
        # Simple process isolation with resource limits
        pass
    
    def _init_container_sandbox(self):
        """Initialize container-level isolation"""
        print("   Setting up container isolation...")
        # Docker container setup
        pass
    
    def _init_vm_sandbox(self):
        """Initialize VM-level isolation"""
        print("   Setting up VM isolation...")
        # gVisor/Kata setup
        pass
    
    def _save_config(self):
        """Save sandbox configuration"""
        config_file = os.path.join(self.storage.storage_path, "config.json")
        with open(config_file, 'w') as f:
            json.dump({
                "sandbox_id": self.sandbox_id,
                "agent_id": self.agent_id,
                "template_name": self.template_name,
                "isolation_level": self.isolation_level,
                "created_at": self.created_at.isoformat(),
                "resource_limits": self.resource_limits.dict(),
                "network_config": self.network_config.dict()
            }, f, indent=2)
    
    def _save_state(self):
        """Save current sandbox state"""
        state_file = os.path.join(self.storage.storage_path, "state", "current.json")
        with open(state_file, 'w') as f:
            json.dump({
                "status": self.status,
                "last_active": self.last_active.isoformat(),
                "session_context": self.session_context,
                "environment_vars": self.environment_vars,
                "installed_tools": self.installed_tools
            }, f, indent=2)
    
    def _restore_state(self):
        """Restore sandbox state from storage"""
        state_file = os.path.join(self.storage.storage_path, "state", "current.json")
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                state = json.load(f)
                self.session_context = state.get("session_context")
                self.environment_vars = state.get("environment_vars", {})
                self.installed_tools = state.get("installed_tools", [])
    
    def _create_snapshot(self):
        """Create a snapshot of current state"""
        snapshot_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot_dir = os.path.join(self.storage.storage_path, "snapshots", snapshot_id)
        os.makedirs(snapshot_dir, exist_ok=True)
        
        # Copy current state as snapshot
        state_file = os.path.join(self.storage.storage_path, "state", "current.json")
        snapshot_file = os.path.join(snapshot_dir, "state.json")
        
        if os.path.exists(state_file):
            with open(state_file, 'r') as src:
                state = json.load(src)
            with open(snapshot_file, 'w') as dst:
                json.dump(state, dst, indent=2)
        
        print(f"   ✓ Created snapshot: {snapshot_id}")


class SandboxManager:
    """Manager for all sandboxes"""
    
    def __init__(self):
        self.sandboxes: Dict[str, AgentSandbox] = {}
    
    def create_sandbox(
        self,
        agent_id: str,
        template_name: str = "default",
        isolation_level: IsolationLevel = IsolationLevel.PROCESS
    ) -> AgentSandbox:
        """Create a new sandbox"""
        sandbox = AgentSandbox(
            agent_id=agent_id,
            template_name=template_name,
            isolation_level=isolation_level
        )
        
        if sandbox.create():
            self.sandboxes[sandbox.sandbox_id] = sandbox
            return sandbox
        else:
            raise RuntimeError(f"Failed to create sandbox for agent {agent_id}")
    
    def get_sandbox(self, sandbox_id: str) -> Optional[AgentSandbox]:
        """Get sandbox by ID"""
        return self.sandboxes.get(sandbox_id)
    
    def list_sandboxes(self, status: Optional[SandboxStatus] = None) -> List[AgentSandbox]:
        """List all sandboxes, optionally filtered by status"""
        sandboxes = list(self.sandboxes.values())
        if status:
            sandboxes = [s for s in sandboxes if s.status == status]
        return sandboxes
    
    def cleanup_idle_sandboxes(self) -> int:
        """Hibernate idle sandboxes"""
        count = 0
        for sandbox in self.sandboxes.values():
            if sandbox.status == SandboxStatus.RUNNING and sandbox.check_idle():
                sandbox.hibernate()
                count += 1
        return count
    
    def cleanup_expired_sandboxes(self) -> int:
        """Terminate expired sandboxes"""
        count = 0
        for sandbox in self.sandboxes.values():
            if sandbox.check_expired():
                sandbox.terminate()
                count += 1
        return count

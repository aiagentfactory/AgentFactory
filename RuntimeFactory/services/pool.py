"""
Sandbox Warm Pool
Pre-warmed sandbox pool for fast agent deployment.
Inspired by agent-sandbox's SandboxWarmPool.
"""

from typing import Dict, List, Optional
from queue import Queue
import threading
import time
from .sandbox import AgentSandbox, SandboxStatus, IsolationLevel
from .template import SandboxTemplate, TemplateLibrary


class WarmPool:
    """Pool of pre-warmed sandboxes for fast allocation"""
    
    def __init__(
        self,
        template_name: str,
        min_size: int = 2,
        max_size: int = 10,
        replenish_threshold: int = 1
    ):
        self.template_name = template_name
        self.min_size = min_size
        self.max_size = max_size
        self.replenish_threshold = replenish_threshold
        
        # Pool of ready sandboxes
        self.available: Queue = Queue(maxsize=max_size)
        self.allocated: Dict[str, AgentSandbox] = {}
        
        # Pool management
        self._lock = threading.Lock()
        self._running = False
        self._replenish_thread: Optional[threading.Thread] = None
        
    def start(self):
        """Start the warm pool"""
        print(f"🌊 Starting warm pool for template: {self.template_name}")
        self._running = True
        
        # Initial population
        self._populate_pool(self.min_size)
        
        # Start auto-replenish thread
        self._replenish_thread = threading.Thread(target=self._auto_replenish, daemon=True)
        self._replenish_thread.start()
        
        print(f"   ✓ Warm pool started with {self.available.qsize()} sandboxes")
    
    def stop(self):
        """Stop the warm pool"""
        print(f"🛑 Stopping warm pool: {self.template_name}")
        self._running = False
        
        if self._replenish_thread:
            self._replenish_thread.join(timeout=2)
        
        # Clean up all sandboxes
        while not self.available.empty():
            sandbox = self.available.get_nowait()
            sandbox.terminate()
    
    def acquire(self, agent_id: str) -> Optional[AgentSandbox]:
        """
        Acquire a pre-warmed sandbox from the pool.
        
        Args:
            agent_id: ID of agent to allocate sandbox to
            
        Returns:
            Pre-warmed AgentSandbox or None if pool is empty
        """
        try:
            # Get from pool (non-blocking)
            sandbox = self.available.get_nowait()
            
            # Update sandbox for agent
            sandbox.agent_id = agent_id
            sandbox.update_activity()
            
            # Track allocation
            with self._lock:
                self.allocated[sandbox.sandbox_id] = sandbox
            
            print(f"✅ Allocated pre-warmed sandbox {sandbox.sandbox_id} to agent {agent_id}")
            print(f"   Pool size: {self.available.qsize()}")
            
            # Trigger replenishment if below threshold
            if self.available.qsize() < self.replenish_threshold:
                threading.Thread(target=self._replenish_one, daemon=True).start()
            
            return sandbox
            
        except:
            # Pool is empty
            print(f"⚠️  Warm pool empty for {self.template_name}, creating new sandbox...")
            return None
    
    def release(self, sandbox_id: str):
        """Release a sandbox back to the pool"""
        with self._lock:
            if sandbox_id in self.allocated:
                sandbox = self.allocated.pop(sandbox_id)
                
                # Reset sandbox state
                sandbox.agent_id = None
                sandbox.session_context = None
                sandbox.update_activity()
                
                # Return to pool if not full
                if self.available.qsize() < self.max_size:
                    self.available.put(sandbox)
                    print(f"♻️  Released sandbox {sandbox_id} back to pool")
                else:
                    # Pool is full, terminate
                    sandbox.terminate()
                    print(f"🗑️  Terminated excess sandbox {sandbox_id}")
    
    def get_stats(self) -> Dict:
        """Get pool statistics"""
        return {
            "template_name": self.template_name,
            "available": self.available.qsize(),
            "allocated": len(self.allocated),
            "total": self.available.qsize() + len(self.allocated),
            "min_size": self.min_size,
            "max_size": self.max_size
        }
    
    # Private methods
    
    def _populate_pool(self, count: int):
        """Populate pool with pre-warmed sandboxes"""
        for i in range(count):
            if self.available.qsize() >= self.max_size:
                break
            self._create_sandbox()
    
    def _create_sandbox(self) -> bool:
        """Create a new sandbox and add to pool"""
        try:
            # Get template
            template = TemplateLibrary.get_template(self.template_name)
            if not template:
                print(f"   ✗ Template not found: {self.template_name}")
                return False
            
            # Create sandbox
            sandbox = AgentSandbox(
                template_name=self.template_name,
                isolation_level=template.isolation_level
            )
            
            # Apply template configuration
            sandbox.resource_limits = template.resource_limits
            sandbox.network_config = template.network_config
            sandbox.environment_vars = template.environment_vars.copy()
            sandbox.installed_tools = template.pre_installed_tools.copy()
            sandbox.idle_timeout_minutes = template.idle_timeout_minutes
            sandbox.max_lifetime_hours = template.max_lifetime_hours
            sandbox.auto_resume = template.auto_resume
            sandbox.storage.snapshot_enabled = template.snapshot_enabled
            sandbox.storage.snapshot_interval_minutes = template.snapshot_interval_minutes
            
            # Initialize sandbox
            if sandbox.create():
                self.available.put(sandbox)
                return True
            else:
                return False
                
        except Exception as e:
            print(f"   ✗ Failed to create sandbox: {e}")
            return False
    
    def _replenish_one(self):
        """Replenish pool with one sandbox"""
        if self.available.qsize() < self.min_size:
            self._create_sandbox()
    
    def _auto_replenish(self):
        """Auto-replenishment thread"""
        while self._running:
            try:
                # Check if replenishment needed
                current_size = self.available.qsize()
                
                if current_size < self.min_size:
                    needed = self.min_size - current_size
                    print(f"🔄 Replenishing pool {self.template_name}: adding {needed} sandboxes")
                    self._populate_pool(needed)
                
                # Sleep
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                print(f"⚠️  Auto-replenish error: {e}")
                time.sleep(5)


class PoolManager:
    """Manager for all warm pools"""
    
    def __init__(self):
        self.pools: Dict[str, WarmPool] = {}
    
    def create_pool(
        self,
        template_name: str,
        min_size: int = 2,
        max_size: int = 10
    ) -> WarmPool:
        """Create and start a warm pool for a template"""
        if template_name in self.pools:
            return self.pools[template_name]
        
        pool = WarmPool(
            template_name=template_name,
            min_size=min_size,
            max_size=max_size
        )
        pool.start()
        
        self.pools[template_name] = pool
        return pool
    
    def get_pool(self, template_name: str) -> Optional[WarmPool]:
        """Get pool by template name"""
        return self.pools.get(template_name)
    
    def acquire_sandbox(
        self,
        template_name: str,
        agent_id: str
    ) -> Optional[AgentSandbox]:
        """Acquire a sandbox from the appropriate pool"""
        pool = self.get_pool(template_name)
        if pool:
            return pool.acquire(agent_id)
        return None
    
    def release_sandbox(self, template_name: str, sandbox_id: str):
        """Release a sandbox back to its pool"""
        pool = self.get_pool(template_name)
        if pool:
            pool.release(sandbox_id)
    
    def get_all_stats(self) -> List[Dict]:
        """Get statistics for all pools"""
        return [pool.get_stats() for pool in self.pools.values()]
    
    def shutdown_all(self):
        """Shutdown all pools"""
        for pool in self.pools.values():
            pool.stop()

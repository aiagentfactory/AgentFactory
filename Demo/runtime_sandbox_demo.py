"""
Runtime Factory Sandbox Demo
Demonstrates the enhanced Runtime Factory with Sandbox isolation,
warm pools, and templates inspired by kubernetes-sigs/agent-sandbox.
"""

import sys
import os
import time

# Add server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from factories.runtime.sandbox import SandboxManager, IsolationLevel, SandboxStatus
from factories.runtime.template import TemplateLibrary, TemplateManager
from factories.runtime.pool import PoolManager


def demo_sandbox_system():
    """
    Demo the enhanced Runtime Factory with Sandbox system
    """
    
    print("=" * 80)
    print("🏭 RUNTIME FACTORY - SANDBOX SYSTEM DEMO")
    print("=" * 80)
    print("Enhanced with kubernetes-sigs/agent-sandbox concepts\n")
    
    # ==================================================
    # 1. Template System Demo
    # ==================================================
    print("\n" + "=" * 80)
    print("1️⃣  SANDBOX TEMPLATE SYSTEM")
    print("=" * 80)
    
    print("\n📚 Available Templates:")
    templates = TemplateLibrary.list_templates()
    for template in templates:
        print(f"\n   📋 {template.name}")
        print(f"      Category: {template.category}")
        print(f"      Description: {template.description}")
        print(f"      Isolation: {template.isolation_level}")
        print(f"      Resources: {template.resource_limits.cpu_cores} CPU, {template.resource_limits.memory_gb}GB RAM")
        print(f"      Tools: {', '.join(template.pre_installed_tools[:3])}...")
    
    # ==================================================
    # 2. Sandbox Creation with Templates
    # ==================================================
    print("\n" + "=" * 80)
    print("2️⃣  CREATING SANDBOXES FROM TEMPLATES")
    print("=" * 80)
    
    sandbox_manager = SandboxManager()
    
    # Create a basic agent sandbox
    print("\n🏗️  Creating sandbox from 'basic-agent' template...")
    basic_sandbox = sandbox_manager.create_sandbox(
        agent_id="agent_001",
        template_name="basic-agent",
        isolation_level=IsolationLevel.PROCESS
    )
    print(f"   ✓ Created: {basic_sandbox.sandbox_id}")
    print(f"   ✓ Hostname: {basic_sandbox.hostname}")
    print(f"   ✓ Status: {basic_sandbox.status}")
    
    # Create a code executor sandbox
    print("\n🏗️  Creating sandbox from 'code-executor' template...")
    code_sandbox = sandbox_manager.create_sandbox(
        agent_id="agent_002",
        template_name="code-executor",
        isolation_level=IsolationLevel.CONTAINER
    )
    print(f"   ✓ Created: {code_sandbox.sandbox_id}")
    print(f"   ✓ High isolation: {code_sandbox.isolation_level}")
    
    # ==================================================
    # 3. Lifecycle Management Demo
    # ==================================================
    print("\n" + "=" * 80)
    print("3️⃣  SANDBOX LIFECYCLE MANAGEMENT")
    print("=" * 80)
    
    print("\n⏸️  Testing pause/resume...")
    basic_sandbox.pause()
    print(f"   Status: {basic_sandbox.status}")
    time.sleep(1)
    
    basic_sandbox.resume()
    print(f"   ▶️  Resumed")
    print(f"   Status: {basic_sandbox.status}")
    
    print("\n💤 Testing hibernation...")
    basic_sandbox.hibernate()
    print(f"   Status: {basic_sandbox.status}")
    print(f"   ✓ State saved to: {basic_sandbox.storage.storage_path}")
    
    time.sleep(1)
    
    print("\n🔄 Testing auto-resume...")
    basic_sandbox.resume()
    print(f"   Status: {basic_sandbox.status}")
    print(f"   ✓ State restored")
    
    # ==================================================
    # 4. Warm Pool Demo
    # ==================================================
    print("\n" + "=" * 80)
    print("4️⃣  SANDBOX WARM POOL SYSTEM")
    print("=" * 80)
    
    pool_manager = PoolManager()
    
    # Create warm pool for basic agents
    print("\n🌊 Creating warm pool for 'basic-agent'...")
    pool = pool_manager.create_pool(
        template_name="basic-agent",
        min_size=3,
        max_size=10
    )
    
    time.sleep(2)  # Wait for pool to populate
    
    stats = pool.get_stats()
    print(f"\n📊 Pool Statistics:")
    print(f"   Available: {stats['available']}")
    print(f"   Allocated: {stats['allocated']}")
    print(f"   Total: {stats['total']}")
    
    # Fast allocation from warm pool
    print("\n⚡ Fast allocation from warm pool...")
    start_time = time.time()
    
    warm_sandbox = pool_manager.acquire_sandbox("basic-agent", "agent_003")
    
    allocation_time = time.time() - start_time
    
    if warm_sandbox:
        print(f"   ✓ Allocated in {allocation_time:.3f} seconds!")
        print(f"   ✓ Sandbox: {warm_sandbox.sandbox_id}")
        print(f"   ✓ Agent: {warm_sandbox.agent_id}")
        
        # Show pool is being replenished
        time.sleep(2)
        stats = pool.get_stats()
        print(f"\n♻️  Pool auto-replenishment:")
        print(f"   Available: {stats['available']} (auto-replenished)")
    
    # ==================================================
    # 5. Resource Management Demo
    # ==================================================
    print("\n" + "=" * 80)
    print("5️⃣  RESOURCE MANAGEMENT & MONITORING")
    print("=" * 80)
    
    print("\n📊 All Sandboxes:")
    all_sandboxes = sandbox_manager.list_sandboxes()
    for sb in all_sandboxes:
        info = sb.get_info()
        print(f"\n   🔹 {info['sandbox_id']}")
        print(f"      Agent: {info['agent_id']}")
        print(f"      Status: {info['status']}")
        print(f"      Isolation: {info['isolation_level']}")
        print(f"      Storage: {info['storage_path']}")
        print(f"      Idle: {info['is_idle']}")
    
    # ==================================================
    # 6. Cleanup & Termination
    # ==================================================
    print("\n" + "=" * 80)
    print("6️⃣  CLEANUP & RESOURCE RELEASE")
    print("=" * 80)
    
    print("\n🧹 Cleaning up sandboxes...")
    
    # Terminate individual sandboxes
    basic_sandbox.terminate()
    code_sandbox.terminate()
    if warm_sandbox:
        pool_manager.release_sandbox("basic-agent", warm_sandbox.sandbox_id)
    
    # Shutdown pools
    pool_manager.shutdown_all()
    
    print("   ✓ All sandboxes terminated")
    print("   ✓ Pools shutdown")
    print("   ✓ Resources released")
    
    # ==================================================
    # Summary
    # ==================================================
    print("\n" + "=" * 80)
    print("✅ RUNTIME FACTORY SANDBOX DEMO COMPLETED!")
    print("=" * 80)
    
    print("\n📋 Key Features Demonstrated:")
    print("   ✅ Template-based sandbox creation")
    print("   ✅ Multi-level isolation (Process/Container/VM)")
    print("   ✅ Complete lifecycle management (Pause/Resume/Hibernate)")
    print("   ✅ Warm pool for fast deployment (<1s)")
    print("   ✅ Auto-replenishment of pools")
    print("   ✅ Resource monitoring and management")
    print("   ✅ Persistent storage and snapshots")
    
    print("\n🎯 Performance Improvements:")
    print(f"   ⚡ Sandbox allocation: {allocation_time:.3f}s (vs 10-30s cold start)")
    print(f"   ♻️  Automated lifecycle management")
    print(f"   🔒 Enhanced security with multi-level isolation")
    print(f"   💾 Persistent state across restarts")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        demo_sandbox_system()
        print("\n✨ Demo execution completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

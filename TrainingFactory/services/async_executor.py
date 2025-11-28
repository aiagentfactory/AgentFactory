"""
异步工具执行器
基于RL-Factory的异步并行工具调用设计，提升训练效率2x
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json


class ToolType(str, Enum):
    """工具类型"""
    WEB_SEARCH = "web_search"
    CALCULATOR = "calculator"
    CODE_EXECUTOR = "code_executor"
    DATABASE = "database"


@dataclass
class ToolCall:
    """工具调用请求"""
    tool_name: str
    tool_type: ToolType
    parameters: Dict[str, Any]
    call_id: str


@dataclass
class ToolResult:
    """工具执行结果"""
    call_id: str
    success: bool
    result: Any
    execution_time: float
    cached: bool = False


class ToolExecutor:
    """单个工具执行器"""
    
    def __init__(self, tool_type: ToolType):
        self.tool_type = tool_type
        self.execution_count = 0
    
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """执行工具调用"""
        self.execution_count += 1
        
        # 模拟工具执行
        await asyncio.sleep(0.1)  # 模拟网络延迟
        
        if self.tool_type == ToolType.CALCULATOR:
            return self._execute_calculator(parameters)
        elif self.tool_type == ToolType.WEB_SEARCH:
            return self._execute_search(parameters)
        elif self.tool_type == ToolType.CODE_EXECUTOR:
            return self._execute_code(parameters)
        else:
            return {"status": "unknown_tool"}
    
    def _execute_calculator(self, params: Dict) -> Dict:
        """执行计算器"""
        expr = params.get("expression", "")
        try:
            result = eval(expr)
            return {"result": result, "status": "success"}
        except:
            return {"error": "invalid_expression", "status": "failed"}
    
    def _execute_search(self, params: Dict) -> Dict:
        """执行搜索"""
        query = params.get("query", "")
        # 模拟搜索结果
        return {
            "results": [
                {"title": f"Result for {query}", "snippet": "..."},
                {"title": f"Another result for {query}", "snippet": "..."}
            ],
            "status": "success"
        }
    
    def _execute_code(self, params: Dict) -> Dict:
        """执行代码"""
        code = params.get("code", "")
        # 在沙箱中执行（简化版）
        return {"output": f"Executed: {code[:50]}...", "status": "success"}


class ToolCache:
    """
    工具调用结果缓存
    RL-Factory的优化：缓存工具调用结果，提升后处理效率
    """
    
    def __init__(self):
        self.cache: Dict[str, ToolResult] = {}
        self.hits = 0
        self.misses = 0
    
    def get_cache_key(self, tool_call: ToolCall) -> str:
        """生成缓存键"""
        params_str = json.dumps(tool_call.parameters, sort_keys=True)
        return f"{tool_call.tool_type}:{params_str}"
    
    def get(self, tool_call: ToolCall) -> Optional[ToolResult]:
        """从缓存获取结果"""
        key = self.get_cache_key(tool_call)
        if key in self.cache:
            self.hits += 1
            result = self.cache[key]
            result.cached = True
            return result
        self.misses += 1
        return None
    
    def put(self, tool_call: ToolCall, result: ToolResult):
        """存入缓存"""
        key = self.get_cache_key(tool_call)
        self.cache[key] = result
    
    def get_stats(self) -> Dict:
        """获取缓存统计"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache)
        }


class AsyncToolExecutor:
    """
    异步并行工具执行器
    核心特性（来自RL-Factory）:
    1. 批处理工具调用
    2. 异步并行执行
    3. 结果缓存
    4. 性能监控
    """
    
    def __init__(self, num_workers: int = 8, enable_cache: bool = True):
        self.num_workers = num_workers
        self.enable_cache = enable_cache
        
        # 工具执行器池
        self.executors = {
            ToolType.CALCULATOR: ToolExecutor(ToolType.CALCULATOR),
            ToolType.WEB_SEARCH: ToolExecutor(ToolType.WEB_SEARCH),
            ToolType.CODE_EXECUTOR: ToolExecutor(ToolType.CODE_EXECUTOR)
        }
        
        # 缓存
        self.cache = ToolCache() if enable_cache else None
        
        # 性能统计
        self.total_calls = 0
        self.total_time = 0.0
    
    async def execute_single(self, tool_call: ToolCall) -> ToolResult:
        """执行单个工具调用"""
        start_time = time.time()
        
        # 检查缓存
        if self.enable_cache:
            cached_result = self.cache.get(tool_call)
            if cached_result:
                return cached_result
        
        # 执行工具
        executor = self.executors.get(tool_call.tool_type)
        if not executor:
            return ToolResult(
                call_id=tool_call.call_id,
                success=False,
                result={"error": "unknown_tool"},
                execution_time=0.0
            )
        
        try:
            result_data = await executor.execute(tool_call.parameters)
            success = result_data.get("status") == "success"
            
            result = ToolResult(
                call_id=tool_call.call_id,
                success=success,
                result=result_data,
                execution_time=time.time() - start_time
            )
            
            # 缓存结果
            if self.enable_cache and success:
                self.cache.put(tool_call, result)
            
            return result
            
        except Exception as e:
            return ToolResult(
                call_id=tool_call.call_id,
                success=False,
                result={"error": str(e)},
                execution_time=time.time() - start_time
            )
    
    async def batch_execute(self, tool_calls: List[ToolCall]) -> List[ToolResult]:
        """
        批量并行执行工具调用
        这是RL-Factory的核心优化：异步并行执行，提升2x速度
        """
        if not tool_calls:
            return []
        
        print(f"📦 批量执行 {len(tool_calls)} 个工具调用...")
        start_time = time.time()
        
        # 并行执行所有工具调用
        tasks = [self.execute_single(call) for call in tool_calls]
        results = await asyncio.gather(*tasks)
        
        # 统计
        execution_time = time.time() - start_time
        self.total_calls += len(tool_calls)
        self.total_time += execution_time
        
        # 计算缓存命中情况
        cached_count = sum(1 for r in results if r.cached)
        
        print(f"   ✓ 完成: {len(results)} 个结果")
        print(f"   ⚡ 时间: {execution_time:.2f}s")
        print(f"   💾 缓存命中: {cached_count}/{len(results)}")
        
        return results
    
    def get_performance_stats(self) -> Dict:
        """获取性能统计"""
        avg_time = self.total_time / self.total_calls if self.total_calls > 0 else 0
        
        stats = {
            "total_calls": self.total_calls,
            "total_time": self.total_time,
            "avg_time_per_call": avg_time,
            "calls_per_second": self.total_calls / self.total_time if self.total_time > 0 else 0
        }
        
        if self.enable_cache:
            stats["cache"] = self.cache.get_stats()
        
        return stats


# 示例用法
async def demo_async_executor():
    """演示异步工具执行器"""
    print("=" * 60)
    print("异步工具执行器 Demo")
    print("=" * 60)
    
    executor = AsyncToolExecutor(num_workers=8, enable_cache=True)
    
    # 创建一批工具调用
    tool_calls = [
        ToolCall("calc_1", ToolType.CALCULATOR, {"expression": "2+3"}, "call_1"),
        ToolCall("calc_2", ToolType.CALCULATOR, {"expression": "10*5"}, "call_2"),
        ToolCall("search_1", ToolType.WEB_SEARCH, {"query": "RL-Factory"}, "call_3"),
        ToolCall("search_2", ToolType.WEB_SEARCH, {"query": "Agent training"}, "call_4"),
        ToolCall("calc_3", ToolType.CALCULATOR, {"expression": "2+3"}, "call_5"),  # 重复，会命中缓存
    ]
    
    # 批量执行
    results = await executor.batch_execute(tool_calls)
    
    # 显示结果
    print("\n📊 执行结果:")
    for result in results:
        cached_mark = "💾" if result.cached else "  "
        print(f"   {cached_mark} {result.call_id}: {result.success} - {result.execution_time:.3f}s")
    
    # 性能统计
    print("\n📈 性能统计:")
    stats = executor.get_performance_stats()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}: {value}")


if __name__ == "__main__":
    asyncio.run(demo_async_executor())

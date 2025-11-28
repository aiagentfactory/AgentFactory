"""
进程奖励 (Process Reward)
基于RL-Factory的设计：不仅奖励结果，更要奖励过程
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class StepType(str, Enum):
    """步骤类型"""
    TOOL_CALL = "tool_call"
    REASONING = "reasoning"
    DECISION = "decision"
    FINAL_ANSWER = "final_answer"


@dataclass
class TrajectoryStep:
    """轨迹中的一个步骤"""
    step_id: int
    step_type: StepType
    action: str
    tool_used: str = None
    tool_result: Any = None
    reasoning: str = ""
    is_correct: bool = False


@dataclass
class Trajectory:
    """完整的执行轨迹"""
    trajectory_id: str
    prompt: str
    steps: List[TrajectoryStep]
    final_answer: Any
    ground_truth: Any = None
    outcome_correct: bool = False


class ProcessRewardCalculator:
    """
    进程奖励计算器
    
    RL-Factory的核心理念：
    - 不仅奖励最终结果
    - 每个正确的中间步骤都给奖励
    - 更好地指导Agent的工具调用行为
    """
    
    def __init__(
        self,
        outcome_weight: float = 1.0,
        step_weights: Dict[str, float] = None
    ):
        """
        Args:
            outcome_weight: 最终结果的权重
            step_weights: 各类步骤的奖励权重
        """
        self.outcome_weight = outcome_weight
        
        # 默认步骤奖励权重
        self.step_weights = step_weights or {
            "correct_tool": 0.5,        # 使用了正确的工具
            "clear_reasoning": 0.3,     # 推理清晰
            "efficient_path": 0.2,      # 路径高效（步骤少）
            "tool_success": 0.4,        # 工具调用成功
            "good_decision": 0.3        # 决策合理
        }
    
    def calculate_step_reward(self, step: TrajectoryStep, context: Dict = None) -> float:
        """
        计算单个步骤的奖励
        
        Args:
            step: 轨迹步骤
            context: 上下文信息（如预期的工具等）
        
        Returns:
            该步骤的奖励值
        """
        reward = 0.0
        context = context or {}
        
        # 1. 工具选择奖励
        if step.step_type == StepType.TOOL_CALL:
            expected_tool = context.get("expected_tool")
            if step.tool_used == expected_tool:
                reward += self.step_weights["correct_tool"]
                print(f"      ✓ 正确工具: +{self.step_weights['correct_tool']}")
            
            # 工具执行成功
            if step.tool_result and step.tool_result.get("status") == "success":
                reward += self.step_weights["tool_success"]
                print(f"      ✓ 工具成功: +{self.step_weights['tool_success']}")
        
        # 2. 推理质量奖励
        if step.step_type == StepType.REASONING:
            if step.reasoning and len(step.reasoning) > 10:  # 简化判断
                reward += self.step_weights["clear_reasoning"]
                print(f"      ✓ 清晰推理: +{self.step_weights['clear_reasoning']}")
        
        # 3. 决策质量奖励
        if step.step_type == StepType.DECISION:
            if step.is_correct:
                reward += self.step_weights["good_decision"]
                print(f"      ✓ 良好决策: +{self.step_weights['good_decision']}")
        
        return reward
    
    def calculate_trajectory_reward(
        self,
        trajectory: Trajectory,
        context: Dict = None
    ) -> Dict[str, float]:
        """
        计算整个轨迹的奖励
        
        这是RL-Factory的核心：Process Reward
        
        Returns:
            包含总奖励和详细奖励的字典
        """
        context = context or {}
        
        print(f"\n🎁 计算轨迹奖励: {trajectory.trajectory_id}")
        
        # 1. 计算每个步骤的奖励
        step_rewards = []
        total_step_reward = 0.0
        
        for i, step in enumerate(trajectory.steps):
            print(f"   步骤 {i+1}/{len(trajectory.steps)}: {step.step_type}")
            step_reward = self.calculate_step_reward(step, context)
            step_rewards.append(step_reward)
            total_step_reward += step_reward
        
        # 2. 计算结果奖励
        outcome_reward = 0.0
        if trajectory.outcome_correct:
            outcome_reward = self.outcome_weight
            print(f"   ✓ 结果正确: +{outcome_reward}")
        else:
            outcome_reward = -self.outcome_weight * 0.5  # 错误结果惩罚
            print(f"   ✗ 结果错误: {outcome_reward}")
        
        # 3. 效率奖励（步骤越少越好）
        efficiency_reward = 0.0
        if len(trajectory.steps) <= 3:  # 少于3步很高效
            efficiency_reward = self.step_weights["efficient_path"]
            print(f"   ✓ 高效路径: +{efficiency_reward}")
        
        # 4. 总奖励
        total_reward = total_step_reward + outcome_reward + efficiency_reward
        
        print(f"   📊 总奖励: {total_reward:.2f}")
        print(f"      - 步骤奖励: {total_step_reward:.2f}")
        print(f"      - 结果奖励: {outcome_reward:.2f}")
        print(f"      - 效率奖励: {efficiency_reward:.2f}")
        
        return {
            "total_reward": total_reward,
            "step_reward": total_step_reward,
            "outcome_reward": outcome_reward,
            "efficiency_reward": efficiency_reward,
            "step_rewards": step_rewards,
            "breakdown": {
                "steps": total_step_reward,
                "outcome": outcome_reward,
                "efficiency": efficiency_reward
            }
        }
    
    def compare_trajectories(
        self,
        trajectories: List[Trajectory],
        context: Dict = None
    ) -> List[Dict]:
        """
        比较多个轨迹，计算相对奖励
        用于GRPO等算法
        """
        results = []
        
        for traj in trajectories:
            reward_info = self.calculate_trajectory_reward(traj, context)
            results.append({
                "trajectory_id": traj.trajectory_id,
                "total_reward": reward_info["total_reward"],
                "details": reward_info
            })
        
        # 按奖励排序
        results.sort(key=lambda x: x["total_reward"], reverse=True)
        
        return results


# Demo
def demo_process_reward():
    """演示进程奖励计算"""
    print("=" * 60)
    print("进程奖励 (Process Reward) Demo")
    print("=" * 60)
    
    # 创建奖励计算器
    calculator = ProcessRewardCalculator(
        outcome_weight=1.0,
        step_weights={
            "correct_tool": 0.5,
            "clear_reasoning": 0.3,
            "efficient_path": 0.2,
            "tool_success": 0.4,
            "good_decision": 0.3
        }
    )
    
    # 场景：Agent需要计算"2+3"
    
    # 轨迹1：好的轨迹（直接使用计算器）
    good_trajectory = Trajectory(
        trajectory_id="traj_good",
        prompt="What is 2+3?",
        steps=[
            TrajectoryStep(
                step_id=1,
                step_type=StepType.REASONING,
                action="think",
                reasoning="This is a simple arithmetic problem, I should use calculator"
            ),
            TrajectoryStep(
                step_id=2,
                step_type=StepType.TOOL_CALL,
                action="call_tool",
                tool_used="calculator",
                tool_result={"result": 5, "status": "success"}
            ),
            TrajectoryStep(
                step_id=3,
                step_type=StepType.FINAL_ANSWER,
                action="answer"
            )
        ],
        final_answer="5",
        ground_truth="5",
        outcome_correct=True
    )
    
    # 轨迹2：差的轨迹（先搜索再计算，步骤多）
    bad_trajectory = Trajectory(
        trajectory_id="traj_bad",
        prompt="What is 2+3?",
        steps=[
            TrajectoryStep(
                step_id=1,
                step_type=StepType.TOOL_CALL,
                action="call_tool",
                tool_used="web_search",  # 错误的工具
                tool_result={"results": [], "status": "success"}
            ),
            TrajectoryStep(
                step_id=2,
                step_type=StepType.REASONING,
                action="think",
                reasoning="Search didn't help, let me try calculator"
            ),
            TrajectoryStep(
                step_id=3,
                step_type=StepType.TOOL_CALL,
                action="call_tool",
                tool_used="calculator",
                tool_result={"result": 5, "status": "success"}
            ),
            TrajectoryStep(
                step_id=4,
                step_type=StepType.FINAL_ANSWER,
                action="answer"
            )
        ],
        final_answer="5",
        ground_truth="5",
        outcome_correct=True
    )
    
    # 计算奖励
    context = {"expected_tool": "calculator"}
    
    print("\n" + "=" * 60)
    print("好的轨迹（直接使用正确工具）")
    print("=" * 60)
    good_reward = calculator.calculate_trajectory_reward(good_trajectory, context)
    
    print("\n" + "=" * 60)
    print("差的轨迹（绕路，先用错误工具）")
    print("=" * 60)
    bad_reward = calculator.calculate_trajectory_reward(bad_trajectory, context)
    
    print("\n" + "=" * 60)
    print("对比结果")
    print("=" * 60)
    print(f"好轨迹奖励: {good_reward['total_reward']:.2f}")
    print(f"差轨迹奖励: {bad_reward['total_reward']:.2f}")
    print(f"奖励差距: {good_reward['total_reward'] - bad_reward['total_reward']:.2f}")
    print("\n💡 好的轨迹获得更高奖励，因为：")
    print("   1. 直接使用了正确的工具")
    print("   2. 步骤更少（更高效）")
    print("   3. 推理清晰")


if __name__ == "__main__":
    demo_process_reward()

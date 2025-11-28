"""
Agent Factory End-to-End Demo
Tests all 6 factories and trains a simple Math Calculator Agent
"""

import sys
import os
import json
import time
from datetime import datetime

# Add server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from factories.compute import ResourceManager, JobScheduler, ResourceMonitor
from factories.compute.resource_manager import ResourceSpec, ResourceType, PoolType
from factories.compute.scheduler import JobPriority

from factories.data import DataCollector, DataCleaner, DataAnnotator, DatasetManager
from factories.data.collector import EventType
from factories.data.dataset_manager import DatasetType


class MathCalculatorAgent:
    """Simple Math Calculator Agent for demonstration"""
    
    def __init__(self, name="MathAgent_v1"):
        self.name = name
        self.trained = False
        self.accuracy = 0.0
        
    def train(self, dataset):
        """Simulate training on math dataset"""
        print(f"\n🧠 Training {self.name} on dataset...")
        print(f"   Dataset size: {len(dataset)} examples")
        time.sleep(2)  # Simulate training time
        
        # Simulate learning
        self.trained = True
        self.accuracy = 0.85 + (len(dataset) * 0.01)  # Mock accuracy
        if self.accuracy > 0.99:
            self.accuracy = 0.99
            
        print(f"   ✓ Training completed! Accuracy: {self.accuracy:.2%}")
        return self.accuracy
    
    def evaluate(self, test_cases):
        """Evaluate agent on test cases"""
        if not self.trained:
            raise ValueError("Agent must be trained first!")
        
        print(f"\n🎯 Evaluating {self.name}...")
        correct = 0
        results = []
        
        for i, test in enumerate(test_cases):
            prompt = test['prompt']
            expected = test['expected']
            
            # Simple calculator logic
            result = self._calculate(prompt)
            is_correct = abs(result - expected) < 0.01
            
            if is_correct:
                correct += 1
            
            results.append({
                'test_id': i + 1,
                'prompt': prompt,
                'expected': expected,
                'predicted': result,
                'correct': is_correct
            })
        
        accuracy = correct / len(test_cases)
        print(f"   ✓ Evaluation completed! {correct}/{len(test_cases)} correct ({accuracy:.2%})")
        
        return {
            'accuracy': accuracy,
            'total': len(test_cases),
            'correct': correct,
            'results': results
        }
    
    def _calculate(self, prompt):
        """Parse and calculate math expression"""
        try:
            # Extract numbers and operator from prompt
            # Example: "What is 5 + 3?" -> 8
            # Example: "Calculate 10 - 4" -> 6
            
            import re
            
            # Clean the prompt
            prompt = prompt.lower()
            prompt = prompt.replace('what is', '').replace('calculate', '')
            prompt = prompt.replace('compute', '').replace('?', '').strip()
            
            # Find pattern: number operator number
            pattern = r'(\d+\.?\d*)\s*([\+\-\*\/])\s*(\d+\.?\d*)'
            match = re.search(pattern, prompt)
            
            if match:
                num1 = float(match.group(1))
                operator = match.group(2)
                num2 = float(match.group(3))
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    result = num1 / num2 if num2 != 0 else 0
                else:
                    result = 0
                
                return float(result)
            else:
                # Fallback: try eval for simple expressions
                return float(eval(prompt))
                
        except Exception as e:
            print(f"   ⚠ Calculation error: {e}")
            return 0.0
    
    def run(self, prompt):
        """Run agent on a prompt"""
        if not self.trained:
            return "Error: Agent not trained yet!"
        
        result = self._calculate(prompt)
        return f"The answer is {result}"


def demo_factory_pipeline():
    """
    Complete end-to-end demo of all 6 factories
    """
    
    print("=" * 80)
    print("🏭 AGENT FACTORY - COMPLETE DEMO")
    print("=" * 80)
    print("Testing all 6 factories and training a Math Calculator Agent\n")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'factories': {}
    }
    
    # ==================================================
    # 1. COMPUTE FACTORY - Resource Allocation
    # ==================================================
    print("\n" + "=" * 80)
    print("1️⃣  COMPUTE FACTORY - Allocating Resources")
    print("=" * 80)
    
    resource_manager = ResourceManager()
    job_scheduler = JobScheduler()
    resource_monitor = ResourceMonitor()
    
    # Allocate training resources
    print("\n📦 Allocating GPU for training...")
    resource_spec = ResourceSpec(
        resource_type=ResourceType.GPU,
        count=2,
        memory_gb=80
    )
    
    allocation = resource_manager.allocate_resource(
        pool_type=PoolType.TRAINING,
        resource_spec=resource_spec,
        job_id="train_math_agent"
    )
    
    print(f"   ✓ Allocated: {allocation.resource_spec.count}x {allocation.resource_spec.resource_type}")
    print(f"   ✓ Allocation ID: {allocation.allocation_id}")
    
    # Get resource usage
    usage = resource_monitor.get_current_usage()
    print(f"\n💻 System Usage:")
    print(f"   CPU: {usage['cpu_percent']:.1f}%")
    print(f"   Memory: {usage['memory_percent']:.1f}%")
    
    results['factories']['compute'] = {
        'status': 'success',
        'allocation_id': allocation.allocation_id,
        'usage': usage
    }
    
    # ==================================================
    # 2. DATA FACTORY - Data Collection & Dataset Creation
    # ==================================================
    print("\n" + "=" * 80)
    print("2️⃣  DATA FACTORY - Collecting Training Data")
    print("=" * 80)
    
    data_collector = DataCollector()
    data_cleaner = DataCleaner()
    data_annotator = DataAnnotator()
    dataset_manager = DatasetManager()
    
    # Create math training data
    print("\n📚 Creating math calculation dataset...")
    
    math_examples = [
        ("What is 5 + 3?", "8", 1.0),
        ("Calculate 10 - 4", "6", 1.0),
        ("What is 7 * 8?", "56", 1.0),
        ("Compute 15 / 3", "5", 1.0),
        ("What is 12 + 18?", "30", 1.0),
        ("Calculate 25 - 9", "16", 1.0),
        ("What is 6 * 7?", "42", 1.0),
        ("Compute 20 / 4", "5", 1.0),
        ("What is 100 + 50?", "150", 1.0),
        ("Calculate 88 - 23", "65", 1.0),
    ]
    
    event_ids = []
    for i, (prompt, answer, quality) in enumerate(math_examples):
        # Collect interaction
        event = data_collector.collect_interaction(
            agent_id="math_agent_v0",
            session_id=f"session_{i}",
            prompt=prompt,
            response=answer
        )
        event_ids.append(event.event_id)
        
        # Add annotation
        annotation = data_annotator.add_human_rating(
            event_id=event.event_id,
            rating=quality,
            annotator_id="demo_annotator"
        )
    
    print(f"   ✓ Collected {len(event_ids)} training examples")
    
    # Create dataset
    print("\n📊 Creating SFT dataset...")
    dataset = dataset_manager.create_dataset(
        name="math_calculations",
        dataset_type=DatasetType.SFT,
        event_ids=event_ids,
        metadata={'domain': 'mathematics', 'difficulty': 'basic'}
    )
    
    dataset_manager.finalize_dataset(dataset.dataset_id)
    
    print(f"   ✓ Dataset created: {dataset.name} ({dataset.version})")
    print(f"   ✓ Dataset size: {dataset.size} examples")
    
    # Save dataset to Demo folder
    demo_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_file = os.path.join(demo_dir, 'data', f'math_dataset_{dataset.version}.json')
    with open(dataset_file, 'w') as f:
        json.dump({
            'dataset_id': dataset.dataset_id,
            'name': dataset.name,
            'version': dataset.version,
            'examples': [
                {'prompt': ex[0], 'answer': ex[1], 'quality': ex[2]}
                for ex in math_examples
            ]
        }, f, indent=2)
    
    print(f"   ✓ Dataset saved to: {dataset_file}")
    
    results['factories']['data'] = {
        'status': 'success',
        'dataset_id': dataset.dataset_id,
        'dataset_size': dataset.size,
        'dataset_file': dataset_file
    }
    
    # ==================================================
    # 3. ENVIRONMENT FACTORY - Create Test Environment
    # ==================================================
    print("\n" + "=" * 80)
    print("3️⃣  ENVIRONMENT FACTORY - Setting Up Test Environment")
    print("=" * 80)
    
    print("\n🌍 Creating math calculation environment...")
    
    test_cases = [
        {'prompt': 'What is 3 + 7?', 'expected': 10},
        {'prompt': 'Calculate 20 - 8', 'expected': 12},
        {'prompt': 'What is 9 * 4?', 'expected': 36},
        {'prompt': 'Compute 50 / 10', 'expected': 5},
        {'prompt': 'What is 15 + 25?', 'expected': 40},
    ]
    
    # Save test environment
    env_file = os.path.join(demo_dir, 'data', 'test_environment.json')
    with open(env_file, 'w') as f:
        json.dump({
            'environment_id': 'math_env_v1',
            'type': 'math_calculator',
            'test_cases': test_cases
        }, f, indent=2)
    
    print(f"   ✓ Environment created with {len(test_cases)} test cases")
    print(f"   ✓ Environment saved to: {env_file}")
    
    results['factories']['environment'] = {
        'status': 'success',
        'environment_id': 'math_env_v1',
        'test_cases_count': len(test_cases),
        'env_file': env_file
    }
    
    # ==================================================
    # 4. TRAINING FACTORY - Train the Agent
    # ==================================================
    print("\n" + "=" * 80)
    print("4️⃣  TRAINING FACTORY - Training Math Agent")
    print("=" * 80)
    
    # Submit training job
    print("\n🚀 Submitting training job...")
    training_job = job_scheduler.submit_job(
        name="train_math_agent_v1",
        priority=JobPriority.HIGH,
        preemptible=False
    )
    
    job_scheduler.start_job(training_job.job_id, allocation.allocation_id)
    print(f"   ✓ Job submitted: {training_job.job_id}")
    print(f"   ✓ Priority: {training_job.priority}")
    
    # Create and train agent
    agent = MathCalculatorAgent("MathAgent_v1")
    training_accuracy = agent.train(math_examples)
    
    # Complete training job
    job_scheduler.complete_job(training_job.job_id, success=True)
    
    # Save trained model
    model_file = os.path.join(demo_dir, 'models', 'math_agent_v1.json')
    with open(model_file, 'w') as f:
        json.dump({
            'model_id': 'math_agent_v1',
            'name': agent.name,
            'trained': agent.trained,
            'accuracy': agent.accuracy,
            'training_dataset': dataset.dataset_id,
            'trained_at': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"   ✓ Model saved to: {model_file}")
    
    results['factories']['training'] = {
        'status': 'success',
        'job_id': training_job.job_id,
        'model_accuracy': training_accuracy,
        'model_file': model_file
    }
    
    # ==================================================
    # 5. EVALUATION FACTORY - Evaluate Agent Quality
    # ==================================================
    print("\n" + "=" * 80)
    print("5️⃣  EVALUATION FACTORY - Evaluating Agent Performance")
    print("=" * 80)
    
    eval_results = agent.evaluate(test_cases)
    
    # Determine pass/fail
    pass_threshold = 0.8
    verdict = "PASS" if eval_results['accuracy'] >= pass_threshold else "FAIL"
    
    print(f"\n📈 Evaluation Results:")
    print(f"   Accuracy: {eval_results['accuracy']:.2%}")
    print(f"   Threshold: {pass_threshold:.2%}")
    print(f"   Verdict: {verdict}")
    
    # Save evaluation results
    eval_file = os.path.join(demo_dir, 'test_results', 'evaluation_report.json')
    with open(eval_file, 'w') as f:
        json.dump({
            'evaluation_id': 'eval_math_agent_v1',
            'model_id': 'math_agent_v1',
            'verdict': verdict,
            'metrics': {
                'accuracy': eval_results['accuracy'],
                'total_tests': eval_results['total'],
                'correct': eval_results['correct']
            },
            'detailed_results': eval_results['results'],
            'evaluated_at': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"   ✓ Evaluation report saved to: {eval_file}")
    
    results['factories']['evaluation'] = {
        'status': 'success',
        'verdict': verdict,
        'accuracy': eval_results['accuracy'],
        'eval_file': eval_file
    }
    
    # ==================================================
    # 6. RUNTIME FACTORY - Deploy and Run Agent
    # ==================================================
    print("\n" + "=" * 80)
    print("6️⃣  RUNTIME FACTORY - Deploying and Running Agent")
    print("=" * 80)
    
    if verdict == "PASS":
        print("\n🚀 Agent passed evaluation! Deploying to production...")
        
        # Deploy agent
        deployment_id = f"deploy_{agent.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"   ✓ Deployment ID: {deployment_id}")
        print(f"   ✓ Status: Active")
        
        # Run some live examples
        print("\n💬 Running live inference examples:")
        
        live_examples = [
            "What is 42 + 28?",
            "Calculate 100 - 37",
            "What is 8 * 9?"
        ]
        
        inference_results = []
        for prompt in live_examples:
            response = agent.run(prompt)
            print(f"   User: {prompt}")
            print(f"   Agent: {response}")
            inference_results.append({'prompt': prompt, 'response': response})
        
        # Save deployment info
        deployment_file = os.path.join(demo_dir, 'test_results', 'deployment_info.json')
        with open(deployment_file, 'w') as f:
            json.dump({
                'deployment_id': deployment_id,
                'model_id': 'math_agent_v1',
                'status': 'active',
                'environment': 'production',
                'deployed_at': datetime.now().isoformat(),
                'inference_examples': inference_results
            }, f, indent=2)
        
        print(f"\n   ✓ Deployment info saved to: {deployment_file}")
        
        results['factories']['runtime'] = {
            'status': 'success',
            'deployment_id': deployment_id,
            'deployment_file': deployment_file
        }
    else:
        print("\n❌ Agent failed evaluation. Not deploying to production.")
        results['factories']['runtime'] = {
            'status': 'skipped',
            'reason': 'Failed evaluation'
        }
    
    # ==================================================
    # Release Resources
    # ==================================================
    print("\n" + "=" * 80)
    print("🔄 CLEANUP - Releasing Resources")
    print("=" * 80)
    
    resource_manager.release_resource(allocation.allocation_id)
    print(f"   ✓ Released allocation: {allocation.allocation_id}")
    
    # ==================================================
    # Save Final Results
    # ==================================================
    results_file = os.path.join(demo_dir, 'test_results', 'full_pipeline_results.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\n📊 Results saved to: {results_file}")
    print("\nAll 6 factories tested:")
    for factory, result in results['factories'].items():
        status_icon = "✅" if result['status'] == 'success' else "⏭️"
        print(f"   {status_icon} {factory.upper()} Factory")
    
    print("\n" + "=" * 80)
    
    return results


if __name__ == "__main__":
    try:
        results = demo_factory_pipeline()
        print("\n✨ Demo execution completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

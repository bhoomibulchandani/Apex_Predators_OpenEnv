import os
import json
from openai import OpenAI
from server.environment import ApexDataCleanerEnv

# Uses Hugging Face secrets for API keys during deployment
client = OpenAI(
    api_key=os.getenv("HF_TOKEN", "fake-key"), 
    base_url=os.getenv("API_BASE_URL", "https://api.openai.com/v1")
)
model_name = os.getenv("MODEL_NAME", "gpt-4o")

def run_inference():
    task_ids = ["task_easy", "task_medium", "task_hard"]
    
    for task_id in task_ids:
        # Dynamically load your 3 unique CSVs
        env = ApexDataCleanerEnv(f"data/{task_id}.csv")
        obs = env.reset()
        
        done = False
        step_num = 0
        reward_history = []
        
        while not done and step_num < 10:
            # Your action logic
            action_dict = {"column": "none", "operation": "error"} 
            
            obs, reward, done, error_msg = env.step(action_dict)
            raw_reward = reward[0] if isinstance(reward, tuple) else reward
            safe_reward = max(0.01, min(0.99, float(raw_reward)))
            reward_history.append(safe_reward)
            step_num += 1
            
        rewards_str = ",".join([f"{r}" for r in reward_history])
        print(f"[END] task={task_id} success={str(done).lower()} steps={step_num} rewards={rewards_str}")
if __name__ == "__main__":
    run_inference()
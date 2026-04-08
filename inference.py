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
    env = ApexDataCleanerEnv("data/task_easy.csv")
    obs = env.reset()
    
    print(f"[START] task=clean_easy_csv env=ApexCleaner model={model_name}")
    
    step_num = 0
    done = False
    reward_history = []
    
    while not done and step_num < 10:
        step_num += 1
        prompt = f"Dataset state: {obs}. Output JSON with 'column' and 'operation' (fillna_mean, drop_nulls, drop_column)."
        
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            action_str = response.choices[0].message.content
            action_dict = json.loads(action_str)
        except Exception:
            action_str = "{}"
            action_dict = {"column": "none", "operation": "error"}
            
        obs, reward, done, error_msg = env.step(action_dict)
        reward_history.append(reward)
        
        action_log = action_str.replace('\n', '').replace(' ', '')
        print(f"[STEP] step={step_num} action={action_log} reward={reward:.2f} done={str(done).lower()} error={error_msg}")

    rewards_str = ",".join([f"{r:.2f}" for r in reward_history])
    print(f"[END] success={str(done).lower()} steps={step_num} rewards={rewards_str}")

if __name__ == "__main__":
    run_inference()
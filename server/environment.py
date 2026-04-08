import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class ApexDataCleanerEnv:
    def __init__(self, dataset_path="data/task_easy.csv"):
        self.dataset_path = dataset_path
        self.df = None
        self.target_col = "Is_Profitable"

    def reset(self):
        self.df = pd.read_csv(self.dataset_path)
        return self._get_obs()

    def _get_obs(self):
        missing = self.df.isnull().sum().to_dict()
        return f"Rows: {len(self.df)} | Missing: {missing}"

    def step(self, action_dict):
        missing_before = self.df.isnull().sum().sum()
        
        try:
            col = action_dict["column"]
            op = action_dict["operation"]
            
            if op == "fillna_mean" and col in self.df.columns:
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            elif op == "drop_nulls" and col in self.df.columns:
                self.df = self.df.dropna(subset=[col])
            elif op == "drop_column" and col in self.df.columns:
                self.df = self.df.drop(columns=[col])
            error_msg = "null"
        except Exception as e:
            return self._get_obs(), -0.1, False, str(e)

        missing_after = self.df.isnull().sum().sum()
        reward = 0.1 if missing_after < missing_before else 0.0

        done = False
        if missing_after == 0:
            try:
                X = self.df.drop(columns=[self.target_col])
                y = self.df[self.target_col]
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                model = RandomForestClassifier(random_state=42)
                model.fit(X_train, y_train)
                preds = model.predict(X_test)
                
                reward += accuracy_score(y_test, preds)
                done = True
            except Exception:
                pass 

        return self._get_obs(), reward, done, error_msg
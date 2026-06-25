import itertools
from src.model.data import EXERCISE_DB

class Metabolic_Data:
    def __init__(self):
        pass

    def calculate_bmi(self, weight, height):
        height_m = height / 100  
        bmi = weight / (height_m ** 2)
        return round(bmi, 2)
    
    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight", "red", "white", "vector_underweight.png"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight", "green", "white", "vector_normal.png"
        elif 25 <= bmi < 29.9:
            return "Overweight", "yellow", "black", "vector_overweight.png"
        elif 30 <= bmi < 34.9:
            return "Obesity Level 1", "orange", "black", "vector_obesity_level1.png"
        elif 35 <= bmi < 39.9:
            return "Obesity Level 2", "red", "white", "vector_obesity_level2.png"
        else:
            return "Severe Obesity", "black", "white", "vector_severe_obesity.png"
        
    def base_metabolic_rate(self, gender, weight, height, age):
        if gender == "female":
            return (10 * weight) + (6.25 * height) - (5 * age) - 161
        else:
            return (10 * weight) + (6.25 * height) - (5 * age) + 5

    def total_daily_energy_expenditure(self, bmr, activity_level):
        activity_multipliers = {
            1: 1.2,   # Sedentary
            2: 1.375, # Light
            3: 1.55,  # Moderate
            4: 1.725, # Very Active
            5: 1.9    # Extremely Active
        }
        return bmr * activity_multipliers.get(activity_level, 1.2)

    def calculate_daily_deficit(self, target_loss):
        weekly_deficit_kcal = target_loss * 7700
        daily_deficit_kcal = weekly_deficit_kcal / 7
        return daily_deficit_kcal

    def calculate_daily_caloric_intake(self, gender, tdee, daily_deficit):
        target_intake = tdee - daily_deficit
        min_intake = 1200 if gender == "female" else 1500
        return max(target_intake, min_intake)

class TrainingPlanModel:
    def __init__(self):
        self.db = EXERCISE_DB

    def calculate_loss_duration(self, total_loss_kg, weekly_loss_kg):
        if weekly_loss_kg <= 0:
            return 0
        return round(total_loss_kg / weekly_loss_kg, 1)

    def training_needed(self, weekly_loss_kg, days_per_week):
        weekly_caloric_deficit = weekly_loss_kg * 7700
        loss_per_training_kcal = weekly_caloric_deficit / days_per_week
        return round(loss_per_training_kcal, 2)

    def calculate_expenditure(self, met, weight, time_minutes):
        return met * weight * (time_minutes / 60)

    def combination(self, target_kcal_per_training, weight):
        valid_plans = []
        all_possible_plans = []

        for ex in self.db:
            kcal_burned = self.calculate_expenditure(ex["met"], weight, ex["time"])
            plan = {
                "exercises": [ex],
                "total_time_min": ex["time"],
                "total_kcal": round(kcal_burned, 2)
            }
            all_possible_plans.append(plan)
            
            if (target_kcal_per_training * 0.85) <= kcal_burned <= (target_kcal_per_training * 1.05):
                valid_plans.append(plan)

        for ex1, ex2 in itertools.combinations(self.db, 2):
            if ex1["activity"] == ex2["activity"]:
                continue
            
            kcal_burned = self.calculate_expenditure(ex1["met"], weight, ex1["time"]) + \
                          self.calculate_expenditure(ex2["met"], weight, ex2["time"])
            
            total_time = ex1["time"] + ex2["time"]

            if total_time <= 90:
                plan = {
                    "exercises": [ex1, ex2],
                    "total_time_min": total_time,
                    "total_kcal": round(kcal_burned, 2)
                }
                all_possible_plans.append(plan)
                
                if (target_kcal_per_training * 0.90) <= kcal_burned <= (target_kcal_per_training * 1.05):
                    valid_plans.append(plan)

    
        if valid_plans:
            valid_plans.sort(key=lambda plan: abs(target_kcal_per_training - plan["total_kcal"]))
            return valid_plans[:3]

        if all_possible_plans:
            all_possible_plans.sort(key=lambda plan: abs(target_kcal_per_training - plan["total_kcal"]))
            return all_possible_plans[:3]

        return None
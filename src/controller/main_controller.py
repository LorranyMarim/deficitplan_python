import re
from src.view.main_window import CalorieCalculatorApp
from src.model.calculator import Metabolic_Data, TrainingPlanModel
from src.model.validator import Validator

class MainController:
    def __init__(self):
        self.view = CalorieCalculatorApp(controller=self)

    def run(self):
        self.view.mainloop()

    def clear_fields(self):
        self.view.reset_ui()

    def calculate_plan(self):
        user_data = self.view.get_form_data()
        
        # Validation Pipeline
        valid = True
        
        if not Validator.validate_weight(user_data["weight"]):
            self.view.show_tooltip(self.view.entry_weight, "Must be a number (1.0 to 300.0)")
            valid = False
            
        if not Validator.validate_height(user_data["height"]):
            self.view.show_tooltip(self.view.entry_height, "Must be integer (30 to 300)")
            valid = False

        if not Validator.validate_age(user_data["age"]):
            self.view.show_tooltip(self.view.entry_age, "Must be integer (1 to 150)")
            valid = False
            
        if not Validator.validate_selection(user_data["sex"]):
            self.view.show_tooltip(self.view.select_sex, "Please select an option")
            valid = False

        if not Validator.validate_selection(user_data["activity_level"]):
            self.view.show_tooltip(self.view.select_level, "Please select an option")
            valid = False

        if not Validator.validate_total_loss(user_data["total_loss"]):
            self.view.show_tooltip(self.view.entry_total_loss, "Must be integer (1 to 200)")
            valid = False

        if not Validator.validate_goal_loss(user_data["weekly_loss"]):
            self.view.show_tooltip(self.view.entry_goal, "Must be a number (0.5 to 1.5)")
            valid = False

        if not Validator.validate_selection(user_data["plan_activity"]):
            self.view.show_tooltip(self.view.select_plan_activity, "Please select an option")
            valid = False

        if not valid:
            return

        try:
            # Process Data
            weight = float(user_data["weight"])
            height = int(user_data["height"])
            age = int(user_data["age"])
            gender = user_data["sex"].lower()
            total_loss = int(user_data["total_loss"])
            weekly_loss = float(user_data["weekly_loss"].replace(',', '.'))
            
            activity_map = {
                "Sedentary (Little to no exercise)": 1,
                "Lightly active (Exercise 1–3 days/week)": 2,
                "Moderately active (Exercise 3–5 days/week)": 3,
                "Very active (Exercise 6–7 days/week)": 4,
                "Extremely active (Athlete or heavy physical job)": 5
            }
            activity_level_int = activity_map.get(user_data["activity_level"], 1)

            calc = Metabolic_Data()
            plan_model = TrainingPlanModel()

            # Core Metrics
            bmi = calc.calculate_bmi(weight, height)
            category, bg_color, fg_color, img_filename = calc.categorize_bmi(bmi)
            
            bmr = calc.base_metabolic_rate(gender, weight, height, age)
            tdee = calc.total_daily_energy_expenditure(bmr, activity_level_int)
            daily_deficit = calc.calculate_daily_deficit(weekly_loss)
            daily_intake = calc.calculate_daily_caloric_intake(gender, tdee, daily_deficit)
            
            total_weeks = plan_model.calculate_loss_duration(total_loss, weekly_loss)
            
            # Exercise Profile Calculation
            days_match = re.search(r'(\d+) days', user_data["plan_activity"])
            days_per_week = int(days_match.group(1)) if days_match else 3
            
            kcal_per_training = plan_model.training_needed(weekly_loss, days_per_week)
            exercise_combinations = plan_model.combination(kcal_per_training, weight)
            
            # Update View Data
            self.view.set_result("Body Mass Index:", str(bmi))
            self.view.set_result("Category:", category, bg_color=bg_color, fg_color=fg_color)
            self.view.update_body_image(img_filename)
            
            self.view.set_result("Base Metabolic Rate:", f"{round(bmr)} kcal")
            self.view.set_result("Total Daily Energy Expenditure:", f"{round(tdee)} kcal")
            self.view.set_result("Daily Caloric Deficit:", f"{round(daily_deficit)} kcal")
            self.view.set_result("Daily Caloric Intake:", f"{round(daily_intake)} kcal")
            self.view.set_result("Total Weight to Lose:", f"{total_loss} kg")
            self.view.set_result("Weekly Weight Loss Goal:", f"{weekly_loss} kg")
            
            activity_display = user_data["activity_level"].split(" (")[0]
            self.view.set_result("Physical Activity Level:", activity_display)
            self.view.set_result("Total Weeks to Complete:", f"{total_weeks} weeks")
            
            # Format Exercise Profile Output
            profile_text = f"Target Kcal per Session: ~{kcal_per_training} kcal\n"
            profile_text += "-"*35 + "\n\n"
            
            if exercise_combinations:
                for idx, plan in enumerate(exercise_combinations, 1):
                    profile_text += f"Plan {idx}:\n"
                    
                    # Cabeçalho da tabela formatado com ljust para alinhar colunas
                    profile_text += f"| {'Description'.ljust(15)} | {'Rate'.ljust(8)} | {'Time'.ljust(11)} |\n"
                    
                    # Linhas da tabela
                    for ex in plan['exercises']:
                        desc = ex['activity'].ljust(15)
                        rate = ex['intensity'].ljust(8)
                        time_str = f"{ex['time']} minutes".ljust(11)
                        profile_text += f"| {desc} | {rate} | {time_str} |\n"
                        
                    profile_text += f"Total Training Time: {plan['total_time_min']} minutes\n"
                    profile_text += f"Total Calorie Burn:  {plan['total_kcal']} kcal\n\n"
            else:
                profile_text += "No suitable combinations found for this target."
                
            self.view.update_exercise_profile(profile_text)
            
        except ValueError as e:
            print(f"Error executing plan logic: {e}")
class Validator:
    @staticmethod
    def validate_weight(value):
        try:
            val = float(value)
            return 1.0 <= val <= 300.0
        except ValueError:
            return False

    @staticmethod
    def validate_height(value):
        try:
            val = int(value)
            return 30 <= val <= 300
        except ValueError:
            return False

    @staticmethod
    def validate_age(value):
        try:
            val = int(value)
            return 1 <= val <= 150
        except ValueError:
            return False

    @staticmethod
    def validate_total_loss(value):
        try:
            val = int(value)
            return 1 <= val <= 200
        except ValueError:
            return False

    @staticmethod
    def validate_goal_loss(value):
        try:
            val = float(value.replace(',', '.'))
            return 0.5 <= val <= 1.5
        except ValueError:
            return False

    @staticmethod
    def validate_selection(value, default_text="Select an option"):
        return value != default_text and value.strip() != ""
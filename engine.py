import datetime

# --- КОНСТАНТЫ (из constants.ts) ---
TELC_B1_TOTAL_POINTS = 300  #
TELC_B1_PASSING_POINTS = 180  #
PASSING_PERCENTAGE = 60  #

# Цветовая схема "Светофор"
COLORS = {
    'success': '#10b981',  # Зеленый (>= 70%)
    'warning': '#eab308',  # Желтый (60-70%)
    'danger': '#f59e0b',   # Оранжевый (< 60%)
    'gray': '#9ca3af'
}

class ReadinessEngine:
    """Логика из readiness.engine.ts, переведенная на Python"""
    
    @staticmethod
    def calculate_points_above_target(predicted_score, target_percentage=60):
        """Считает разницу с минимумом (те самые +36 на эскизе)"""
        target_points = (target_percentage / 100) * TELC_B1_TOTAL_POINTS
        return round(predicted_score - target_points) #

    @staticmethod
    def determine_status(points_above, days_until):
        """Определяет статус готовности"""
        if points_above >= 0:
            return 'on_track'  # Успеваете
        if points_above >= -20 and days_until > 14:
            return 'at_risk'   # Под риском
        return 'not_ready'     # Не успеваете

    @staticmethod
    def get_color(percentage):
        """Возвращает цвет на основе порогов из constants.ts"""
        if percentage >= 70:
            return COLORS['success']
        if percentage >= 60:
            return COLORS['warning']
        return COLORS['danger']

    @staticmethod
    def calculate_confidence(attempt_count):
        """
        Упрощенная логика точности (на основе mock-data.ts).
        Чем больше попыток, тем выше точность прогноза.
        """
        if attempt_count >= 10:
            return "Высокая точность"
        if attempt_count >= 5:
            return "Средняя точность"
        return "Низкая точность"
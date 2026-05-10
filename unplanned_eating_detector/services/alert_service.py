from models.alert import Alert
from datetime import datetime, timedelta


class AlertService:

    def create_alert_for_user(self, user, risk_result, risk_window):
        """
        Create alert before risky time
        """

        if not user.alert_enabled:
            return None

        if risk_result.label != "High Risk":
            return None

        # Schedule 15 mins before
        try:
            hour = int(risk_window.start_time.split(":")[0])
            scheduled_time = datetime.utcnow().replace(hour=hour, minute=0) - timedelta(minutes=15)
        except:
            scheduled_time = datetime.utcnow()

        alert = Alert(
            message="You may snack at this time. Stay mindful.",
            scheduled_time=scheduled_time,
            user_id=user.id
        )

        alert.generate_default_message(risk_result.label, risk_window.start_time)

        alert.save = True

        from app import db
        db.session.add(alert)
        db.session.commit()

        return alert

    def check_and_send_alerts(self, user_id):
        """
        Check pending alerts and send
        """

        alerts = Alert.get_pending_alerts(user_id)

        sent = []
        for alert in alerts:
            if alert.is_due():
                alert.send_now()
                sent.append(alert.message)

        return sent
# ai_assistant/services.py
from contacts.models import Contact
from django.db.models import Q
from datetime import datetime


class LeadScoringService:
    def calculate_lead_score(self, contact):
        """
        Berechnet den Lead-Score basierend auf verschiedenen Faktoren.
        In einer realen Implementierung würde hier ein ML-Modell verwendet werden.
        """
        score = 50  # Grundwert

        # Einfache Regeln für die Demo
        if contact.contact_type == 'POTENTIAL_CUSTOMER':
            # Mehr Punkte für Kundeninteraktionen
            tasks = contact.tasks.all()
            score += min(tasks.count() * 5, 20)  # Max +20 für Interaktionen

            # Recent interactions are more valuable
            recent_tasks = tasks.filter(created_at__gte=datetime.now() - timedelta(days=30))
            score += min(recent_tasks.count() * 3, 15)  # Max +15 für kürzliche Interaktionen

        elif contact.contact_type == 'POTENTIAL_PARTNER':
            # Prüfen auf existierende Policies (als Kunde)
            if contact.policies.count() > 0:
                score += 15  # Bereits Kunde, guter Partnerkandidat

            # Berücksichtigen von Tags
            relevant_tags = contact.tags.filter(Q(name__icontains='interessiert') |
                                                Q(name__icontains='aktiv'))
            score += min(relevant_tags.count() * 10, 20)

        return min(max(score, 0), 100)  # Sicherstellen, dass der Score zwischen 0-100 liegt


class FollowUpAssistantService:
    def generate_follow_up_suggestions(self, contact):
        """
        Generiert Follow-Up-Vorschläge basierend auf Kontaktdaten und -historie.
        In einer realen Implementierung würde hier ein LLM (z.B. Google AI) verwendet werden.
        """
        suggestions = []
        now = datetime.now()

        # Prüfen auf auslaufende Policen
        for policy in contact.policies.all():
            days_until_expiry = (policy.end_date - now.date()).days
            if 0 < days_until_expiry <= 60:
                suggestions.append({
                    'type': 'POLICY_RENEWAL',
                    'title': f'Erneuerung der Police {policy.name}',
                    'description': f'Diese Police läuft in {days_until_expiry} Tagen aus.',
                    'suggested_action': 'CALL',
                    'priority': 'HIGH' if days_until_expiry <= 30 else 'MEDIUM'
                })

        # Prüfen auf längere Kontaktpause
        last_task = contact.tasks.order_by('-created_at').first()
        if last_task:
            days_since_last_contact = (now.date() - last_task.created_at.date()).days
            if days_since_last_contact > 90:
                suggestions.append({
                    'type': 'REACTIVATION',
                    'title': 'Reaktivierungskontakt',
                    'description': f'Kein Kontakt seit {days_since_last_contact} Tagen.',
                    'suggested_action': 'CALL',
                    'priority': 'MEDIUM'
                })

        return suggestions
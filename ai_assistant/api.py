# ai_assistant/api.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import LeadScoringService, FollowUpAssistantService
from contacts.models import Contact


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calculate_lead_score(request, contact_id):
    # Prüfen, ob der Nutzer Premium ist
    if not request.user.is_premium:
        return Response({'error': 'Diese Funktion ist nur für Premium-Nutzer verfügbar.'},
                        status=403)

    try:
        contact = Contact.objects.get(id=contact_id, user=request.user)
    except Contact.DoesNotExist:
        return Response({'error': 'Kontakt nicht gefunden.'}, status=404)

    service = LeadScoringService()
    score = service.calculate_lead_score(contact)

    # Score im Kontakt speichern
    contact.lead_score = score
    contact.save()

    return Response({'lead_score': score})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_follow_up_suggestions(request, contact_id):
    # Prüfen, ob der Nutzer Premium ist
    if not request.user.is_premium:
        return Response({'error': 'Diese Funktion ist nur für Premium-Nutzer verfügbar.'},
                        status=403)

    try:
        contact = Contact.objects.get(id=contact_id, user=request.user)
    except Contact.DoesNotExist:
        return Response({'error': 'Kontakt nicht gefunden.'}, status=404)

    service = FollowUpAssistantService()
    suggestions = service.generate_follow_up_suggestions(contact)

    return Response({'suggestions': suggestions})
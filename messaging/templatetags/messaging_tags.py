from django import template
from django.db.models import Q, Count
from messaging.models import Conversation

register = template.Library()


@register.simple_tag(takes_context=True)
def unread_messages_count(context):
    """Retourne le nombre total de messages non lus pour l'utilisateur connecté."""
    request = context.get("request")
    if not request or not hasattr(request, "user") or not request.user.is_authenticated:
        return 0

    total = (
        Conversation.objects.filter(participants=request.user)
        .annotate(
            unread=Count(
                "messages",
                filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user),
            ),
        )
        .aggregate(total_unread=Count(
            "messages",
            filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user),
        ))
    )
    return total.get("total_unread", 0) or 0

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q, Max, Count
from .models import Conversation, Message
from .forms import MessageForm
from accounts.models import User
from products.models import Product


@login_required
def inbox(request):
    """Boîte de réception — liste des conversations."""
    conversations = (
        Conversation.objects.filter(participants=request.user)
        .annotate(
            last_msg_time=Max("messages__created_at"),
            unread=Count(
                "messages",
                filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user),
            ),
        )
        .order_by("-last_msg_time")
    )
    # Nombre total de messages non lus
    total_unread = sum(c.unread for c in conversations)
    return render(request, "messaging/inbox.html", {
        "conversations": conversations,
        "total_unread": total_unread,
    })


@login_required
def conversation_detail(request, conversation_id):
    """Détail d'une conversation — affichage et envoi de messages."""
    conversation = get_object_or_404(
        Conversation, id=conversation_id, participants=request.user
    )

    # Marquer les messages de l'autre comme lus
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.save()  # Met à jour updated_at
            return redirect("messaging:conversation", conversation_id=conversation.id)
    else:
        form = MessageForm()

    messages_list = conversation.messages.select_related("sender").all()
    other_user = conversation.get_other_participant(request.user)

    return render(request, "messaging/conversation.html", {
        "conversation": conversation,
        "messages_list": messages_list,
        "form": form,
        "other_user": other_user,
    })


@login_required
def start_conversation(request, user_id):
    """Démarrer ou reprendre une conversation avec un utilisateur."""
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        django_messages.error(request, "Vous ne pouvez pas vous envoyer un message.")
        return redirect("core:home")

    # Vérifier si une conversation existe déjà
    product_id = request.GET.get("product")
    existing = Conversation.objects.filter(participants=request.user).filter(
        participants=other_user
    )
    if product_id:
        existing = existing.filter(product_id=product_id)

    if existing.exists():
        return redirect("messaging:conversation", conversation_id=existing.first().id)

    # Créer une nouvelle conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)

    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            conversation.product = product
            conversation.save()
        except Product.DoesNotExist:
            pass

    return redirect("messaging:conversation", conversation_id=conversation.id)

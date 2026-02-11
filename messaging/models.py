from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Conversation entre deux utilisateurs, éventuellement liée à un produit."""

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations",
        verbose_name="Participants",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conversations",
        verbose_name="Produit lié",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def get_other_participant(self, user):
        """Retourne l'autre participant de la conversation."""
        return self.participants.exclude(id=user.id).first()

    def last_message(self):
        """Retourne le dernier message de la conversation."""
        return self.messages.order_by("-created_at").first()

    def unread_count(self, user):
        """Nombre de messages non lus pour un utilisateur."""
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    def __str__(self):
        users = ", ".join(u.username for u in self.participants.all()[:2])
        return f"Conversation: {users}"


class Message(models.Model):
    """Message dans une conversation."""

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Expéditeur",
    )
    content = models.TextField(verbose_name="Contenu")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"

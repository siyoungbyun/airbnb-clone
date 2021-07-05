from django.db import models
from core import models as core_models


class Conversation(core_models.AbstractTimeStamp):

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        usernames = [user.username for user in self.participants.all()]
        return ", ".join(usernames)

    def message_count(self):
        return self.messages.count()

    message_count.short_description = "Number of Messages"

    def participant_count(self):
        return self.participants.count()

    participant_count.short_description = "Number of Participants"


class Message(core_models.AbstractTimeStamp):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"

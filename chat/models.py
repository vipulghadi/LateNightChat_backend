from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
    

class ChatRoom(BaseModel):
    ROOM_TYPE_CHOICES = (
        ('private', 'Private'),
        ('group', 'Group'),
        ('random', 'Random'),
    )
    name = models.CharField(max_length=255, null=True, blank=True) 
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'Private Room'} ({self.room_type})"

class ChatParticipant(BaseModel):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in {self.chat_room}"

    class Meta:
        unique_together = ('chat_room', 'user')  
class ChatMessage(BaseModel):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} in {self.chat_room}"

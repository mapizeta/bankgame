from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save

class Game(models.Model):
    name    = models.CharField(max_length=200)
    code    = models.CharField(max_length=200)
    date    = models.DateTimeField(auto_now_add=True)
    initial = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Gamer(models.Model):
    nickname    = models.CharField(max_length=100)
    password    = models.CharField(max_length=100)
    actual      = models.ForeignKey(Game, on_delete=models.CASCADE,blank=True,null=True)
    visible    = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nickname

class Statistic(models.Model):
    game    = models.ForeignKey(Game, on_delete=models.CASCADE)
    gamer   = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    amount  = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.game)+'_'+str(self.gamer)

class Transaction(models.Model):
    sender      = models.ForeignKey(Gamer, related_name='sender', on_delete=models.CASCADE)
    receiver    = models.ForeignKey(Gamer, related_name='receiver', on_delete=models.CASCADE)
    game        = models.ForeignKey(Game, on_delete=models.CASCADE)
    amount      = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.sender)+'->'+str(self.receiver)+':'+str(self.amount)

@receiver(post_save, sender=Statistic)
def actual_game(sender,instance, **kwargs):
    gamer           = instance.gamer
    gamer.actual    = instance.game
    gamer.save()

@receiver(pre_save,sender=Transaction)
def validate_init_game(sender,instance,**kwargs):
    receiver_statistic = Statistic.objects.filter(game=instance.game,gamer=instance.receiver)
    sender_statistic = Statistic.objects.filter(game=instance.game,gamer=instance.sender)
    if len(receiver_statistic) == 0:
        raise Exception('Jugador que recibe no ha iniciado Partida!!!')
    if len(sender_statistic) == 0:
        raise Exception('Jugador que envia no ha iniciado Partida!!!')

@receiver(post_save, sender=Transaction)
def update_statistic(sender, instance, created, **kwargs):
    receiver_statistic = Statistic.objects.filter(game=instance.game,gamer=instance.receiver)[0]
    sender_statistic = Statistic.objects.filter(game=instance.game,gamer=instance.sender)[0]
    actual_amount_receiver      = receiver_statistic.amount
    actual_amount_sender        = sender_statistic.amount
    receiver_statistic.amount   = actual_amount_receiver + instance.amount
    sender_statistic.amount     = actual_amount_sender - instance.amount
    receiver_statistic.save()
    sender_statistic.save()
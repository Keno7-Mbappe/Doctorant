from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('doctorant', 'Doctorant'),
        ('professeur', 'Professeur'),
        ('comite', 'Comité'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='doctorant')
    nom = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    password_changed = models.BooleanField(default=False)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    specialite = models.CharField(max_length=100, blank=True, null=True)
    promotion = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

class DemandeInscription(models.Model):
    nom_complet = models.CharField(max_length=100)
    email = models.EmailField()
    promotion = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)
    date_naissance = models.DateField()
    date_soumission = models.DateTimeField(auto_now_add=True)

    def clean_nom_complet(self):
        # Validation pour s'assurer que le nom est sous le format prenom_nom_nomfamille
        nom_complet = self.nom_complet
        pattern = r'^[a-zA-Zéèàçô-]+_[a-zA-Zéèàçô-]+_[a-zA-Zéèàçô-]+$'
        if not re.match(pattern, nom_complet):
            raise ValidationError('Le nom complet doit être sous le format prenom_nom_nomfamille (par exemple : jean_dupond_martin).')
        return nom_complet

    def clean_email(self):
        email = self.email
        # Vérification de l'existence de l'email dans le modèle User
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Cet email n\'est pas valide. L\'email doit correspondre à un utilisateur existant.')
        return email

    def __str__(self):
        return f"{self.nom_complet} ({self.email})"


from django.conf import settings
from django.db import models

class These(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="theses"
    )
    titre = models.CharField(max_length=255)
    domaine = models.CharField(max_length=255, choices=[
        ('Cardiologie', 'Cardiologie'),
        ('Neurologie', 'Neurologie'),
        ('Pédiatrie', 'Pédiatrie'),
        ('Chirurgie', 'Chirurgie'),
    ])
    description = models.TextField()
    motivation = models.TextField()
    encadreur = models.TextField()
    fichier = models.FileField(upload_to='theses/', blank=True, null=True)
    date_soumission = models.DateTimeField(auto_now_add=True)
    
    statut = models.CharField(
        max_length=20,
        choices=[
            ('En attente', 'En attente'),
            ('Approuvé', 'Approuvé'),
            ('Rejeté', 'Rejeté'),
        ],
        default='En attente'
    )
    approuve_par_comite = models.BooleanField(default=False)
    commentaire_rejet = models.TextField(blank=True, null=True)
    date_soutenance = models.DateField(null=True, blank=True)

    # === Nouveau : Rapport intermédiaire ===
   
   
    grille_evaluation = models.FileField(
        upload_to='grilles_evaluation/', blank=True, null=True
    )

    rapporteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='rapports_assigned'
    )
    statut_rapport = models.CharField(
        max_length=50,
        choices=[
            ('Non assigné', 'Non assigné'),
            ('Assigné', 'Assigné'),
            ('Évalué', 'Évalué'),
        ],
        default='Non assigné'
    )
    avis_rapporteur = models.CharField(
    max_length=50,
    choices=[
        ('valider', 'Validé'),
        ('avis_sr', 'Favorable sans réserve'),
        ('avis_mr', 'Favorable avec corrections mineures'),
        ('avis_mjr', 'Favorable avec corrections majeures'),
        ('refuser', 'Défavorable'),
    ],
    blank=True,
    null=True
)

    date_rapport_intermediaire = models.DateTimeField(null=True, blank=True)

    
    def jury_complet(self):
      roles = self.affectation_set.values_list('role', flat=True)
      roles_normalisés = [r.replace('é', 'e').lower() for r in roles]
      return all(r in roles_normalisés for r in ['president', 'rapporteur', 'examinateur', 'redacteur'])

    jury_complet.boolean = True
    jury_complet.short_description = "Jury complet"

    def __str__(self):
        return self.titre

    
   

# dans models.py
class Notification(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    titre = models.CharField(max_length=200, default="Notification")
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)  # Stocke le commentaire de rejet


class HistoriqueAction(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    date_action = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, default="En attente")  # Nouveau champ statut

    def __str__(self):
        return f'{self.utilisateur.username} a effectué l\'action "{self.action}" le {self.date_action} avec le statut {self.statut}'


class RapportIntermediaire(models.Model):
    fichier = models.FileField(upload_to='rapports_intermediaires/')
    these = models.ForeignKey(These, related_name='rapports_intermediaires', on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport intermédiaire pour {self.these.titre}"


class RapportFinal(models.Model):
    these = models.ForeignKey(These, on_delete=models.CASCADE, related_name='rapports_finals')
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='rapports_finals/')
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport final pour {self.these.titre}"


class Comite(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    email = models.EmailField()
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"Comité: {self.user.username} - {self.role}"


class Commentaire(models.Model):
    these = models.ForeignKey(These, on_delete=models.CASCADE)
    commentaire = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Affectation(models.Model):
    ROLE_CHOICES = [
        ('rapporteur', 'Rapporteur'),
        ('examinateur', 'Examinateur'),
        ('president', 'Président'),
        ('redacteur', 'Rédacteur'),
    ]

    these = models.ForeignKey(These, on_delete=models.CASCADE)
    professeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_affectation = models.DateTimeField(auto_now_add=True)
    grille_evaluation = models.FileField(upload_to='grilles/', blank=True, null=True)
    decision = models.CharField(max_length=50, blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('these', 'professeur', 'role')  # empêche les doublons

    def __str__(self):
        return f"{self.professeur} - {self.role} - {self.these}"



# models.py
class DemandeUtilisateur(models.Model):
    nom_complet = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('professeur', 'Professeur'), ('comite', 'Comité')])
    promotion = models.CharField(max_length=100, blank=True, null=True)  # facultatif

    def __str__(self):
        return f"{self.nom_complet} - {self.role}"




from django.db import models
from django.core.mail import send_mail

class Soutenance(models.Model):
    these = models.ForeignKey(These, on_delete=models.CASCADE)
    president = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='president_soutenance', limit_choices_to={'affectation__role': 'président'})
    rapporteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='rapporteur_soutenance', limit_choices_to={'affectation__role': 'rapporteur'})
    examinateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='examinateur_soutenance', limit_choices_to={'affectation__role': 'examinateur'})
    redacteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='redacteur_soutenance', limit_choices_to={'affectation__role': 'rédacteur'})
    date_soutenance = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Soutenance de {self.these}"

    def save(self, *args, **kwargs):
        # Si une date est ajoutée, envoyer l'email
        if self.date_soutenance:
            self.send_soutenance_email()
        super().save(*args, **kwargs)

    def send_soutenance_email(self):
      membres = [self.president, self.rapporteur, self.examinateur, self.redacteur]
      subject = f"Soutenance de la thèse {self.these.titre}"
      message = f"La date de soutenance pour la thèse {self.these.titre} a été fixée au {self.date_soutenance}."
      from_email = "rama.ali0902@gmail.com"  # Remplacez par votre email admin
      recipient_list = [membre.email for membre in membres if membre and membre.email]
    
    # ✅ Correction ici :
      if self.these.utilisateur.email:
        recipient_list.append(self.these.utilisateur.email)
      send_mail(subject, message, from_email, recipient_list)
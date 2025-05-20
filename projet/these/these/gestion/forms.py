from django import forms
from .models import Commentaire, DemandeInscription, RapportIntermediaire

# forms.py
from django import forms
from .models import DemandeInscription

class DoctorantInscriptionForm(forms.ModelForm):
    class Meta:
        model = DemandeInscription
        fields = ['nom_complet', 'email', 'promotion', 'adresse', 'date_naissance']
    
    def clean_nom_complet(self):
        nom_complet = self.cleaned_data.get('nom_complet')
        # Validation personnalisée du nom
        return nom_complet
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Validation personnalisée de l'email
        return email

    
from django import forms

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

from django import forms
from .models import These, Utilisateur

class TheseForm(forms.ModelForm):
    class Meta:
        model = These
        fields = ['titre', 'domaine', 'description', 'motivation', 'encadreur', 'fichier']
        widgets = {
            'domaine': forms.Select(choices=These._meta.get_field('domaine').choices),
            'description': forms.Textarea(attrs={'rows': 3}),
            'motivation': forms.Textarea(attrs={'rows': 3}),
            'encadreur': forms.Select(choices=[(u.id, u.nom) for u in Utilisateur.objects.filter(role='professeur')])
        }

 # Formulaire pour les commentaires du comité
class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['commentaire']


from django import forms
from .models import  These

class RapportIntermediaireForm(forms.ModelForm):
    class Meta:
        model = RapportIntermediaire
        fields = ['titre', 'fichier']

        
        
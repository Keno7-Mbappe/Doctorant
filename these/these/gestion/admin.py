from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, DemandeInscription

class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Infos', {'fields': ('nom', 'email', 'adresse', 'specialite', 'promotion', 'date_naissance')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_active', 'is_staff')}),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

from django.contrib import admin
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import Utilisateur, DemandeInscription
import secrets

@admin.register(DemandeInscription)
class DemandeInscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'promotion')
    actions = ['valider_demande']  # Action pour valider la demande d'inscription

    def valider_demande(self, request, queryset):
        for demande in queryset:
            # Générer un mot de passe aléatoire
            mot_de_passe = secrets.token_urlsafe(8)
            # Créer un nouvel utilisateur avec les informations de la demande
            utilisateur = Utilisateur.objects.create(
                username=demande.email,
                nom=demande.nom_complet,
                email=demande.email,
                role='doctorant',
                password=make_password(mot_de_passe),
                password_changed=False
            )
            # Envoyer l'email à l'utilisateur
            send_mail(
                subject='Votre compte a été créé',
                message=f'Bonjour {demande.nom_complet},\n\nVos identifiants sont :\nEmail: {demande.email}\nMot de passe: {mot_de_passe}',
                from_email=None,
                recipient_list=[demande.email],
                fail_silently=False,
            )
            # Supprimer la demande après validation
            demande.delete()
        # Message de confirmation pour l'admin
        self.message_user(request, "Comptes créés avec succès et emails envoyés.")

    # Description de l'action dans l'interface admin
    valider_demande.short_description = "Valider les demandes sélectionnées"


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'nom', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('email', 'nom', 'username')




# gestion/admin.py
import secrets
from django.contrib import admin
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import DemandeUtilisateur, Utilisateur  # Assure-toi d'importer les bons modèles

@admin.register(DemandeUtilisateur)
class DemandeUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'role')
    actions = ['valider_utilisateur']

    def valider_utilisateur(self, request, queryset):
        for demande in queryset:
            if Utilisateur.objects.filter(email=demande.email).exists():
                self.message_user(request, f"L'email {demande.email} est déjà utilisé.", level='error')
                continue

            mot_de_passe = secrets.token_urlsafe(8)
            utilisateur = Utilisateur.objects.create(
                username=demande.email,
                nom=demande.nom_complet,
                email=demande.email,
                role=demande.role,
                password=make_password(mot_de_passe),
                password_changed=False
            )
            send_mail(
                subject='Votre compte a été créé',
                message=f'Bonjour {demande.nom_complet},\n\nVos identifiants sont :\nEmail: {demande.email}\nMot de passe: {mot_de_passe}',
                from_email=None,
                recipient_list=[demande.email],
                fail_silently=False,
            )
            demande.delete()

        self.message_user(request, "Comptes validés avec succès.")

    valider_utilisateur.short_description = "Valider les utilisateurs sélectionnés (Professeur/Comité)"



from django.contrib import admin
from .models import Soutenance, These, Affectation
from .admin_forms import SoutenanceAdminForm

class SoutenanceAdmin(admin.ModelAdmin):
    form = SoutenanceAdminForm

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        these_id = request.GET.get('these')

        if these_id:
            try:
                these = These.objects.get(id=these_id)
                affectations = Affectation.objects.filter(these=these)
                roles = {a.role.replace('é', 'e'): a.professeur.id for a in affectations}

                initial.update({
                    'these': these_id,
                    'president': roles.get('president'),
                    'rapporteur': roles.get('rapporteur'),
                    'examinateur': roles.get('examinateur'),
                    'redacteur': roles.get('redacteur'),
                })
            except These.DoesNotExist:
                pass
        return initial

admin.site.register(Soutenance, SoutenanceAdmin)
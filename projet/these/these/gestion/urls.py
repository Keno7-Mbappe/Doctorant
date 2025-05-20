from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomPasswordChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    #pour la page de presentataion 
    path('presentation/', views.presentation, name='presentation'),
    path('apropo/', views.apropo, name='apropo'),
    path('demande-inscription/', views.demande_inscription, name='demande_inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion_etudiant, name='deconnexion_etudiant'),
    path('deconnexion_comite/', views.deconnexion_comite, name='deconnexion_comite'),
    path('deconnexion_professeur/', views.deconnexion_professeur, name='deconnexion_professeur'),
    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('mot-de-passe-oublie/envoye/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reinitialiser/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('accueil/', views.accueil_etudiant, name='accueil_etudiant'),
    path('guide_etudiant', views.guide_etudiant, name='guide_etudiant'),
    path('copie_zero/', views.copie_zero, name='copie_zero'),
    path('rapport_intermediaire/', views.rapport_intermediaire, name='rapport_intermediaire'),
    path('profil/', views.profil_etudiant, name='profil_etudiant'),
    path('rapport_final/', views.rapport_final, name='rapport_final'),
    path('historique/', views.historique_these, name='historique'),
    path('accueil_comite/', views.accueil_comite, name='accueil_comite'), 
    path('guide_comite', views.guide_comite, name='guide_comite'),
    path('decision-these/<int:these_id>/', views.decision_these, name='decision_these'),
    path('verifier_titre/', views.verifier_titre, name='verifier_titre'),
     path('approuver_rapport_intermediaire/<int:id>/', views.approuver_rapport_intermediaire, name='approuver_rapport_intermediaire'),
    path('approuver_rapport_final/<int:id>/', views.approuver_rapport_final, name='approuver_rapport_final'),
    path('assigner-rapporteur/<int:these_id>/', views.assigner_rapporteur, name='assigner_rapporteur'),
    path('accueil_prof/', views.accueil_prof, name='accueil_prof'), 
    path('guide_prof', views.guide_prof, name='guide_prof'),
    path('page_rapporteur', views.page_rapporteur, name='page_rapporteur'),
    path('rapport_inter/', views.rapport_intermediaire_view, name='rapport_inter'),
    path('tableau_theses_comite/', views.tableau_theses_comite, name='tableau_theses_comite'),
    path('theses_academiques/', views.theses_academiques, name='theses_academiques'),
    path('approuver_these/<int:these_id>/', views.approuver_these, name='approuver_these'),
    path('rejeter_these/<int:these_id>/', views.rejeter_these, name='rejeter_these'),
    path('commenter_these/<int:these_id>/', views.commenter_these, name='commenter_these'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('composition_jury/', views.composition_jury, name='composition_jury'),
    path('composition_jury/<int:these_id>/valider/', views.valider_composition, name='valider_composition'),
    path('soutenances/', views.liste_soutenances, name='liste_soutenances'),
    path('verifier_plagiat/<int:these_id>/', views.verifier_plagiat, name='verifier_plagiat'),
    path('verifier_plagiat_rapport/<int:these_id>/', views.verifier_plagiat_rapport, name='verifier_plagiat_rapport'),
    path('verifier_titre/', views.verifier_titre, name='verifier_titre'),
    path('changer-mot-de-passe/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('changer-mot-de-passe/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profil_comite/', views.profil_comite, name='profil_comite'),
    path('profil_prof/', views.profil_prof, name='profil_prof'),
    

    

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


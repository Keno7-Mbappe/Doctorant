
from django import forms
from .models import Soutenance, These, Affectation

class SoutenanceAdminForm(forms.ModelForm):
    class Meta:
        model = Soutenance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SoutenanceAdminForm, self).__init__(*args, **kwargs)

        # Filtrer uniquement les thèses avec jury complet
        theses_avec_jury = []
        for these in These.objects.all():
            roles = these.affectation_set.values_list('role', flat=True)
            roles_normalisés = [r.replace('é', 'e') for r in roles]
            if all(r in roles_normalisés for r in ['president', 'rapporteur', 'examinateur', 'redacteur']):
                theses_avec_jury.append(these.id)
        self.fields['these'].queryset = These.objects.filter(id__in=theses_avec_jury)

        # Pré-remplissage si une thèse est sélectionnée
        if 'these' in self.initial:
            these = self.initial['these']
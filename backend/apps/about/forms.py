from django import forms


class ContactForm(forms.Form):
    name = forms.EmailField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Тема', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение', widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'height: 12rem'}))

    def __str__(self):
        return self.email

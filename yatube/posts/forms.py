from django import forms

from .models import Post, Group


class PostForm(forms.Form):
    class Meta:
        model = Post

    text = forms.CharField(widget=forms.Textarea, label='Текст поста')
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Группа',
        help_text='Группа, к которой будет относиться пост',
    )

    def clean_text(self):
        data = self.cleaned_data['text']
        if not data:
            raise forms.ValidationError('Пост не можеть быть без текста!')
        return data

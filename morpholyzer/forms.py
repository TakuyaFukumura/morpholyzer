from django import forms


class TextAnalysisForm(forms.Form):
    """日本語テキスト入力フォーム"""
    text = forms.CharField(
        label='解析したいテキスト',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 50,
            'placeholder': '日本語のテキストを入力してください...',
            'class': 'form-control'
        }),
        help_text='形態素解析を行いたい日本語テキストを入力してください。',
        max_length=1000,
        required=True
    )
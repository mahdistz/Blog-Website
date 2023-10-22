from django import forms
from blog_post.models import User, Post, Comment, Category, Tag


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password


class CreateEditPostForm(forms.ModelForm):
    category = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_category(self):
        category_name = self.cleaned_data['category'].strip()
        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            return category
        return None

    def clean_tag(self):
        tag_names = self.cleaned_data['tag'].split(',') if self.cleaned_data['tag'] else []
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            tags.append(tag)
        return tags


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

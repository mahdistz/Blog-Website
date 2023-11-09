from django import forms
from blog_post.models import User, Post, Comment, Tag, Profile


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


class CreatePostForm(forms.ModelForm):
    tags = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_tags(self):
        tag_names = self.cleaned_data['tags'].split(',') if self.cleaned_data['tags'] else []
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            tags.append(tag)
        return tags


class UpdatePostForm(forms.ModelForm):
    tags = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags']

    def clean_tags(self):
        tag_names = self.cleaned_data['tags'].split(',') if self.cleaned_data['tags'] else []
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            tags.append(tag)
        return tags


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

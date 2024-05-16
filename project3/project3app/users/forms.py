from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) )

class PlayerForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) )
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}) )
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Surname'}) )
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Date of Birth'}))
    height = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Height'}) )
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Weight'}) )

class CoachForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) )
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}) )
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Surname'}) )
    nationality = forms.CharField(widget=forms.TextInput(attrs={'placeholder:': 'Nationality'}) )

class JuryForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) )
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}) )
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Surname'}) )
    nationality = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nationality'}) )

class StadiumNameUpdateForm(forms.Form):
    stadium_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Stadium ID'}) )
    new_stadium_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New Stadium Name'}) )

class MatchSessionDeleteForm(forms.Form):
    session_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Session ID'}) )

class MatchSessionForm(forms.Form):
    session_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Session ID'}) )
    stadium_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Stadium ID'}) )
    time_slot = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Time Slot'}) )
    date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Date'}) )
    jury_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jury Name'}) )
    jury_surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jury Surname'}) )

class SessionSquadsForm(forms.Form):
    player1Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 1 Name'}) )
    player1Surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 1 Surname'}) )
    player1position = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Player 1 Position'}) )
    player2Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 2 Name'}) )
    player2Surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 2 Surname'}) )
    player2position = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Player 2 Position'}) )
    player3Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 3 Name'}) )
    player3Surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 3 Surname'}) )
    player3position = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Player 3 Position'}) )
    player4Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 4 Name'}) )
    player4Surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 4 Surname'}) )
    player4position = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Player 4 Position'}) )
    player5Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 5 Name'}) )
    player5Surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 5 Surname'}) )
    player5position = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Player 5 Position'}) )
    player6Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 6 Name'}) )
    player6Surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Player 6 Surname'}) )
    player6position = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Player 6 Position'}) )

class JuryRateForm(forms.Form):
    session_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Session ID'}) )
    rating = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Rating'}) )
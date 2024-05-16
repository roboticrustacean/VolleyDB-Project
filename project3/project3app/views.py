from django.shortcuts import render, redirect
from django.http import HttpResponse
from project3app.users.login import *
from project3app.users.forms import *
from project3app.dbmanager import *
from project3app.coach import *
from project3app.jury import *
from project3app.player import *
from django.contrib import messages

# Create your views here.
def index(request):
    index_text = "view.index() called."
    context = {'index_text': index_text}
    return render(request, 'renders/index.html', context)

def printNumber(request,number):
    numbers = [i for i in range(number,number+5)]
    arr = []
    for i in range(len(numbers)):
        arr.append({"index":i,"number":numbers[i]})
    return render(request, 'renders/numbers.html', {"arr":arr})

def printString(request,string):
    return HttpResponse("view.printString() called with string: "+string)

def loginIndex(request):
    context = {'login_fail': False, 'login_form': LoginForm()}
    return render(request, 'project3app/login.html', context)

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    loginCheck = CheckCredentials(username, password)

    if loginCheck == 1:  # Admin
        request.session['username'] = username
        return redirect('../admin_home/')
    elif loginCheck == 2:  # Player
        request.session['username'] = username
        return redirect('../player_home/')
    elif loginCheck == 3:  # Coach
        request.session['username'] = username
        return redirect('../coach_home/')
    elif loginCheck == 4:  # Jury
        request.session['username'] = username
        return redirect('../jury_home/')
    else:
        context = {'login_fail': True, 'login_form': LoginForm()}
        return render(request, 'project3app/login.html', context)

def home(request):
    username = request.session['username']
    return render(request, 'project3app/home.html', {'username': username})


def admin_home(request):
    # Instantiate the forms
    player_form = PlayerForm()
    coach_form = CoachForm()
    jury_form = JuryForm()
    stadium_name_update_form = StadiumNameUpdateForm()

    if request.method == 'POST':
        # Check if the submitted form is for adding a player
        if 'add_player' in request.POST:
            player_form = PlayerForm(request.POST)  # Bind the form data to the request POST data
            if player_form.is_valid():
                # If the form data is valid, extract the data and call the function to add player to the database
                username = player_form.cleaned_data['username']
                password = player_form.cleaned_data['password']
                name = player_form.cleaned_data['name']
                surname = player_form.cleaned_data['surname']
                date_of_birth = player_form.cleaned_data['date_of_birth']
                height = player_form.cleaned_data['height']
                weight = player_form.cleaned_data['weight']

                if add_player(username, password, name, surname, date_of_birth, height, weight):
                    messages.success(request, 'Player added successfully!', extra_tags="add_player_msg")  # Display success message
                    return redirect('admin_home')  # Redirect to a different URL after successful addition
                else:
                    # Handle error if player is not added
                    messages.error(request, 'Player not added!', extra_tags="add_player_msg")
                    return redirect('admin_home')
                
        # Check if the submitted form is for adding a coach
        elif 'add_coach' in request.POST:
            coach_form = CoachForm(request.POST)  # Bind the form data to the request POST data
            if coach_form.is_valid():
                # If the form data is valid, extract the data and call the function to add coach to the database
                username = coach_form.cleaned_data['username']
                password = coach_form.cleaned_data['password']
                name = coach_form.cleaned_data['name']
                surname = coach_form.cleaned_data['surname']
                nationality = coach_form.cleaned_data['nationality']

                if add_coach(username, password, name, surname, nationality):
                    messages.success(request, 'Coach added successfully!', extra_tags="add_coach_msg")
                    return redirect('admin_home')
                else:
                    messages.error(request, 'Coach not added!', extra_tags="add_coach_msg")
                    return redirect('admin_home')

        # Check if the submitted form is for adding a jury member
        elif 'add_jury' in request.POST:
            jury_form = JuryForm(request.POST)  # Bind the form data to the request POST data
            if jury_form.is_valid():
                # If the form data is valid, extract the data and call the function to add jury member to the database
                username = jury_form.cleaned_data['username']
                password = jury_form.cleaned_data['password']
                name = jury_form.cleaned_data['name']
                surname = jury_form.cleaned_data['surname']
                nationality = jury_form.cleaned_data['nationality']

                if add_jury(username, password, name, surname, nationality):
                    messages.success(request, 'Jury member added successfully!', extra_tags="add_jury_msg")
                    return redirect('admin_home')
                else:
                    messages.error(request, 'Jury member not added!', extra_tags="add_jury_msg")
                    return redirect('admin_home')

        # Check if the submitted form is for updating the stadium name
        elif 'update_stadium_name' in request.POST:
            stadium_name_update_form = StadiumNameUpdateForm(request.POST)  # Bind the form data to the request POST data
            if stadium_name_update_form.is_valid():
                # If the form data is valid, extract the data and call the function to update the stadium name
                stadium_id = stadium_name_update_form.cleaned_data['stadium_id']
                new_stadium_name = stadium_name_update_form.cleaned_data['new_stadium_name']

                if update_stadium_name(stadium_id, new_stadium_name):
                    messages.success(request, 'Stadium name updated successfully!', extra_tags="update_stadium_name_msg")
                    return redirect('admin_home')
                else:
                    messages.error(request, 'Stadium name not updated!', extra_tags="update_stadium_name_msg")
                    return redirect('admin_home')
    
        

    # Pass the form instances to the template context
    context = {
        'player_form': player_form,
        'coach_form': coach_form,
        'jury_form': jury_form,
        'stadium_name_update_form': stadium_name_update_form
    }

    # Render the admin home template with the forms
    return render(request, 'project3app/admin_home.html', context)

def player_home(request):
    username = request.session.get('username')
    
    # Call the functions from player.py
    former_teammates = view_former_teammates(username)
    average_height = most_played_with_height(username)

    context = {
        'username': username,
        'former_teammates': former_teammates,
        'average_height': average_height
    }
    
    return render(request, 'project3app/player_home.html', context)

def coach_home(request):
    username = request.session.get('username')
    # Instantiate the forms
    match_session_delete_form = MatchSessionDeleteForm()
    match_session_form = MatchSessionForm()
    session_squads_form = SessionSquadsForm()

    stadiums = list_all_stadiums()
    print(stadiums)

    if request.method == 'POST':
        
        if 'delete_match_session' in request.POST:
            match_session_delete_form = MatchSessionDeleteForm(request.POST)
            if match_session_delete_form.is_valid():
                session_id = match_session_delete_form.cleaned_data['session_id']

                if delete_match_session(session_id):
                    messages.success(request, 'Match session deleted successfully!', extra_tags="delete_match_session_msg")
                    return redirect('coach_home')
                else:
                    messages.error(request, 'Match session not deleted!', extra_tags="delete_match_session_msg")
                    return redirect('coach_home')
        elif 'add_match_session' in request.POST:
            match_session_form = MatchSessionForm(request.POST)
            if match_session_form.is_valid():

                team_id = get_current_team(username)
                if team_id == None:
                    messages.error(request, 'Team not found!', extra_tags="add_match_session_msg")
                    return redirect('coach_home')
                session_id = match_session_form.cleaned_data['session_id']
                stadium_id = match_session_form.cleaned_data['stadium_id']
                time_slot = match_session_form.cleaned_data['time_slot']
                date = match_session_form.cleaned_data['date']
                jury_name = match_session_form.cleaned_data['jury_name']
                jury_surname = match_session_form.cleaned_data['jury_surname']

                # Assign the session_id returned by add_match_session to added_session_id
                added_session_id = add_match_session(session_id, team_id, stadium_id, time_slot, date, jury_name, jury_surname)
                if added_session_id is not None:
                    request.session['added_session_id'] = added_session_id
                    messages.success(request, 'Match session added successfully!', extra_tags="add_match_session_msg")
                else:
                    messages.error(request, 'Match session not added!', extra_tags="add_match_session_msg")
                return redirect('coach_home')
        elif 'create_session_squads' in request.POST:
            session_squads_form = SessionSquadsForm(request.POST)
            if session_squads_form.is_valid():
                team_id = get_current_team(username)
                if team_id is None:
                    messages.error(request, 'Team not found!', extra_tags="create_session_squads_msg")
                    return redirect('coach_home')
                players = []
                for i in range(1,7):
                    player_name = session_squads_form.cleaned_data['player'+str(i)+'Name']
                    player_surname = session_squads_form.cleaned_data['player'+str(i)+'Surname']
                    position_id = session_squads_form.cleaned_data['player'+str(i)+'position']
                    player = (player_name, player_surname, position_id)
                    players.append(player)
            added_session_id = request.session.get('added_session_id')
            print(players)
            print(added_session_id)
            if added_session_id is None:
                messages.error(request, 'Match session not added!', extra_tags="create_session_squads_msg")
                return redirect('coach_home')
            if create_session_squad(added_session_id, team_id, players):
                messages.success(request, 'Squads created successfully!', extra_tags="create_session_squads_msg")
                return redirect('coach_home')
            else:
                messages.error(request, 'Squads not created!', extra_tags="create_session_squads_msg")
                return redirect('coach_home')
    # Pass the form instances to the template context
    context = {
        'username': username,
        'match_session_delete_form': match_session_delete_form,
        'match_session_form': match_session_form,
        'session_squads_form': session_squads_form,
        'stadiums': stadiums
    }    

    return render(request, 'project3app/coach_home.html', context)

def jury_home(request):
    username = request.session.get('username')

    rating_avg = average_rating(username)
    rating_count = number_of_ratings(username)

    jury_rate_form = JuryRateForm()
    if request.method == 'POST':
        if 'rate_session' in request.POST:
            jury_rate_form = JuryRateForm(request.POST)
            if jury_rate_form.is_valid():
                session_id = jury_rate_form.cleaned_data['session_id']
                rating = jury_rate_form.cleaned_data['rating']

                if rate_session(session_id, username, rating):
                    messages.success(request, 'Rating submitted successfully!', extra_tags="rate_session_msg")
                    return redirect('jury_home')
                else:
                    messages.error(request, 'Rating not submitted!', extra_tags="rate_session_msg")
                    return redirect('jury_home')
    context = {
        'username': username,
        'rating_avg': rating_avg,
        'rating_count': rating_count,
        'jury_rate_form': jury_rate_form
    }
    return render(request, 'project3app/jury_home.html', context)
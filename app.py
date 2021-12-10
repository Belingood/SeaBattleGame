import random
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from forms.game_forms import StartForm, ReviewForm
from sea_battle_game import SeaBattleGame
from datetime import datetime

# Dictionary of text content for different languages
texts = {'restart': {'eng': 'Restart', 'rus': 'Начать заново'},
         'go': {'eng': 'GO', 'rus': 'ВПЕРЁД'},
         'ships_rule': {'eng': 'There must be a distance of at least one cell between the ships. You need to arrange: ',
                        'rus': 'Между кораблями должна быть дистанция минимум одна клетка. Вам нужно расставить: '},
         'pcs': {'eng': 'pcs.', 'rus': 'шт.'},
         'game': {'eng': 'Game', 'rus': 'Играть'},
         'decks': {'eng': 'Number of ships decks', 'rus': 'Количество палуб'},
         'note': {'eng': 'Note the coordinates for the shots, maximum: ',
                  'rus': 'Отметьте координаты для выстрелов, максимум: '},
         'shots': {'eng': 'shots fired at you by an opponent', 'rus': 'выстрелов произвёл по вам соперник'},
         'fire': {'eng': 'Fire', 'rus': 'Огонь'},
         'send': {'eng': 'Send', 'rus': 'Отправить'},
         'review': {'eng': 'Write a review about the game', 'rus': 'Написать отзыв об игре'}
         }


app = Flask(__name__)
app.config.from_object(Config)

# Start page
@app.route('/index/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    global sbg, rival_sea, count_fire_use, count_fire_rival, coord_for_fire_rival
    # Create a game object
    sbg = SeaBattleGame()
    # Place enemy ships (automatically) through a special function
    rival_sea = sbg.ships_randomizer()
    # Generating a random number of shots for the user
    count_fire_use = sbg.counter_fire()
    # The number of shots fired by the rival
    count_fire_rival = 0
    # List of coordinates of the player's field for the opponent's shots
    coord_for_fire_rival = [str(i) + str(j) for i in range(10) for j in range(10)]
    form = StartForm()
    if form.validate_on_submit():
        global name_frm, language
        # Set the username from the form
        name_frm = form.name.data
        # Set the language from the form
        language = form.language.data
        # Get the way of placing ships
        rand = form.rand.data
        if rand == 'manual':
            # Redirected to the manual ships placement page
            return redirect(url_for('custom'))
        elif rand == 'auto':
            # Call the function of random placement of ships
            auto_sea = sbg.ships_randomizer()
            global use_sea
            use_sea = auto_sea
            # Redirected to the page of game
            return redirect(url_for('game'))

    return render_template('index.html',
                           form=form,
                           texts=texts,
                           language='eng')


# The page of the manual placement of ships
@app.route('/custom/', methods=['GET', 'POST'])
def custom():
    # Empty list of coordinates
    c_ships = []
    # Whether it is necessary to check the number of ships (for the first opening of the page - False)
    pst = False
    if request.method == 'POST':
        # Get a list of marked checkboxes of the 'ij' format
        c_ships = request.form.getlist('user_custom_ships')
        # Turn on the check of the number of ships
        pst = True
    global sbg
    # Create a field where empty cells are assigned = 0, and marked cells = 1
    n_sea = sbg.manual_placement_marking(c_ships)
    # Check if there is an intersection of ships
    er = sbg.intersection_reviewer(n_sea)
    # Check the number and size of ships
    cnt = sbg.ships_counter(n_sea)
    # Return a dictionary with statistics about placed ships
    res = sbg.resultant(er, cnt)
    # If the number of ships is correct and if ships are not intersection
    if res['Ships count'] == 'Correct' and 'Good' in res['Allocation']:
        global use_sea
        use_sea = n_sea
        # Redirecting to the game page
        return redirect(url_for('game'))
    # If the form was involved and ships are not correct - form a flash message
    elif pst:
        # If count of ships is incorrect
        if res['Ships count'] != 'Correct':
            warn_mes_1 = {'eng': 'Ships count or/and size is not correct!',
                          'rus': 'Неправильное количество кораблей и/или их размеры!'}[language]
        else:
            warn_mes_1 = ''
        # If ships are intersection
        if 'Good' not in res['Allocation']:
            warn_mes_2 = {'eng': 'Ships are intersection!', 'rus': 'Корабли пересекаются!'}[language]
        else:
            warn_mes_2 = ''
        flash(f'{warn_mes_1} {warn_mes_2}')

    return render_template('custom.html',
                           er=er,
                           c_ships=c_ships,
                           texts=texts,
                           language=language)


# The game page
@app.route('/game/', methods=['GET', 'POST'])
def game():
    global use_sea, rival_sea, count_fire_use, count_fire_rival
    use_sea_game = use_sea
    rival_sea_game = rival_sea
    # The background color of flash message
    win_color = 'green'
    # The visibility of shoot-button
    button_display = 'inline-block'

    if request.method == 'POST':
        # Get a list of marked checkboxes of the 'ij' format
        fire_rival = request.form.getlist('rival_ships')
        # Marking shots on the opponent's field
        rival_sea_game = sbg.clarif_damage(rival_sea_game, fire_rival, count_fire_use)
        # Generate the number of shots for the opponent
        count_fire_rival = sbg.counter_fire()
        # The set of coordinates, where it makes no sense to shoot
        dont_shoot = sbg.counting_survivors(use_sea_game)[1]

        # Remove unnecessary coordinates from the list for shots
        for crd in dont_shoot:
            if crd in coord_for_fire_rival:
                coord_for_fire_rival.remove(crd)

        # Shuffle the list of coordinates for shots
        random.shuffle(coord_for_fire_rival)

        # Collect coordinates for shots at the player's ships in this turn
        fire_use = []
        for _ in range(count_fire_rival):
            try:
                fire_use.append(coord_for_fire_rival.pop())
            except IndexError:
                break

        # Update the player field
        use_sea_game = sbg.clarif_damage(use_sea_game, fire_use, count_fire_rival)
        # Generate a random number of shots for the user
        count_fire_use = sbg.counter_fire()

    # The count of survivors ships for user and system
    unbroken_use = sbg.counting_survivors(use_sea_game)[0]
    unbroken_rival = sbg.counting_survivors(rival_sea_game)[0]
    # The count of survivors ships more than 0 (True or False)
    live_use = sbg.counting_survivors(use_sea_game)[0] > 0
    live_rival = sbg.counting_survivors(rival_sea_game)[0] > 0

    # Form the flash message of users win or lose
    if not live_use and live_rival:
        win_color = 'red'
        button_display = 'none'
        flash({'eng': '🏊 You lose!', 'rus': '🏊 Вы проиграли!'}[language])
    elif not live_rival and live_use:
        button_display = 'none'
        flash({'eng': '🏆 You win!', 'rus': '🏆 Вы выиграли!'}[language])
    elif not live_rival and not live_use:
        button_display = 'none'
        flash({'eng': '🤷 Draw!', 'rus': '🤷 Ничия!'}[language])

    return render_template('game.html',
                           rival_sea_game=rival_sea_game,
                           use_sea_game=use_sea_game,
                           name_frm=name_frm,
                           count_fire_rival=count_fire_rival,
                           count_fire_use=count_fire_use,
                           unbroken_use=unbroken_use,
                           unbroken_rival=unbroken_rival,
                           win_color=win_color,
                           button_display=button_display,
                           texts=texts,
                           language=language)


# The review page
@app.route('/review/', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        txt = form.review.data
        dt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Write a review to file
        with open('reviews.txt', 'a', encoding='utf-8') as f:
            print(f'Date: {dt}\nName: {name_frm}\nReview: {txt}\n', file=f)
        with open('reviews.txt', 'r', encoding='utf-8') as fr:
            txt_check = txt in fr.read()
        # The message of write success
        if txt_check:
            flash({'eng': 'Message sent successfully', 'rus': 'Сообщение успешно отправлено'}[language])

    return render_template('review.html',
                           form=form,
                           texts=texts,
                           language=language)


if __name__ == '__main__':
    app.run()

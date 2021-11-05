# SeaBattleGame

![SeaBattleGame](/static/img/ships.jpg)

### Language: PYTHON
### Framework: FLASK

[![Demo](/static/img/demo.jpg)](https://sea-battle-game-flask.herokuapp.com/)

> ##### Introduction
> Games are not what I would like to do. However, in this work, the logical part fascinated me most of all. The main task in the study of the Flask framework was the study of forms. In this project, both conventional forms and forms created using WTForms.

The game is a classic naval battle from a school notebook :)
There are two options for placing ships to choose from - self-placement and automatic. Selecting the placement of ships manually triggers check functions that check the dimensions and the number of placed ships. Another function checks if there are intersections of ships and if they are placed close to each other (there is no required distance). If an incorrect placement is detected, problem areas are highlighted in color.
![SeaBattleGame](/static/img_readme/inters.jpg)

The most difficult task turned out to be writing a function for automatic placement of ships, so that the conditions for the correct size, number and required spacing of ships were met. As a result, the function completely randomly selects the orientation of each ship (horizontal or vertical) and its location on the field (at sea :)), while all the above requirements are met.
> Below are the four generated fields with ships. Each of them is unique and meets all the conditions.
![SeaBattleGame](/static/img_readme/rand.jpg)

### Game process

First, on the start page, you will be asked to enter your name, select the interface language and the method of placing the ships.

If you choose the manual method, you will be redirected to the appropriate page, otherwise your ships will be automatically arranged by the system in random order.

On the page for manual ship placement, you will be offered a special form with checkboxes in the form of a 10x10 matrix (see image above). You do not need to enter any coordinates such as "A2", "C8", etc. All you need to do is mark the checkboxes, which is very convenient, fast and more interactive.

> By the way, I had to work hard when writing a check function that would count the number of ships in accordance with their dimensions and understand whether they are all located correctly.

If the placed ships passed the check successfully, then you will be taken to the battle page.

The battle page displays your field and the enemy (system) field. On your field, you can monitor the damage inflicted on you, and mark positions for shots on the enemy's field.

The number of undamaged ship decks remaining is also available from the information. Below the system tells you how many shots you can fire in the **next turn** and how many shots your opponent **has already** fired at you.

> **A** - The number of shots fired by the opponent after your volley at him.
> **B** - The number of shots you can fire on this turn.
> ![SeaBattleGame](/static/img_readme/ab.jpg)

Each new turn, both the player and the enemy are given a **random** number of shots in the range from **0 to 5**. You yourself choose where to shoot, the system shoots at randomly selected places, while it never shoots again at the same place.

You need to mark the appropriate number of positions for firing at enemy ships. If you mark less than the number of shots dropped out, then fewer shots will be fired (as many as you marked). If you mark a more number of coordinates, then the system will randomly select the required number from the coordinates you marked and fire shots at them.

> **A** - It is required to mark 3 positions, but 12 are marked.
> **B** - Of the 12 marked, the system randomly selected 3 (allowed amount).
> ![SeaBattleGame](/static/img_readme/more.jpg)

When I tested the game, I noticed that the system is quite easy to beat. Therefore, I decided to make the system a little smarter)

I wrote a function that, when detecting a hit to your ship, excludes positions that are diagonally located relative to the damaged deck from firing. That is, those positions where a priori the ship cannot be.

![SeaBattleGame](/static/img_readme/not_shoot.jpg)
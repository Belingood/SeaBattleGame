# SeaBattleGame

![SeaBattleGame](/static/img/ships.jpg)

### Language: PYTHON
### Framework: FLASK

> ##### Introduction
> Games are not what I would like to do. However, in this work, the logical part fascinated me most of all. The main task in the study of the Flask framework was the study of forms. In this project, both conventional forms and forms created using WTForms.

The game is a classic naval battle from a school notebook :)
There are two options for placing ships to choose from - self-placement and automatic. Selecting the placement of ships manually triggers check functions that check the dimensions and the number of placed ships. Another function checks if there are intersections of ships and if they are placed close to each other (there is no required distance). If an incorrect placement is detected, problem areas are highlighted in color.
![SeaBattleGame](/static/img_readme/mark-intersection.jpg)

The most difficult task turned out to be writing a function for automatic placement of ships, so that the conditions for the correct size, number and required spacing of ships were met. As a result, the function completely randomly selects the orientation of each ship (horizontal or vertical) and its location on the field (at sea :)), while all the above requirements are met.
> Below are the four generated fields with ships. Each of them is unique and meets all the conditions.
![SeaBattleGame](/static/img_readme/random.jpg)
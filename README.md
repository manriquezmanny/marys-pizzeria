# Mary's Pizzeria
#### Video Demo:  <https://youtu.be/fGN-2rPG4fc>
#### Description: I created a simple flask application that allows users to place a pizza order for pickup at mary's pizzeria! (A hypothetical pizzeria) My app.py file runs the webapp using flask, I followed the standard flask framework of having a static folder with css and images in their own folders. I have a few templates that I route to that each extend the template.html.

#### The template.html file includes the navbar.html file! I am most proud of my menu.html template file! The menu template uses jinja variables and a for loop to easily and dynamically add or remove items from the restaurant's menu! The menu itself is a python dictionary in the app.py file. The key's in that dictionary hare named the same as the image files that correspond to them. This makes it easy to loop over each item (key) in MENU dictionary and add them to the menu template with an image, description, title etc!

#### The Checkout template lists all the items in the order, their price, and size! Each item also has a remove item button that will remove the item from the order when clicked. When an item is removed, the total price of the order is updated accordingly. I was able to do this by creating a remove function that takes an item_id value as a parameter. I get the item_id value with flask's request from the remove button's form! The remove button redirects to the remove route which then calls the remove function and updates and edits some of my global variables (The ORDER list, and the total_price). 

#### I also want to eventually replace the flash messages I use with some nice javascript innerhtml changes in the menu.html template.

#### One of the hardest parts for me in this project was getting everything to scale properly and fit inside the divs using css! I kept at it until I felt like I had reached a good point and everything fits right even when I scale my window down to a very small size!

#### When I first started this project, I wanted to include a database using sqlalchemy, but soon realized that would take a lot more time and effort than I currently have available. In the future, once I have more expericnce with flask and sqlalchemy, I do plan on updating this project to have users able to register accounts, and earn rewards points with each order!

#### The pictures I used for this project were obtained from pexels.com and are free to use! They have the license for their pictures at pexels.com/license/

#### I had a blast taking this course and look forward to taking the cs50 web development course with python next! Thank you cs50!!!
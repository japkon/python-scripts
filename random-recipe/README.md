# random-recipe

random_recipe.py takes a sender email and password, and a list of recipients and
sends the recipients a random recipe from food.com.

Every recipe on food.com has an associated category, so unwanted categories can
be added to the 'unwanted_categories' file. If a recipe's category is in the
file, it will not be emailed, and a new recipe will be randomly chosen. Each
unwanted category should be on its own line in 'unwanted_categories'.

I run the script every day at 4:00 PM with cron on my Raspberry Pi so I can get
a random dinner idea every day.

Note: The program uses Gmail as its SMTP Server, so only Gmail accounts will
work to send the emails from.

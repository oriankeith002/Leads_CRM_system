## Leads Management System.

Hi Welcome to my Leads Management System.

## About 
In this project, i am develop a leads management system to help various agents track leads that have been assigned to them. 

## Requirements
All you need for this project include:
- Python
- Django
- Tailwind CSS 

## Styling guide. 
We will be using the django crispy forms plugin to improve on the appearance of our forms. 

Install it using:
`pip install django-cripsy-forms`

Then also from the guide of django crispy forms in the docs. We are required to pick a **Template Pack**. 
There a variety of template packs but since we are working with `tailwind css`. Luckily there is a _tailwind css_ pack. 

We install it using"
`pip install crispy-tailwind`.

## Settings.
By default therese plugins require that we add them to our `settings.py` file in the django project. 

```python 
INSTALLED_APPS = [

    # third party crispy forms plugin
    'crispy_forms',
    'crispy_tailwind',
]


CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

```

## Useful Links:

More information about django plugins can be found at : https://djangopackages.org  

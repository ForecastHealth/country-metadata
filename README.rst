===================================================================
 python-botech_metadata - Standalone ISO 3166-1 country definitions
===================================================================

:Authors:
        Mike Spindel (Original creator)
        Forecast Health Australia (Author of this fork)
:Version: 0.0.1


`botech-metadata` is a module that allows quick retrieval of country information.


Regions
-------
- South Asia
- No Region
- Europe & Central Asia
- Middle East & North Africa
- East Asia & Pacific
- Sub-Saharan Africa
- Latin America & Caribbean


Income Groups
-------------
- Low income
- Lower middle income
- Upper middle income
- High income



Country details
---------------

::

  >>> from botech_metadata import countries
  >>>
  >>> countries.get('us')
  Country(name='United States', alpha2='US', alpha3='USA', numeric='840')
  >>> countries.get('ala')
  Country(name='Åland Islands', alpha2='AX', alpha3='ALA', numeric='248')
  >>> countries.get(8)
  Country(name='Albania', alpha2='AL', alpha3='ALB', numeric='008')


Country lists and indexes
-------------------------

::

  >>> from botech_metadata import countries

  >>> for c in countries:
         print(c)
  >>> Country(name='Afghanistan', alpha2='AF', alpha3='AFG', numeric='004')
  Country(name='Åland Islands', alpha2='AX', alpha3='ALA', numeric='248')
  Country(name='Albania', alpha2='AL', alpha3='ALB', numeric='008')
  Country(name='Algeria', alpha2='DZ', alpha3='DZA', numeric='012')

::

  >>> import botech_metadata

  >>> botech_metadata.countries_by_name
  >>> {'AFGHANISTAN': Country(name='Afghanistan', alpha2='AF', alpha3='AFG', numeric='004'),
  'ALBANIA': Country(name='Albania', alpha2='AL', alpha3='ALB', numeric='008'),
  'ALGERIA': Country(name='Algeria', alpha2='DZ', alpha3='DZA', numeric='012'),
  ...

  >>> botech_metadata.countries_by_numeric
  >>> {'004': Country(name='Afghanistan', alpha2='AF', alpha3='AFG', numeric='004'),
  '008': Country(name='Albania', alpha2='AL', alpha3='ALB', numeric='008'),
  '010': Country(name='Antarctica', alpha2='AQ', alpha3='ATA', numeric='010'),
  ...

  >>> botech_metadata.countries_by_alpha2
  >>> {'AD': Country(name='Andorra', alpha2='AD', alpha3='AND', numeric='020'),
  'AE': Country(name='United Arab Emirates', alpha2='AE', alpha3='ARE', numeric='784'),
  'AF': Country(name='Afghanistan', alpha2='AF', alpha3='AFG', numeric='004'),
  ...

  >>> botech_metadata.countries_by_alpha3
  >>> {'ABW': Country(name='Aruba', alpha2='AW', alpha3='ABW', numeric='533'),
  'AFG': Country(name='Afghanistan', alpha2='AF', alpha3='AFG', numeric='004'),
  'AGO': Country(name='Angola', alpha2='AO', alpha3='AGO', numeric='024'),
  ...


Countries by field
------------------

::

  >>> from botech_metadata import countries
  >>> foo = countries.find_by('income', 'low income')
  >>> print(foo)
  [Country(name='Afghanistan', alpha2='AF', alpha3='AFG', numeric='4', apolitical_name='Afghanistan', region='South Asia', income='Low income', appendix_3=True), Country(name='Burkina Faso', alpha2='BF', alpha3='BFA', numeric='854', apolitical_name='Burkina Fa...


Countries by category
---------------------

::

  >>> from botech_metadata import countries
  >>> foo = countries.countries_by_category('region')
  >>> print(foo)
  {'SOUTH ASIA': [Country(name='Afghanistan', alpha2='AF', alpha3='AFG', numeric='4', apolitical_name='Afghanistan', region='South Asia', income='Low income', appendix_3=True), Country(name='Bangladesh', alpha2='BD', alpha3='BGD', numeric='50', apolitical_name='Bangladesh', region='South Asia', income='Lower middle income', appendix_3=True), Co...

Countries by categories
---------------------

::

  >>> from botech_metadata import countries
  >>> foo = countries.countries_by_categories('region', 'income', 'appendix_3')
  >>> print(foo)
  >>> {'Latin America & Caribbean, Low income, False': [], 'Latin America & Caribbean, Low income, True': [], 'Latin America & Caribbean, No Income, False': [Country(name='Venezuela, Bolivarian Republic of', alpha2='VE', alpha3='VEN', numeric='862', apolitical_name='Venezuela, Bolivarian Republic of', region='Lat

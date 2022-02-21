test = {
  'name': 'q1.5',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Make sure your estimator is subtracting a reasonable value from the mean observation
          >>> 0.6*modifier < estimated_modifier <  1.5*modifier 
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}

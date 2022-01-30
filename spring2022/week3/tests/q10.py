test = {
  'name': '',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> type(time1) == float
          True
          >>> type(time0) == time.struct_time
          True
          >>> difftemeA == 61344000
          True
          >>> difftemeB == 61344000.0
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

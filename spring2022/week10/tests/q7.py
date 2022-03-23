test = {
  'name': '',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> test = Table.read_table('sf_salaries_2014.csv').select("salary")
          >>> len(simulate_sample_mean(test, 'salary', 100, 100)) == 100
          True
          >>> min(means) > -618
          True
          >>> max(means) < 471952.64
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
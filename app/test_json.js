var request_body = {
  'user': 'laureneliz',
  'imported': true,
  'clusters': [
    {
      'name': 'sweater',
      'avgDays': 30,
      'projects': [
        {'name': "husband sweater",
        'id': 100},
        {'name': "cat sweater",
        'id': 12}
      ]
    }
  ]
}

var delete_body = {'name': "socks",
    'clusterID': 12,
    'id': 100}

var delete_body_2 = 
    {
    "name": "husband sweater",
    "clusterID": 23,
    "id": 314
    }

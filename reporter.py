class Reporter:
    def __init__(self, name='report'):
        self.file = open(f'{name}.html', 'w')
        self.title = '<h1>Test report:</h1>'
        self.test_number = 0
        self.passed = 0
        self.failed = 0
        self.blocked = 0

    def start(self):
        self.file.write(f'<html><head><title>{self.title}</title>')
        self.file.write('<style>.PASS {color: green;} '
                        '.FAILED {color: red;} '
                        '.BLOCKED {color: blue;}</style>')
        self.file.write('</head><body>')
        self.file.write(f'<center><h2>{self.title}<h2></center>')
        self.file.write('<hr>')
        self.file.write('')

    def add_test(self, result, title=None, description=''):
        self.test_number += 1
        if result is True:
            result = 'PASS'
            self.passed += 1
        elif result is False:
            result = 'FAILED'
            self.failed += 1
        elif result == 'B':
            result = 'BLOCKED'
            self.blocked += 1
        self.file.write(f'<p><h3 class="{result}">{self.test_number} : {result} |\t\t\t {title}</h3></p>')
        self.file.write(f'<p>{description}</p>\n<hr>')

    def end(self):
        self.file.write('<hr>')
        self.file.write(f'<p>Total tests: {self.test_number} | '
                        f'Passed: {self.passed} | '
                        f'Failed: {self.failed} | '
                        f'Blocked: {self.blocked}<p>')
        self.file.write('</body></html>')


r = Reporter(name='Test')
r.title = 'Test'
r.start()
r.add_test(True, title='Test', description='Some test')
r.add_test(False, title='Another test')
r.add_test('B', title='Blocked test', description='Must be blue')
r.end()

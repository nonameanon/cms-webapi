class Reporter:
    def __init__(self, name='report'):
        self.file = open(f'{name}.html', 'w')
        self.title = '<h1>Test report:</h1>'
        self.test_number = 0
        self.passed = 0
        self.failed = 0
        self.blocked = 0

    def start(self):
        self.file.write(f'<center>{self.title}</center>')
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
        self.file.write(f'<p><h3>{self.test_number} : {result}</h3><h4>{title}</h4></p>')
        self.file.write(f'<p>{description}</p>\n<hr>')

    def end(self):
        self.file.write('<hr>')
        self.file.write(f'<p>Total tests: {self.test_number} | '
                        f'Passed: {self.passed} | '
                        f'Failed: {self.failed} | '
                        f'Blocked: {self.blocked}<p>')


r = Reporter()
r.start()
r.add_test('PASS', title='Test', description='Some test')

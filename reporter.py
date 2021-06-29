import os


class Reporter:
    def __init__(self, name='report'):
        self.cycle_results = {}
        if not os.path.exists('reports'):
            os.mkdir('reports', 0o666)
        self.file = open(f'reports/{name}.html', 'w')
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

    def cycle_start(self, title=None):
        self.file.write('<hr>')
        self.file.write(f'<p><h4>Cycle: {title}</h4></p>')
        self.file.write('<hr>')

    def cycle_end(self):
        self.file.write('<hr>')

    def end(self):
        self.file.write('<hr>')
        self.file.write(f'<p>Total tests: {self.test_number} | '
                        f'Passed: {self.passed} | '
                        f'Failed: {self.failed} | '
                        f'Blocked: {self.blocked}<p>')
        self.file.write('</body></html>')
        self.file.close()

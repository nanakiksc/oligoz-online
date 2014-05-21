import webapp2
import jinja2
import os

import oligoz

jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class OligozPage(webapp2.RequestHandler):
    def get(self):
        template_values = { 'oligos': '' }
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        oligoz_args = {
                'infile': self.request.get('fasta', default_value=''),
                'extraL': self.request.get('extraL', default_value=''),
                'extraR': self.request.get('extraR', default_value=''),
                'approx': self.request.get('approx', default_value=False)
                }
        is_allpairs = self.request.get('allpairs', default_value=False)

        pairs = oligoz.fasta_search(
                oligoz_args['infile'],
                extraL = oligoz_args['extraL'],
                extraR = oligoz_args['extraR'],
                approx = oligoz_args['approx']
                )   

        oligoz_out = oligoz.main(pairs, allpairs=is_allpairs)

        template_values = { 'oligos': oligoz_out }
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', OligozPage)], debug=True)

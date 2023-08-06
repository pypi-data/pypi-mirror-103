# Copyright 2019 Eficent <http://www.eficent.com>
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2.extensions import AsIs

def map_gender_values(cr):
  openupgrade.map_values(
        cr,
        'gender',
        'gender',
        [('man', 'male'),
         ('woman', 'female'),
         ],
        table='res_partner', write='sql')

@openupgrade.migrate()
def migrate(env, version):
  cr = env.cr
  map_gender_values(cr)
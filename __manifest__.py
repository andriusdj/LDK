{
    'name': "fostral_ldk",
    'summary': "LDK clan manager",
    'description': "Adds LDK clan management features",
    'author': "Fostral, MB",
    'website': "https://www.fostral.net/",
    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'LDK',
    'version': '1.0.0',
    'license': 'Other proprietary',
    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/castle_chest.xml',
        'views/res_partner_extend.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}


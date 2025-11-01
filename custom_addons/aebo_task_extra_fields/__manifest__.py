{
    'name': "Task Extra Fields (Order/Serial/Client)",
    'version': '18.0.1.0.1',
    'depends': ['base','project'],
    'author': "Aebo",
    'category': 'Project',
    'data': [
        'security/security.xml',
        'views/project_task_views.xml',
        'views/project_task_kanban.xml',
    ],
    'installable': True,
    'application': False,
}
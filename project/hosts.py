from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host('api', 'project.urls', name='api'),
    host('admin', 'project.admin_url', name='admin'),
)

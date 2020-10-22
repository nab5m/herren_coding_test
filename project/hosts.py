from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host('api', 'project.api_urls', name='api'),
    host('admin', 'project.admin_urls', name='admin'),
)

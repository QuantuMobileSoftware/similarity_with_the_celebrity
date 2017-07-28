import time

from invoke import task


def wait_port_is_open(host, port):
    import socket
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return
        time.sleep(1)


@task
def prepare_db(ctx):
    wait_port_is_open('db', 5432)
    ctx.run('python manage.py migrate --noinput')
    ctx.run('python manage.py collectstatic --noinput')

    # uploading file to db
    ctx.run('python manage.py import_files_2_db')


@task
def run_dev(ctx):
    prepare_db(ctx)
    ctx.run('uwsgi --ini uwsgi_dev.ini')

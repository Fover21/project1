from flask import Flask, render_template, redirect
from flask import jsonify, send_file
from flask import request, session
from functools import wraps

app = Flask(__name__)

app.secret_key = 'ward'


def warpper(fun):
    @wraps(fun)
    def inner(*args, **kwargs):
        if not session.get('username') == 'ward':
            next = request.path
            return redirect('/login?next={}'.format(next))
        ret = fun(*args, **kwargs)
        return ret

    return inner


@app.route('/')
@warpper
def index():
    # return redirect('/login')
    # return jsonify({'name': 'ward'})
    return send_file('app.py')


@app.route('/dd')
@warpper
def dd():
    # return redirect('/login')
    return jsonify({'name': 'ward'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form)
        user_info = request.form.to_dict()
        if user_info.get('user') == "1" and user_info.get('pwd') == "1":
            next = request.args.get('next')
            if next:
                ret = redirect(next)
            else:
                ret = redirect('/')
            session['username'] = "ward"
            return ret
        else:
            return '账号或密码错误'
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)

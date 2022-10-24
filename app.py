from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tarefa = request.form['content']
        nova_tarefa = Todo(content = tarefa)

        try:
            db.session.add(nova_tarefa)
            db.session.commit()
            return redirect('/')

        except:
            return 'Ocorreu um erro ao adicionar!'

    else:
        tarefas = Todo.query.order_by(Todo.data_created).all()
        return render_template('index.html', tarefas=tarefas)

@app.route('/delete/<int:id>')
def delete(id):
    deletar_tarefa = Todo.query.get_or_404(id)

    try:
        db.session.delete(deletar_tarefa)
        db.session.commit()
        return redirect('/')

    except:
        return 'Ocorreu um erro ao deletar essa tarefa!'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    tarefas = Todo.query.get_or_404(id)

    if request.method == 'POST':
        tarefas.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'Ocorreu um erro ao atualizar essa tarefa!'

    else:
        return render_template('update.html', tarefas=tarefas)

if __name__ == "__main__":
    app.run(debug=True)

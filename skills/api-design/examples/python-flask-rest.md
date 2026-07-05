# Exemplo: API REST em Python (Flask)

## Contexto

API REST simples para gerenciamento de tarefas usando Flask e SQLAlchemy.

## Estrutura

```
app/
├── __init__.py
├── models.py
├── routes.py
└── schemas.py
```

## Implementação

### models.py
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
```

### routes.py
```python
from flask import Blueprint, request, jsonify
from .models import db, Task

bp = Blueprint('tasks', __name__)

@bp.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'completed': t.completed} for t in tasks])

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title}), 201

@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'id': task.id, 'completed': task.completed})
```

## Testes

```python
def test_create_task(client):
    response = client.post('/tasks', json={'title': 'Test task'})
    assert response.status_code == 201
    assert response.json['title'] == 'Test task'

def test_list_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.json, list)
```

## Output Esperado

```bash
$ curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
{"id":1,"title":"Buy milk","completed":false}

$ curl http://localhost:5000/tasks
[{"id":1,"title":"Buy milk","completed":false}]
```

## Referências

- [Flask REST API Tutorial](https://flask.palletsprojects.com/en/2.3.x/patterns/api/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
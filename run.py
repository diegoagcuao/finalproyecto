from app import create_app, database as db  # Cambiar a 'database'

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()  # Usar 'database' en lugar de 'db'
    app.run(debug=True, host='0.0.0.0', port=8080)

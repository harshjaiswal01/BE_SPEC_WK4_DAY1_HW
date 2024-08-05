from flask import Flask
from models import db
import graphene
from schema import Query, Mutation
from flask_graphql import GraphQLView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:BAC146@localhost/movies"

db.init_app(app)

schema = graphene.Schema(query=Query, mutation=Mutation) #Represents the schema that our server will user

app.add_url_rule( #Registering endpoint /graphql, and using the GraphQLView to handle requests
    '/graphql',
    view_func= GraphQLView.as_view('graphql', schema=schema, graphiql=True) #Setting our schema and toggle the use of the GraphiQL UI
)

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True)
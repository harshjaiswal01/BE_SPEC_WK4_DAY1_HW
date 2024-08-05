import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Bakery as BakeryModel, db

class Bakery(SQLAlchemyObjectType):
    class Meta:
        model = BakeryModel #This object type should be modeled after our SQLAlchemy movie model

class Query(graphene.ObjectType):
    bakery = graphene.List(Bakery) #Can query movies which are of type Movie
    search_bakery = graphene.List(Bakery, name=graphene.String(), category=graphene.String(), price=graphene.Float())

    def resolve_bakery(self, info): #Resolvers are functions responsible for actually interacting with our db
        return db.session.execute(db.select(BakeryModel)).scalars()

    def resolve_search_bakery(root, info, name=None, category=None, price=None):        
        query = db.select(BakeryModel)
        if name:
            query = query.where(BakeryModel.name(f'%{name}%'))
        if category:
            query = query.where(BakeryModel.category.ilike(f'%{category}%'))
        if price:
            query = query.where(BakeryModel.price == price)
        results = db.session.execute(query).scalars().all()
        return results
    

class AddProduct(graphene.Mutation): #Creating our addMovie Mutation
    class Arguments: #The arguments required to add a movie
        name = graphene.String(required=True)
        title = graphene.String(required=True)
        price = graphene.Float(required=True)
 

    bakery = graphene.Field(Bakery)

    def mutate(self, info, name, category, price): #This is the function that runs when the mutation is called
        bakery = BakeryModel(name = name, category = category, price = price) #Creating an instance of MovieModel
        db.session.add(bakery)
        db.session.commit() #Adding movie to our database
        
        db.session.refresh(bakery)
        return AddProduct(bakery=bakery)
    
class UpdateProduct(graphene.Mutation):
    class Arguments: #Arguments 
        id = graphene.Int(required=True)
        name = graphene.String(required=False) #making it not required to have these fields so we can update specific pieces of info
        category = graphene.String(required=False)
        price = graphene.Float(required=False)

    bakery = graphene.Field(Bakery)

    def mutate(self, info, id, name=None, category=None, price=None):
        bakery = db.session.get(BakeryModel, id)
        if not bakery:
            return None
        if name:
            bakery.name = name
        if category:
            bakery.category = category
        if price:
            bakery.price = price

        db.session.add(bakery)
        db.session.commit()
        return UpdateProduct(bakery=bakery)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    bakery = graphene.Field(Bakery)

    def mutate(self, info, id):
        bakery = db.session.get(BakeryModel, id)
        print(info.context)
        if bakery:
            db.session.delete(bakery)
            db.session.commit()
        else:
            return DeleteProduct(bakery=bakery)
        
        return DeleteProduct(bakery=bakery)

class Mutation(graphene.ObjectType):
    create_product = AddProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()